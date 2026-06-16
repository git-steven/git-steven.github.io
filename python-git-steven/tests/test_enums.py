from terracoil.geometry.enums import CardinalEnum, DimensionEnum, OrientationEnum, SpanEnum


class TestCardinal:
  def test_origin_distinct(self):
    assert CardinalEnum.ORIGIN != CardinalEnum.NORTH

  def test_north_west_composition(self):
    assert CardinalEnum.NORTH_WEST == CardinalEnum.NORTH | CardinalEnum.WEST

  def test_north_east_composition(self):
    assert CardinalEnum.NORTH_EAST == CardinalEnum.NORTH | CardinalEnum.EAST

  def test_south_west_composition(self):
    assert CardinalEnum.SOUTH_WEST == CardinalEnum.SOUTH | CardinalEnum.WEST

  def test_south_east_composition(self):
    assert CardinalEnum.SOUTH_EAST == CardinalEnum.SOUTH | CardinalEnum.EAST

  def test_short_aliases_match_long(self):
    assert CardinalEnum.NW == CardinalEnum.NORTH_WEST
    assert CardinalEnum.NE == CardinalEnum.NORTH_EAST
    assert CardinalEnum.SW == CardinalEnum.SOUTH_WEST
    assert CardinalEnum.SE == CardinalEnum.SOUTH_EAST


class TestOrientation:
  def test_horizontal_value(self):
    assert OrientationEnum.HORIZONTAL.value == "horizontal"

  def test_vertical_value(self):
    assert OrientationEnum.VERTICAL.value == "vertical"


class TestDimension:
  def test_width_value(self):
    assert DimensionEnum.WIDTH.value == "width"

  def test_height_value(self):
    assert DimensionEnum.HEIGHT.value == "height"

  def test_distinct(self):
    assert DimensionEnum.WIDTH != DimensionEnum.HEIGHT


class TestSpanEnum:
  def test_curve_value(self):
    assert SpanEnum.CURVE.value == "curve"

  def test_segment_value(self):
    assert SpanEnum.SEGMENT.value == "segment"

  def test_midpoint_value(self):
    assert SpanEnum.MIDPOINT.value == "midpoint"

  def test_all_distinct(self):
    assert len({SpanEnum.CURVE, SpanEnum.SEGMENT, SpanEnum.MIDPOINT}) == 3
