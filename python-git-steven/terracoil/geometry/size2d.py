from __future__ import annotations

from dataclasses import dataclass

from terracoil.util import RealNumber
from .enums import DimensionEnum


@dataclass(frozen=True)
class Size2D:
  """
  Immutable 2D size with width and height.
  Aspect ratio is derived as ``width / height``.
  """
  width: RealNumber
  height: RealNumber

  def __post_init__(self) -> None:
    if self.width <= 0 or self.height <= 0:
      raise ValueError(f"Width and Height must be positive numbers: w={self.width}, h={self.height}.")

  @property
  def aspect_ratio(self) -> float:
    """Aspect ratio ``width / height``."""
    return self.width / self.height

  @classmethod
  def init_with_ar(cls, measure: RealNumber, ar: float, dim: DimensionEnum = DimensionEnum.WIDTH) -> Size2D:
    """
    Build a Size2D from one dimension's ``measure`` and an aspect ratio ``ar`` (width/height).
    When ``dim`` is :attr:`DimensionEnum.WIDTH`, ``measure`` is the width; otherwise it is the height.
    """
    if measure <= 0 or ar <= 0:
      raise ValueError(f"Measurement and aspect ratio must be positive: m={measure}, ar={ar}.")
    (w, h) = (measure, measure / ar) if dim == DimensionEnum.WIDTH else (measure * ar, measure)
    return cls(width=w, height=h)
