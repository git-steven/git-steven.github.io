import pytest
from dataclasses import FrozenInstanceError

from terracoil.geometry import Size2D
from terracoil.geometry.enums import DimensionEnum


class TestSize2DConstruction:
  def test_basic(self):
    s = Size2D(width=10.0, height=4.0)
    assert s.width == 10.0
    assert s.height == 4.0

  def test_aspect_ratio(self):
    assert Size2D(width=10.0, height=5.0).aspect_ratio == 2.0

  def test_aspect_ratio_square(self):
    assert Size2D(width=4.0, height=4.0).aspect_ratio == 1.0

  def test_immutability(self):
    s = Size2D(width=10.0, height=4.0)
    with pytest.raises(FrozenInstanceError):
      s.width = 5.0  # type: ignore[misc]

  def test_equality_and_hash(self):
    a = Size2D(width=3.0, height=4.0)
    b = Size2D(width=3.0, height=4.0)
    assert a == b
    assert hash(a) == hash(b)


class TestSize2DValidation:
  def test_negative_width_rejected(self):
    with pytest.raises(ValueError, match="positive"):
      Size2D(width=-1.0, height=4.0)

  def test_negative_height_rejected(self):
    with pytest.raises(ValueError, match="positive"):
      Size2D(width=4.0, height=-1.0)

  def test_zero_width_rejected(self):
    with pytest.raises(ValueError):
      Size2D(width=0.0, height=4.0)

  def test_zero_height_rejected(self):
    with pytest.raises(ValueError):
      Size2D(width=4.0, height=0.0)


class TestSize2DInitWithAr:
  def test_dim_width(self):
    s = Size2D.init_with_ar(measure=10.0, ar=2.0, dim=DimensionEnum.WIDTH)
    assert s.width == 10.0
    assert s.height == 5.0
    assert s.aspect_ratio == 2.0

  def test_dim_height(self):
    s = Size2D.init_with_ar(measure=10.0, ar=2.0, dim=DimensionEnum.HEIGHT)
    assert s.width == 20.0
    assert s.height == 10.0
    assert s.aspect_ratio == 2.0

  def test_default_dim_is_width(self):
    s = Size2D.init_with_ar(measure=10.0, ar=2.0)
    assert s.width == 10.0
    assert s.height == 5.0

  def test_zero_measure_rejected(self):
    with pytest.raises(ValueError):
      Size2D.init_with_ar(measure=0.0, ar=2.0)

  def test_negative_ar_rejected(self):
    with pytest.raises(ValueError):
      Size2D.init_with_ar(measure=10.0, ar=-1.0)

  def test_zero_ar_rejected(self):
    with pytest.raises(ValueError):
      Size2D.init_with_ar(measure=10.0, ar=0.0)
