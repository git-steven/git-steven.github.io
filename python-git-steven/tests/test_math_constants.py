import math

from terracoil.util.math_constants import MathConstants


class TestMathConstants:
  def test_phi(self):
    assert math.isclose(MathConstants.PHI, (1.0 + math.sqrt(5.0)) / 2.0)

  def test_tau(self):
    assert math.isclose(MathConstants.TAU, 2.0 * math.pi)

  def test_epsilon_positive(self):
    assert MathConstants.EPSILON > 0.0
