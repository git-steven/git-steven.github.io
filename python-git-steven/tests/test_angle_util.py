import math

import pytest

from terracoil.util import AngleUtil
from terracoil.util.math_constants import MathConstants


class TestAngleUtilNormalizedToRadians:
  def test_zero(self):
    assert AngleUtil.normalized_to_radians(0.0) == 0.0

  def test_full_turn(self):
    assert math.isclose(AngleUtil.normalized_to_radians(1.0), MathConstants.TAU)

  def test_quarter_turn(self):
    assert math.isclose(AngleUtil.normalized_to_radians(0.25), MathConstants.TAU / 4)

  def test_half_turn(self):
    assert math.isclose(AngleUtil.normalized_to_radians(0.5), math.pi)

  def test_int_input(self):
    assert math.isclose(AngleUtil.normalized_to_radians(1), MathConstants.TAU)


class TestAngleUtilNormalizedToDegrees:
  def test_zero(self):
    assert AngleUtil.normalized_to_degrees(0.0) == 0.0

  def test_full_turn(self):
    assert AngleUtil.normalized_to_degrees(1.0) == 360.0

  def test_quarter_turn(self):
    assert AngleUtil.normalized_to_degrees(0.25) == 90.0

  def test_half_turn(self):
    assert AngleUtil.normalized_to_degrees(0.5) == 180.0


class TestAngleUtilRadiansToNormalized:
  def test_zero(self):
    assert AngleUtil.radians_to_normalized(0.0) == 0.0

  def test_tau(self):
    assert math.isclose(AngleUtil.radians_to_normalized(MathConstants.TAU), 1.0)

  def test_pi(self):
    assert math.isclose(AngleUtil.radians_to_normalized(math.pi), 0.5)


class TestAngleUtilRadiansToDegrees:
  def test_pi(self):
    assert math.isclose(AngleUtil.radians_to_degrees(math.pi), 180.0)

  def test_tau(self):
    assert math.isclose(AngleUtil.radians_to_degrees(MathConstants.TAU), 360.0)

  def test_zero(self):
    assert AngleUtil.radians_to_degrees(0.0) == 0.0


class TestAngleUtilDegreesToNormalized:
  def test_zero(self):
    assert AngleUtil.degrees_to_normalized(0.0) == 0.0

  def test_quarter(self):
    assert AngleUtil.degrees_to_normalized(90.0) == 0.25

  def test_full(self):
    assert AngleUtil.degrees_to_normalized(360.0) == 1.0


class TestAngleUtilDegreesToRadians:
  def test_pi(self):
    assert math.isclose(AngleUtil.degrees_to_radians(180.0), math.pi)

  def test_tau(self):
    assert math.isclose(AngleUtil.degrees_to_radians(360.0), MathConstants.TAU)


class TestAngleUtilRoundTrips:
  @pytest.mark.parametrize("n", [0.0, 0.25, 0.5, 0.75, 1.25, -0.1, 2.0])
  def test_normalized_radians_round_trip(self, n: float):
    rt = AngleUtil.radians_to_normalized(AngleUtil.normalized_to_radians(n))
    assert math.isclose(rt, n)

  @pytest.mark.parametrize("d", [0.0, 90.0, 180.0, 360.0, -45.0])
  def test_degrees_radians_round_trip(self, d: float):
    rt = AngleUtil.radians_to_degrees(AngleUtil.degrees_to_radians(d))
    assert math.isclose(rt, d, abs_tol=1e-12)

  @pytest.mark.parametrize("n", [0.0, 0.25, 0.5, 0.75, 1.5, -0.5])
  def test_normalized_degrees_round_trip(self, n: float):
    rt = AngleUtil.degrees_to_normalized(AngleUtil.normalized_to_degrees(n))
    assert math.isclose(rt, n)


class TestAngleUtilWrap:
  def test_in_range_unchanged(self):
    assert AngleUtil.wrap(0.0) == 0.0
    assert AngleUtil.wrap(0.5) == 0.5
    assert AngleUtil.wrap(0.999) == 0.999

  def test_wrap_negative(self):
    assert math.isclose(AngleUtil.wrap(-0.1), 0.9)

  def test_wrap_below_negative_one(self):
    assert math.isclose(AngleUtil.wrap(-1.25), 0.75)

  def test_wrap_above_one(self):
    assert math.isclose(AngleUtil.wrap(1.25), 0.25)

  def test_wrap_far_above(self):
    assert math.isclose(AngleUtil.wrap(2.5), 0.5)

  def test_wrap_returns_float(self):
    assert isinstance(AngleUtil.wrap(0), float)
