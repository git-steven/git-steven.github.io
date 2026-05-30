import math
from collections.abc import Iterator

import pytest
from dataclasses import FrozenInstanceError

from terracoil.geometry import Curve, Ellipse, GoldenEllipse, Segment, Size2D, Vector2D
from terracoil.geometry.enums import DimensionEnum, SpanEnum


def _bezier_arc_length(c: Curve, samples: int = 200) -> float:
  """Polyline-approximate arc length of a quadratic Bezier."""
  ts: list[float] = [i / samples for i in range(samples + 1)]
  pts: list[Vector2D] = [
    (1 - t) ** 2 * c.start + 2 * (1 - t) * t * c.control + t ** 2 * c.end
    for t in ts
  ]
  return sum((pts[i + 1] - pts[i]).magnitude for i in range(samples))


def _ramanujan_perimeter(a: float, b: float) -> float:
  """Ramanujan's high-accuracy ellipse perimeter approximation."""
  h: float = ((a - b) / (a + b)) ** 2
  return math.pi * (a + b) * (1 + 3 * h / (10 + math.sqrt(4 - 3 * h)))


def _on_ellipse(pt: Vector2D, a: float, b: float, cx: float = 0.0, cy: float = 0.0, abs_tol: float = 1e-9) -> bool:
  """True if ``pt`` lies on the ellipse with semi-axes ``a, b`` centered at ``(cx, cy)``."""
  return math.isclose(((pt.x - cx) / a) ** 2 + ((pt.y - cy) / b) ** 2, 1.0, abs_tol=abs_tol)


class TestEllipseBasics:
  def test_construction(self):
    e = Ellipse(location=Vector2D(1.0, 2.0), size=Size2D(width=10.0, height=4.0))
    assert e.location == Vector2D(1.0, 2.0)
    assert e.size == Size2D(width=10.0, height=4.0)

  def test_dx(self):
    e = Ellipse(location=Vector2D(0.0, 0.0), size=Size2D(width=10.0, height=4.0))
    assert e.dx == 10.0

  def test_dy(self):
    e = Ellipse(location=Vector2D(0.0, 0.0), size=Size2D(width=10.0, height=4.0))
    assert e.dy == 4.0

  def test_immutability(self):
    e = Ellipse(location=Vector2D(0.0, 0.0), size=Size2D(width=10.0, height=4.0))
    with pytest.raises(FrozenInstanceError):
      e.size = Size2D(width=1.0, height=1.0)  # type: ignore[misc]

  def test_equality_and_hash(self):
    a = Ellipse(location=Vector2D(0.0, 0.0), size=Size2D(width=10.0, height=4.0))
    b = Ellipse(location=Vector2D(0.0, 0.0), size=Size2D(width=10.0, height=4.0))
    assert a == b
    assert hash(a) == hash(b)


@pytest.fixture
def ellipse() -> Ellipse:
  return Ellipse(location=Vector2D(0.0, 0.0), size=Size2D(width=10.0, height=4.0))


class TestGenerateCurveSegmentsBasics:
  def test_returns_iterator(self, ellipse: Ellipse):
    gen = ellipse.generate_curve_segments(seg_cnt=4, gap_pct=0.0)
    assert isinstance(gen, Iterator)

  def test_yields_curves(self, ellipse: Ellipse):
    segs = list(ellipse.generate_curve_segments(seg_cnt=8, gap_pct=0.0))
    assert all(isinstance(s, Curve) for s in segs)

  def test_count_matches(self, ellipse: Ellipse):
    assert len(list(ellipse.generate_curve_segments(seg_cnt=8, gap_pct=0.0))) == 8

  def test_closure(self, ellipse: Ellipse):
    segs = list(ellipse.generate_curve_segments(seg_cnt=8, gap_pct=0.0))
    assert segs[-1].end.approx_equals(segs[0].start, tolerance=1e-6)

  def test_continuity(self, ellipse: Ellipse):
    segs = list(ellipse.generate_curve_segments(seg_cnt=8, gap_pct=0.0))
    for i in range(len(segs) - 1):
      assert segs[i].end.approx_equals(segs[i + 1].start, tolerance=1e-9)

  def test_equal_arc_length_chord_proxy(self, ellipse: Ellipse):
    segs = list(ellipse.generate_curve_segments(seg_cnt=8, gap_pct=0.0))
    chords: list[float] = [(s.end - s.start).magnitude for s in segs]
    mean_chord: float = sum(chords) / len(chords)
    max_dev: float = max(abs(c - mean_chord) for c in chords)
    assert max_dev / mean_chord < 0.15

  def test_equal_arc_length_bezier_arc_proxy(self, ellipse: Ellipse):
    """Each Bezier's polyline-arc-length should be close to perimeter/N."""
    n: int = 16
    segs = list(ellipse.generate_curve_segments(seg_cnt=n, gap_pct=0.0))
    lengths: list[float] = [_bezier_arc_length(s) for s in segs]
    perimeter: float = _ramanujan_perimeter(5.0, 2.0)
    target: float = perimeter / n
    max_dev: float = max(abs(L - target) for L in lengths)
    assert max_dev / target < 0.02

  def test_perimeter_approximation(self, ellipse: Ellipse):
    """Sum of Bezier arc lengths approximates the ellipse perimeter."""
    segs = list(ellipse.generate_curve_segments(seg_cnt=12, gap_pct=0.0))
    total: float = sum(_bezier_arc_length(s) for s in segs)
    ref: float = _ramanujan_perimeter(5.0, 2.0)
    assert abs(total - ref) / ref < 0.005

  def test_translated_ellipse_segments_are_translated(self):
    e_origin = Ellipse(location=Vector2D(0.0, 0.0), size=Size2D(width=10.0, height=4.0))
    e_shift = Ellipse(location=Vector2D(7.0, -3.0), size=Size2D(width=10.0, height=4.0))
    a = list(e_origin.generate_curve_segments(seg_cnt=6, gap_pct=0.0))
    b = list(e_shift.generate_curve_segments(seg_cnt=6, gap_pct=0.0))
    for sa, sb in zip(a, b):
      assert sb.start.approx_equals(sa.start + Vector2D(7.0, -3.0), tolerance=1e-9)

  def test_circle_yields_equal_chord_lengths(self):
    """Special case: a circle has uniform arc length, so chords should be exactly equal."""
    e = Ellipse(location=Vector2D(0.0, 0.0), size=Size2D(width=10.0, height=10.0))
    segs = list(e.generate_curve_segments(seg_cnt=8, gap_pct=0.0))
    chords: list[float] = [(s.end - s.start).magnitude for s in segs]
    assert max(chords) - min(chords) < 1e-6


class TestGenerateCurveSegmentsStartAngle:
  def test_start_angle_zero_starts_at_rightmost(self, ellipse: Ellipse):
    segs = list(ellipse.generate_curve_segments(seg_cnt=8, gap_pct=0.0, start_angle=0.0))
    assert math.isclose(segs[0].start.x, 5.0)
    assert math.isclose(segs[0].start.y, 0.0, abs_tol=1e-12)

  def test_start_angle_quarter_starts_at_top(self, ellipse: Ellipse):
    segs = list(ellipse.generate_curve_segments(seg_cnt=6, gap_pct=0.0, start_angle=0.25))
    assert math.isclose(segs[0].start.x, 0.0, abs_tol=1e-9)
    assert math.isclose(segs[0].start.y, 2.0)

  def test_start_angle_half_starts_at_leftmost(self, ellipse: Ellipse):
    segs = list(ellipse.generate_curve_segments(seg_cnt=6, gap_pct=0.0, start_angle=0.5))
    assert math.isclose(segs[0].start.x, -5.0)
    assert math.isclose(segs[0].start.y, 0.0, abs_tol=1e-9)

  def test_start_angle_wraps_negative(self, ellipse: Ellipse):
    a = list(ellipse.generate_curve_segments(seg_cnt=6, gap_pct=0.0, start_angle=-0.75))
    b = list(ellipse.generate_curve_segments(seg_cnt=6, gap_pct=0.0, start_angle=0.25))
    assert a[0].start.approx_equals(b[0].start, tolerance=1e-12)

  def test_start_angle_wraps_above_one(self, ellipse: Ellipse):
    a = list(ellipse.generate_curve_segments(seg_cnt=6, gap_pct=0.0, start_angle=1.25))
    b = list(ellipse.generate_curve_segments(seg_cnt=6, gap_pct=0.0, start_angle=0.25))
    assert a[0].start.approx_equals(b[0].start, tolerance=1e-12)


class TestGenerateCurveSegmentsValidation:
  @pytest.mark.parametrize("bad_count", [-5, 0, 1, 2])
  def test_seg_cnt_guard(self, ellipse: Ellipse, bad_count: int):
    with pytest.raises(ValueError, match=">= 3"):
      list(ellipse.generate_curve_segments(seg_cnt=bad_count, gap_pct=0.0))

  @pytest.mark.parametrize("bad_gap", [-0.1, -1.0, 0.76, 1.0, 5.0])
  def test_gap_pct_guard(self, ellipse: Ellipse, bad_gap: float):
    with pytest.raises(ValueError, match="Gap percentage"):
      list(ellipse.generate_curve_segments(seg_cnt=4, gap_pct=bad_gap))

  def test_gap_pct_zero_is_valid(self, ellipse: Ellipse):
    list(ellipse.generate_curve_segments(seg_cnt=4, gap_pct=0.0))

  def test_gap_pct_max_boundary_is_valid(self, ellipse: Ellipse):
    list(ellipse.generate_curve_segments(seg_cnt=4, gap_pct=0.75))


class TestGenerateCurveSegmentsGapPct:
  def test_gap_pct_zero_yields_seg_cnt_items(self, ellipse: Ellipse):
    segs = list(ellipse.generate_curve_segments(seg_cnt=8, gap_pct=0.0))
    assert len(segs) == 8

  def test_gap_pct_positive_yields_double(self, ellipse: Ellipse):
    segs = list(ellipse.generate_curve_segments(seg_cnt=8, gap_pct=0.25))
    assert len(segs) == 16

  def test_gap_pct_alternates_is_gap_flag(self, ellipse: Ellipse):
    """With gap_pct > 0 and span_enum=CURVE, the yields alternate span/gap."""
    segs = list(ellipse.generate_curve_segments(seg_cnt=4, gap_pct=0.3))
    for i, s in enumerate(segs):
      assert isinstance(s, Curve)
      assert s.is_gap == (i % 2 == 1), f"index {i}: expected is_gap={i % 2 == 1}, got {s.is_gap}"

  def test_gap_arc_length_ratio_matches_gap_pct(self, ellipse: Ellipse):
    """span:gap arc-length ratio approximates (1-gap_pct):gap_pct."""
    n: int = 12
    gap: float = 0.2
    segs = list(ellipse.generate_curve_segments(seg_cnt=n, gap_pct=gap))
    span_lens: list[float] = [_bezier_arc_length(s) for i, s in enumerate(segs) if i % 2 == 0]
    gap_lens: list[float] = [_bezier_arc_length(s) for i, s in enumerate(segs) if i % 2 == 1]
    for sl, gl in zip(span_lens, gap_lens):
      assert math.isclose(gl / (sl + gl), gap, abs_tol=0.02)

  def test_continuity_with_gaps(self, ellipse: Ellipse):
    """Each piece's end equals the next piece's start, across span/gap boundaries."""
    segs = list(ellipse.generate_curve_segments(seg_cnt=6, gap_pct=0.2))
    for i in range(len(segs) - 1):
      assert segs[i].end.approx_equals(segs[i + 1].start, tolerance=1e-9)

  def test_closure_with_gaps(self, ellipse: Ellipse):
    segs = list(ellipse.generate_curve_segments(seg_cnt=6, gap_pct=0.2))
    assert segs[-1].end.approx_equals(segs[0].start, tolerance=1e-6)

  def test_total_arc_length_unchanged_by_gaps(self, ellipse: Ellipse):
    """Sum of (span + gap) arc lengths should still approximate the perimeter."""
    segs = list(ellipse.generate_curve_segments(seg_cnt=12, gap_pct=0.3))
    total: float = sum(_bezier_arc_length(s) for s in segs)
    ref: float = _ramanujan_perimeter(5.0, 2.0)
    assert abs(total - ref) / ref < 0.005


class TestGenerateCurveSegmentsSpanEnumCurve:
  def test_default_is_curve(self, ellipse: Ellipse):
    segs = list(ellipse.generate_curve_segments(seg_cnt=4, gap_pct=0.0))
    assert all(isinstance(s, Curve) for s in segs)

  def test_explicit_curve(self, ellipse: Ellipse):
    segs = list(ellipse.generate_curve_segments(seg_cnt=4, gap_pct=0.0, span_enum=SpanEnum.CURVE))
    assert all(isinstance(s, Curve) for s in segs)

  def test_curve_endpoints_on_ellipse(self, ellipse: Ellipse):
    segs = list(ellipse.generate_curve_segments(seg_cnt=6, gap_pct=0.0, span_enum=SpanEnum.CURVE))
    for s in segs:
      assert _on_ellipse(s.start, 5.0, 2.0)
      assert _on_ellipse(s.end, 5.0, 2.0)


class TestGenerateCurveSegmentsSpanEnumSegment:
  def test_returns_segments(self, ellipse: Ellipse):
    segs = list(ellipse.generate_curve_segments(seg_cnt=6, gap_pct=0.0, span_enum=SpanEnum.SEGMENT))
    assert all(isinstance(s, Segment) for s in segs)

  def test_count_no_gap(self, ellipse: Ellipse):
    assert len(list(ellipse.generate_curve_segments(seg_cnt=6, gap_pct=0.0, span_enum=SpanEnum.SEGMENT))) == 6

  def test_count_with_gap(self, ellipse: Ellipse):
    assert len(list(ellipse.generate_curve_segments(seg_cnt=5, gap_pct=0.2, span_enum=SpanEnum.SEGMENT))) == 10

  def test_endpoints_on_ellipse(self, ellipse: Ellipse):
    segs = list(ellipse.generate_curve_segments(seg_cnt=6, gap_pct=0.0, span_enum=SpanEnum.SEGMENT))
    for s in segs:
      assert _on_ellipse(s.start, 5.0, 2.0)
      assert _on_ellipse(s.stop, 5.0, 2.0)

  def test_continuity(self, ellipse: Ellipse):
    """Each segment's stop should equal the next segment's start."""
    segs = list(ellipse.generate_curve_segments(seg_cnt=6, gap_pct=0.0, span_enum=SpanEnum.SEGMENT))
    for i in range(len(segs) - 1):
      assert segs[i].stop.approx_equals(segs[i + 1].start, tolerance=1e-9)


class TestGenerateCurveSegmentsSpanEnumMidpoint:
  def test_returns_vector2d(self, ellipse: Ellipse):
    segs = list(ellipse.generate_curve_segments(seg_cnt=6, gap_pct=0.0, span_enum=SpanEnum.MIDPOINT))
    assert all(isinstance(s, Vector2D) for s in segs)

  def test_count_no_gap(self, ellipse: Ellipse):
    assert len(list(ellipse.generate_curve_segments(seg_cnt=6, gap_pct=0.0, span_enum=SpanEnum.MIDPOINT))) == 6

  def test_count_with_gap(self, ellipse: Ellipse):
    assert len(list(ellipse.generate_curve_segments(seg_cnt=5, gap_pct=0.2, span_enum=SpanEnum.MIDPOINT))) == 10

  def test_midpoints_on_ellipse(self, ellipse: Ellipse):
    pts = list(ellipse.generate_curve_segments(seg_cnt=6, gap_pct=0.0, span_enum=SpanEnum.MIDPOINT))
    for pt in pts:
      assert _on_ellipse(pt, 5.0, 2.0)

  def test_circle_midpoints_uniformly_spaced(self):
    """On a circle, arc-length midpoints are evenly spaced in parametric angle too."""
    e = Ellipse(location=Vector2D(0.0, 0.0), size=Size2D(width=10.0, height=10.0))
    pts = list(e.generate_curve_segments(seg_cnt=8, gap_pct=0.0, span_enum=SpanEnum.MIDPOINT))
    # First midpoint should be at parametric angle = 0.5 * (2π/8) = π/8.
    expected_first = Vector2D(5.0 * math.cos(math.pi / 8), 5.0 * math.sin(math.pi / 8))
    assert pts[0].approx_equals(expected_first, tolerance=1e-9)


class TestSpanItemUnknownEnum:
  def test_raises_value_error_for_unknown(self, ellipse: Ellipse):
    with pytest.raises(ValueError, match="Unknown SpanEnum"):
      ellipse._span_item(0.0, 0.1, 0.05, span_enum="not_an_enum", is_gap=False)  # type: ignore[arg-type]


class TestGoldenEllipse:
  def test_default_dim_is_width(self):
    g = GoldenEllipse(measure=10.0)
    assert math.isclose(g.size.width, 10.0)
    assert math.isclose(g.size.aspect_ratio, (1 + math.sqrt(5)) / 2)

  def test_dim_height(self):
    g = GoldenEllipse(measure=10.0, dim=DimensionEnum.HEIGHT)
    assert math.isclose(g.size.height, 10.0)
    assert math.isclose(g.size.aspect_ratio, (1 + math.sqrt(5)) / 2)

  def test_default_location_is_origin(self):
    assert GoldenEllipse(measure=10.0).location == Vector2D.zero()

  def test_explicit_location(self):
    g = GoldenEllipse(measure=10.0, location=Vector2D(3.0, 4.0))
    assert g.location == Vector2D(3.0, 4.0)

  def test_immutability(self):
    g = GoldenEllipse(measure=10.0)
    with pytest.raises(FrozenInstanceError):
      g.size = Size2D(width=1.0, height=1.0)  # type: ignore[misc]

  def test_validation_negative(self):
    with pytest.raises(ValueError):
      GoldenEllipse(measure=-1.0)

  def test_validation_zero(self):
    with pytest.raises(ValueError):
      GoldenEllipse(measure=0.0)

  def test_inherits_generate_curve_segments(self):
    g = GoldenEllipse(measure=10.0)
    assert len(list(g.generate_curve_segments(seg_cnt=8, gap_pct=0.0))) == 8

  def test_is_an_ellipse(self):
    assert isinstance(GoldenEllipse(measure=10.0), Ellipse)
