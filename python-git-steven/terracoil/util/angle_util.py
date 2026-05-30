import math

from .math_constants import MathConstants
from .types import RealNumber


class AngleUtil:
  """
  Conversions between the three angle representations used in terracoil.

  ``normalized``: turns, where ``1.0`` = one full revolution = ``360°`` = ``2π`` rad.
  ``radians``: standard math radians.
  ``degrees``: standard degrees.
  """

  @classmethod
  def normalized_to_radians(cls, n: RealNumber) -> float:
    """Convert a normalized-turn angle to radians."""
    return float(n) * MathConstants.TAU

  @classmethod
  def normalized_to_degrees(cls, n: RealNumber) -> float:
    """Convert a normalized-turn angle to degrees."""
    return float(n) * 360.0

  @classmethod
  def radians_to_normalized(cls, r: RealNumber) -> float:
    """Convert radians to normalized turns."""
    return float(r) / MathConstants.TAU

  @classmethod
  def radians_to_degrees(cls, r: RealNumber) -> float:
    """Convert radians to degrees."""
    return float(r) * (180.0 / math.pi)

  @classmethod
  def degrees_to_normalized(cls, d: RealNumber) -> float:
    """Convert degrees to normalized turns."""
    return float(d) / 360.0

  @classmethod
  def degrees_to_radians(cls, d: RealNumber) -> float:
    """Convert degrees to radians."""
    return float(d) * (math.pi / 180.0)

  @classmethod
  def wrap(cls, n: RealNumber) -> float:
    """Reduce a normalized angle to ``[0.0, 1.0)`` via modulo (handles negatives correctly)."""
    return float(n) % 1.0
