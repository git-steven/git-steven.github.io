from __future__ import annotations

from dataclasses import dataclass
from math import sqrt, atan2, cos, sin, isclose

from terracoil.util import AngleUtil, MathConstants, RealNumber


@dataclass(frozen=True)
class Vector2D:
  """
  Immutable 2D vector with the essential operations: component arithmetic,
  scalar arithmetic, dot and cross products, magnitude, normalization,
  rotation, projection, reflection, and linear interpolation.

  Instances are hashable and compare component-wise via the dataclass-generated
  ``__eq__``. For tolerance-aware comparison use :meth:`approx_equals`.
  """
  x: float
  y: float

  # --- Factory constructors -------------------------------------------------

  @classmethod
  def zero(cls) -> Vector2D:
    """Return the zero vector ``(0, 0)``."""
    return cls(0.0, 0.0)

  @classmethod
  def unit_x(cls) -> Vector2D:
    """Return the unit vector along the positive x-axis."""
    return cls(1.0, 0.0)

  @classmethod
  def unit_y(cls) -> Vector2D:
    """Return the unit vector along the positive y-axis."""
    return cls(0.0, 1.0)

  @classmethod
  def from_angle(cls, turns: RealNumber, magnitude: RealNumber = 1.0) -> Vector2D:
    """Build a vector from a polar angle in normalized ``turns`` (``1.0`` = full revolution) and a ``magnitude``."""
    radians: float = AngleUtil.normalized_to_radians(turns)
    return cls(magnitude * cos(radians), magnitude * sin(radians))

  @classmethod
  def from_tuple(cls, pair: tuple[RealNumber, RealNumber]) -> Vector2D:
    """Build a vector from an ``(x, y)`` tuple."""
    return cls(pair[0], pair[1])

  # --- Magnitude and direction ----------------------------------------------

  @property
  def magnitude_squared(self) -> float:
    """Squared magnitude; cheaper than :attr:`magnitude` for comparisons."""
    return self.x * self.x + self.y * self.y

  @property
  def magnitude(self) -> float:
    """Euclidean magnitude (length)."""
    return sqrt(self.magnitude_squared)

  @property
  def angle(self) -> float:
    """Polar angle in normalized turns ``[0.0, 1.0)``, measured counter-clockwise from the positive x-axis."""
    return AngleUtil.wrap(AngleUtil.radians_to_normalized(atan2(self.y, self.x)))

  def normalized(self) -> Vector2D:
    """Unit vector in the same direction; returns the zero vector unchanged."""
    mag: float = self.magnitude
    result: Vector2D = self
    if mag > MathConstants.EPSILON:
      result = Vector2D(self.x / mag, self.y / mag)
    return result

  def is_zero(self) -> bool:
    """True if magnitude is within ``EPSILON`` of zero."""
    return self.magnitude_squared <= MathConstants.EPSILON * MathConstants.EPSILON

  # --- Arithmetic operators -------------------------------------------------

  def __add__(self, other: Vector2D) -> Vector2D:
    return Vector2D(self.x + other.x, self.y + other.y)

  def __sub__(self, other: Vector2D) -> Vector2D:
    return Vector2D(self.x - other.x, self.y - other.y)

  def __neg__(self) -> Vector2D:
    return Vector2D(-self.x, -self.y)

  def __mul__(self, scalar: RealNumber) -> Vector2D:
    return Vector2D(self.x * scalar, self.y * scalar)

  def __rmul__(self, scalar: RealNumber) -> Vector2D:
    return self.__mul__(scalar)

  def __truediv__(self, scalar: RealNumber) -> Vector2D:
    if scalar == 0:
      raise ZeroDivisionError("Vector2D division by zero scalar")
    return Vector2D(self.x / scalar, self.y / scalar)

  def __abs__(self) -> float:
    """Magnitude, so ``abs(v)`` returns ``|v|``."""
    return self.magnitude

  # --- Vector products ------------------------------------------------------

  def dot(self, other: Vector2D) -> float:
    """Dot product ``self . other``."""
    return self.x * other.x + self.y * other.y

  def cross(self, other: Vector2D) -> float:
    """
    Scalar cross product (the z-component of the 3D cross).
    Positive when ``other`` lies counter-clockwise from ``self``.
    """
    return self.x * other.y - self.y * other.x

  # --- Geometric operations -------------------------------------------------

  def distance_to(self, other: Vector2D) -> float:
    """Euclidean distance from ``self`` to ``other``."""
    return (self - other).magnitude

  def angle_between(self, other: Vector2D) -> float:
    """
    Signed angle in normalized turns rotating ``self`` onto ``other``.
    Positive is counter-clockwise; the result lies in ``(-0.5, 0.5]``.
    """
    return AngleUtil.radians_to_normalized(atan2(self.cross(other), self.dot(other)))

  def rotated(self, turns: RealNumber) -> Vector2D:
    """Vector rotated counter-clockwise by ``turns`` (normalized; ``0.25`` = quarter turn)."""
    radians: float = AngleUtil.normalized_to_radians(turns)
    c: float = cos(radians)
    s: float = sin(radians)
    return Vector2D(self.x * c - self.y * s, self.x * s + self.y * c)

  def perpendicular(self) -> Vector2D:
    """Counter-clockwise 90-degree perpendicular."""
    return Vector2D(-self.y, self.x)

  def projected_onto(self, other: Vector2D) -> Vector2D:
    """
    Vector projection of ``self`` onto ``other``.
    Projecting onto the zero vector yields the zero vector.
    """
    denom: float = other.magnitude_squared
    result: Vector2D = Vector2D.zero()
    if denom > MathConstants.EPSILON:
      result = other * (self.dot(other) / denom)
    return result

  def reflected(self, normal: Vector2D) -> Vector2D:
    """
    Reflect ``self`` across the line whose ``normal`` is given.
    The normal need not be unit length; it is normalized internally.
    """
    unit_normal: Vector2D = normal.normalized()
    return self - unit_normal * (2.0 * self.dot(unit_normal))

  def lerp(self, other: Vector2D, t: RealNumber) -> Vector2D:
    """
    Linear interpolation toward ``other``.
    ``t=0`` returns ``self``; ``t=1`` returns ``other``.
    """
    return Vector2D(self.x + (other.x - self.x) * t, self.y + (other.y - self.y) * t)

  # --- Equality and conversion ----------------------------------------------

  def approx_equals(self, other: Vector2D, tolerance: RealNumber = MathConstants.EPSILON) -> bool:
    """Component-wise equality within ``tolerance``."""
    return isclose(self.x, other.x, abs_tol=tolerance) and isclose(self.y, other.y, abs_tol=tolerance)

  def as_tuple(self) -> tuple[float, float]:
    """Return ``(x, y)`` as a plain tuple."""
    return self.x, self.y
