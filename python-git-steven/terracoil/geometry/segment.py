from __future__ import annotations

from dataclasses import dataclass
from math import sqrt, atan2, cos, sin, isclose

from terracoil.util import AngleUtil, MathConstants, RealNumber
from .vector2d import Vector2D

@dataclass(frozen=True)
class Segment:
  """
  A segment, consisting of 2 Vectors
  """
  start: Vector2D
  stop: Vector2D

  def length(self) -> float:
    return self.start.distance_to(self.stop)
