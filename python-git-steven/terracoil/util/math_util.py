import math
from .math_constants import MathConstants
from .types import RealNumber
class MathUtil:
  @classmethod
  def is_pos(cls, v:RealNumber ):
    """ Tolerantly checks for positivity; only return true if value is over EPSILON """
    return v > MathConstants.EPSILON

  @classmethod
  def is_neg(cls, v:RealNumber ):
    """ Tolerantly checks for negativity; only return true if value is over EPSILON """
    return v < -MathConstants.EPSILON


  @classmethod
  def is_zero(cls, v:RealNumber):
    """ Tolerantly checks for zero; returns true if ``|v|`` is below EPSILON """
    return abs(v) < MathConstants.EPSILON

  @classmethod
  def is_nearly(cls, n:RealNumber, actual: RealNumber=0):
    return cls.is_zero(abs(n - actual))
