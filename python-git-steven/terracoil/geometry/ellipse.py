from __future__ import annotations

import math
from collections.abc import Iterator
from dataclasses import dataclass

import numpy as np

from terracoil.util import AngleUtil, MathConstants, RealNumber
from . import Size2D, Vector2D
from .curve import Curve
from .enums import DimensionEnum, SpanEnum
from .segment import Segment


@dataclass(frozen=True)
class Ellipse:
  """Immutable ellipse defined by a center ``location`` and bounding ``size``."""
  location: Vector2D
  size: Size2D

  @property
  def dx(self) -> RealNumber:
    """Width of the ellipse's bounding box."""
    return self.size.width

  @property
  def dy(self) -> RealNumber:
    """Height of the ellipse's bounding box."""
    return self.size.height

  def generate_curve_segments(
    self,
    seg_cnt: int,
    gap_pct: float,
    start_angle: RealNumber = 0.0,
    span_enum: SpanEnum = SpanEnum.CURVE,
  ) -> Iterator[Curve | Vector2D | Segment]:
    """
    Yield ``seg_cnt`` equal-arc-length pieces of this ellipse, optionally
    interleaved with gap pieces, in a representation selected by ``span_enum``.

    With ``gap_pct == 0`` exactly ``seg_cnt`` items are yielded; with
    ``gap_pct > 0`` twice as many (a span piece followed by a gap piece,
    repeating). Each span piece spans an equal share of the perimeter; each
    gap piece is the ``gap_pct`` slice that follows.

    :param seg_cnt: Number of logical segments. Must be ``>= 3`` because a
      quadratic Bezier degenerates when an arc spans ``>= 180°`` (parallel
      tangents); central symmetry of an ellipse forces ``seg_cnt == 2`` to
      produce two 180° spans.
    :param gap_pct: Percentage of each segment's arc length to leave as gap
      *after* the span. Must lie in ``[0.0, 0.75]``. ``0.0`` yields no gaps;
      ``0.75`` leaves ``0.25`` for the visible span.
    :param start_angle: Where the first piece begins, in normalized turns
      ``[0.0, 1.0)`` (``0.25`` = quarter turn). Wrapped via
      :meth:`terracoil.util.AngleUtil.wrap`, so negatives and values
      ``>= 1.0`` are accepted.
    :param span_enum: What to yield for each piece —
      :attr:`SpanEnum.CURVE` yields :class:`Curve` (quadratic Bezier, with
      ``is_gap`` set on gap pieces), :attr:`SpanEnum.SEGMENT` yields
      :class:`Segment` (straight chord between endpoints), or
      :attr:`SpanEnum.MIDPOINT` yields :class:`Vector2D` (point on the ellipse
      at the arc-length midpoint of the piece).
    :raises ValueError: If ``seg_cnt < 3`` or ``gap_pct`` is outside
      ``[0.0, 0.75]``.
    """
    if seg_cnt < 3:
      raise ValueError(
        f"Segment count must be >= 3 (quadratic Bezier degenerates at >=180° spans): {seg_cnt}"
      )
    if gap_pct < 0.0 or gap_pct > 0.75:
      raise ValueError(f"Gap percentage must be between 0.0 and 0.75 (inclusive): {gap_pct}")

    samples: int = max(2048, seg_cnt * 64)
    t_table: np.ndarray = np.linspace(0.0, MathConstants.TAU, samples + 1)
    ds_dt: np.ndarray = np.sqrt((self.dx * np.sin(t_table)) ** 2 + (self.dy * np.cos(t_table)) ** 2)
    dt: float = float(t_table[1] - t_table[0])
    arc_table: np.ndarray = np.concatenate(([0.0], np.cumsum(0.5 * (ds_dt[:-1] + ds_dt[1:]) * dt)))
    perimeter: float = float(arc_table[-1])

    start_radians: float = AngleUtil.normalized_to_radians(AngleUtil.wrap(start_angle))
    arc_at_start: float = float(np.interp(start_radians, t_table, arc_table))
    segment_arc: float = perimeter / seg_cnt
    span_fraction: float = 1.0 - gap_pct
    has_gap: bool = gap_pct > 0.0

    t_current: float = start_radians
    current_arc: float = arc_at_start
    for _ in range(seg_cnt):
      span_end_arc: float = current_arc + segment_arc * span_fraction
      t_span_end: float = self._arc_to_t(span_end_arc, arc_table, t_table, perimeter)
      t_span_mid: float = self._arc_to_t((current_arc + span_end_arc) / 2.0, arc_table, t_table, perimeter)
      yield self._span_item(t_current, t_span_end, t_span_mid, span_enum, is_gap=False)

      if has_gap:
        gap_end_arc: float = current_arc + segment_arc
        t_gap_end: float = self._arc_to_t(gap_end_arc, arc_table, t_table, perimeter)
        t_gap_mid: float = self._arc_to_t((span_end_arc + gap_end_arc) / 2.0, arc_table, t_table, perimeter)
        yield self._span_item(t_span_end, t_gap_end, t_gap_mid, span_enum, is_gap=True)
        t_current = t_gap_end
      else:
        t_current = t_span_end

      current_arc += segment_arc

  def _arc_to_t(
    self,
    unwrapped_arc: float,
    arc_table: np.ndarray,
    t_table: np.ndarray,
    perimeter: float,
  ) -> float:
    """Map an unwrapped cumulative arc length back to a parametric angle (may exceed ``TAU`` on wraparound)."""
    base_arc: float = unwrapped_arc % perimeter
    wraps: int = int(unwrapped_arc // perimeter)
    return wraps * MathConstants.TAU + float(np.interp(base_arc, arc_table, t_table))

  def _point_at(self, t_radians: float) -> Vector2D:
    """Point on the ellipse at parametric angle ``t_radians`` (internal: radians)."""
    a: float = self.size.width / 2.0
    b: float = self.size.height / 2.0
    return Vector2D(self.location.x + a * math.cos(t_radians), self.location.y + b * math.sin(t_radians))

  def _span_item(
    self,
    t_start: float,
    t_end: float,
    t_mid: float,
    span_enum: SpanEnum,
    is_gap: bool,
  ) -> Curve | Vector2D | Segment:
    """Construct the yielded item for a single span piece, selected by ``span_enum``."""
    result: Curve | Vector2D | Segment
    if span_enum == SpanEnum.CURVE:
      result = self._bezier_segment(t_start, t_end, is_gap=is_gap)
    elif span_enum == SpanEnum.SEGMENT:
      result = Segment(start=self._point_at(t_start), stop=self._point_at(t_end))
    elif span_enum == SpanEnum.MIDPOINT:
      result = self._point_at(t_mid)
    else:
      raise ValueError(f"Unknown SpanEnum: {span_enum}")
    return result

  def _bezier_segment(self, t0_radians: float, t1_radians: float, is_gap: bool = False) -> Curve:
    """
    Quadratic-Bezier approximation of the elliptical arc from parametric angle
    ``t0_radians`` to ``t1_radians`` (radians, internal). The control point is
    the tangent-intersection construction on the unit circle, mapped through the
    ellipse's affine transform ``(x, y) -> (a*x + cx, b*y + cy)``.
    """
    a: float = self.size.width / 2.0
    b: float = self.size.height / 2.0
    half_span: float = (t1_radians - t0_radians) / 2.0
    mid: float = (t0_radians + t1_radians) / 2.0
    k: float = 1.0 / math.cos(half_span)
    start: Vector2D = self._point_at(t0_radians)
    end: Vector2D = self._point_at(t1_radians)
    control: Vector2D = Vector2D(self.location.x + a * k * math.cos(mid), self.location.y + b * k * math.sin(mid))
    return Curve(start=start, control=control, end=end, is_gap=is_gap)


@dataclass(frozen=True, init=False)
class GoldenEllipse(Ellipse):
  """Immutable ellipse whose bounding box has the golden ratio (phi)."""

  def __init__(
    self,
    measure: RealNumber,
    dim: DimensionEnum = DimensionEnum.WIDTH,
    location: Vector2D | None = None,
  ) -> None:
    if measure <= 0:
      raise ValueError(f"Measure must be positive: {measure}")
    (w, h) = (measure, measure / MathConstants.PHI) if dim == DimensionEnum.WIDTH else (measure * MathConstants.PHI, measure)
    object.__setattr__(self, 'location', location if location is not None else Vector2D.zero())
    object.__setattr__(self, 'size', Size2D(width=w, height=h))
