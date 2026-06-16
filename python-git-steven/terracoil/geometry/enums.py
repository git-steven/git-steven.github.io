from __future__ import annotations
from enum import auto, IntFlag, StrEnum

class CardinalEnum(IntFlag):
  ORIGIN = auto()
  NORTH = auto()
  SOUTH = auto()
  WEST = auto()
  EAST = auto()

  NW = NORTH_WEST = NORTH | WEST
  NE = NORTH_EAST = NORTH | EAST
  SW = SOUTH_WEST = SOUTH | WEST
  SE = SOUTH_EAST = SOUTH | EAST

class OrientationEnum(StrEnum):
  HORIZONTAL = auto()
  VERTICAL = auto()


class DimensionEnum(StrEnum):
  HEIGHT = auto()
  WIDTH = auto()
  #DEPTH = auto()

class SpanEnum(StrEnum):
  CURVE = auto()
  SEGMENT = auto()
  MIDPOINT = auto()
