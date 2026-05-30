from terracoil.util import MathUtil
from terracoil.util.math_constants import MathConstants


class TestMathUtilIsPos:
  def test_positive_returns_true(self):
    assert MathUtil.is_pos(1.0) is True

  def test_just_above_epsilon_true(self):
    assert MathUtil.is_pos(MathConstants.EPSILON * 2) is True

  def test_zero_false(self):
    assert MathUtil.is_pos(0.0) is False

  def test_negative_false(self):
    assert MathUtil.is_pos(-1.0) is False

  def test_below_epsilon_false(self):
    assert MathUtil.is_pos(MathConstants.EPSILON / 2) is False


class TestMathUtilIsNeg:
  def test_negative_true(self):
    assert MathUtil.is_neg(-1.0) is True

  def test_zero_false(self):
    assert MathUtil.is_neg(0.0) is False

  def test_positive_false(self):
    assert MathUtil.is_neg(1.0) is False

  def test_just_above_negative_epsilon_false(self):
    assert MathUtil.is_neg(-MathConstants.EPSILON / 2) is False


class TestMathUtilIsZero:
  def test_zero_true(self):
    assert MathUtil.is_zero(0.0) is True

  def test_tiny_positive_true(self):
    assert MathUtil.is_zero(MathConstants.EPSILON / 2) is True

  def test_tiny_negative_true(self):
    assert MathUtil.is_zero(-MathConstants.EPSILON / 2) is True

  def test_one_false(self):
    assert MathUtil.is_zero(1.0) is False

  def test_above_epsilon_false(self):
    assert MathUtil.is_zero(MathConstants.EPSILON * 2) is False


class TestMathUtilIsNearly:
  def test_default_actual_zero(self):
    assert MathUtil.is_nearly(0.0) is True

  def test_default_actual_zero_with_nonzero_arg(self):
    assert MathUtil.is_nearly(1.0) is False

  def test_with_actual_equal(self):
    assert MathUtil.is_nearly(5.0, actual=5.0) is True

  def test_with_actual_different(self):
    assert MathUtil.is_nearly(5.0, actual=4.0) is False
