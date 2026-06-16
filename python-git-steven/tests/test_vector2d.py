import math

import pytest
from dataclasses import FrozenInstanceError

from terracoil.geometry import Vector2D


class TestVector2DConstruction:
  def test_basic(self):
    v = Vector2D(3.0, 4.0)
    assert v.x == 3.0
    assert v.y == 4.0

  def test_immutability(self):
    v = Vector2D(1.0, 2.0)
    with pytest.raises(FrozenInstanceError):
      v.x = 5.0  # type: ignore[misc]

  def test_equality_and_hash(self):
    a = Vector2D(1.0, 2.0)
    b = Vector2D(1.0, 2.0)
    assert a == b
    assert hash(a) == hash(b)


class TestVector2DFactories:
  def test_zero(self):
    assert Vector2D.zero() == Vector2D(0.0, 0.0)

  def test_unit_x(self):
    assert Vector2D.unit_x() == Vector2D(1.0, 0.0)

  def test_unit_y(self):
    assert Vector2D.unit_y() == Vector2D(0.0, 1.0)

  def test_from_tuple(self):
    assert Vector2D.from_tuple((1.0, 2.0)) == Vector2D(1.0, 2.0)


class TestVector2DFromAngle:
  def test_zero_turns(self):
    v = Vector2D.from_angle(0.0)
    assert math.isclose(v.x, 1.0)
    assert math.isclose(v.y, 0.0, abs_tol=1e-12)

  def test_quarter_turn(self):
    v = Vector2D.from_angle(0.25)
    assert math.isclose(v.x, 0.0, abs_tol=1e-12)
    assert math.isclose(v.y, 1.0)

  def test_half_turn(self):
    v = Vector2D.from_angle(0.5)
    assert math.isclose(v.x, -1.0)
    assert math.isclose(v.y, 0.0, abs_tol=1e-12)

  def test_three_quarter_turn(self):
    v = Vector2D.from_angle(0.75)
    assert math.isclose(v.x, 0.0, abs_tol=1e-12)
    assert math.isclose(v.y, -1.0)

  def test_with_magnitude(self):
    v = Vector2D.from_angle(0.0, magnitude=3.0)
    assert math.isclose(v.x, 3.0)
    assert math.isclose(v.y, 0.0, abs_tol=1e-12)


class TestVector2DAngleProperty:
  def test_positive_x_axis_is_zero(self):
    assert math.isclose(Vector2D(1.0, 0.0).angle, 0.0, abs_tol=1e-12)

  def test_positive_y_axis_is_quarter(self):
    assert math.isclose(Vector2D(0.0, 1.0).angle, 0.25)

  def test_negative_x_axis_is_half(self):
    assert math.isclose(Vector2D(-1.0, 0.0).angle, 0.5)

  def test_negative_y_axis_is_three_quarter(self):
    assert math.isclose(Vector2D(0.0, -1.0).angle, 0.75)

  def test_angle_is_wrapped_to_unit_interval(self):
    angle: float = Vector2D(0.0, -1.0).angle
    assert 0.0 <= angle < 1.0


class TestVector2DMagnitude:
  def test_magnitude(self):
    assert Vector2D(3.0, 4.0).magnitude == 5.0

  def test_magnitude_squared(self):
    assert Vector2D(3.0, 4.0).magnitude_squared == 25.0

  def test_zero_magnitude(self):
    assert Vector2D.zero().magnitude == 0.0

  def test_abs(self):
    assert abs(Vector2D(3.0, 4.0)) == 5.0


class TestVector2DNormalization:
  def test_unit_length(self):
    v = Vector2D(3.0, 4.0).normalized()
    assert math.isclose(v.magnitude, 1.0)

  def test_zero_normalized_stays_zero(self):
    assert Vector2D.zero().normalized() == Vector2D.zero()

  def test_is_zero_true_for_zero(self):
    assert Vector2D.zero().is_zero()

  def test_is_zero_false_for_unit(self):
    assert not Vector2D(1.0, 0.0).is_zero()


class TestVector2DArithmetic:
  def test_addition(self):
    assert Vector2D(1.0, 2.0) + Vector2D(3.0, 4.0) == Vector2D(4.0, 6.0)

  def test_subtraction(self):
    assert Vector2D(4.0, 6.0) - Vector2D(1.0, 2.0) == Vector2D(3.0, 4.0)

  def test_negation(self):
    assert -Vector2D(1.0, -2.0) == Vector2D(-1.0, 2.0)

  def test_scalar_mul_right(self):
    assert Vector2D(1.0, 2.0) * 3 == Vector2D(3.0, 6.0)

  def test_scalar_mul_left(self):
    assert 3 * Vector2D(1.0, 2.0) == Vector2D(3.0, 6.0)

  def test_scalar_div(self):
    assert Vector2D(6.0, 4.0) / 2 == Vector2D(3.0, 2.0)

  def test_div_by_zero_raises(self):
    with pytest.raises(ZeroDivisionError):
      _ = Vector2D(1.0, 2.0) / 0


class TestVector2DProducts:
  def test_dot(self):
    assert Vector2D(1.0, 2.0).dot(Vector2D(3.0, 4.0)) == 11.0

  def test_cross_positive(self):
    assert Vector2D(1.0, 0.0).cross(Vector2D(0.0, 1.0)) == 1.0

  def test_cross_negative(self):
    assert Vector2D(0.0, 1.0).cross(Vector2D(1.0, 0.0)) == -1.0


class TestVector2DGeometry:
  def test_distance_to(self):
    assert Vector2D(0.0, 0.0).distance_to(Vector2D(3.0, 4.0)) == 5.0

  def test_angle_between_ccw_in_turns(self):
    a = Vector2D(1.0, 0.0)
    b = Vector2D(0.0, 1.0)
    assert math.isclose(a.angle_between(b), 0.25)

  def test_angle_between_cw_is_negative(self):
    a = Vector2D(1.0, 0.0)
    b = Vector2D(0.0, -1.0)
    assert math.isclose(a.angle_between(b), -0.25)

  def test_rotated_quarter_turn(self):
    v = Vector2D(1.0, 0.0).rotated(0.25)
    assert math.isclose(v.x, 0.0, abs_tol=1e-12)
    assert math.isclose(v.y, 1.0)

  def test_rotated_full_turn_is_identity(self):
    v = Vector2D(1.0, 0.0).rotated(1.0)
    assert math.isclose(v.x, 1.0)
    assert math.isclose(v.y, 0.0, abs_tol=1e-12)

  def test_perpendicular_ccw(self):
    assert Vector2D(1.0, 0.0).perpendicular() == Vector2D(0.0, 1.0)

  def test_projected_onto(self):
    v = Vector2D(2.0, 3.0).projected_onto(Vector2D(1.0, 0.0))
    assert v == Vector2D(2.0, 0.0)

  def test_projected_onto_zero_is_zero(self):
    v = Vector2D(2.0, 3.0).projected_onto(Vector2D.zero())
    assert v == Vector2D.zero()

  def test_reflected_across_y_axis_normal(self):
    v = Vector2D(1.0, 1.0).reflected(Vector2D(0.0, 1.0))
    assert math.isclose(v.x, 1.0)
    assert math.isclose(v.y, -1.0)

  def test_lerp_midpoint(self):
    v = Vector2D(0.0, 0.0).lerp(Vector2D(10.0, 20.0), 0.5)
    assert v == Vector2D(5.0, 10.0)

  def test_lerp_t_zero(self):
    v = Vector2D(1.0, 1.0).lerp(Vector2D(5.0, 5.0), 0.0)
    assert v == Vector2D(1.0, 1.0)

  def test_lerp_t_one(self):
    v = Vector2D(1.0, 1.0).lerp(Vector2D(5.0, 5.0), 1.0)
    assert v == Vector2D(5.0, 5.0)


class TestVector2DEquality:
  def test_approx_equals_within_tolerance(self):
    assert Vector2D(1.0, 2.0).approx_equals(Vector2D(1.0 + 1e-15, 2.0))

  def test_approx_equals_outside_tolerance(self):
    assert not Vector2D(1.0, 2.0).approx_equals(Vector2D(1.5, 2.0))

  def test_approx_equals_custom_tolerance(self):
    assert Vector2D(1.0, 2.0).approx_equals(Vector2D(1.05, 2.0), tolerance=0.1)

  def test_as_tuple(self):
    assert Vector2D(1.0, 2.0).as_tuple() == (1.0, 2.0)
