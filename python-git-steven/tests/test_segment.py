import pytest
from dataclasses import FrozenInstanceError

from terracoil.geometry import Segment, Vector2D


class TestSegment:
  def test_construction(self):
    s = Segment(start=Vector2D(0.0, 0.0), stop=Vector2D(3.0, 4.0))
    assert s.start == Vector2D(0.0, 0.0)
    assert s.stop == Vector2D(3.0, 4.0)

  def test_length(self):
    s = Segment(start=Vector2D(0.0, 0.0), stop=Vector2D(3.0, 4.0))
    assert s.length() == 5.0

  def test_length_zero_when_collapsed(self):
    s = Segment(start=Vector2D(1.0, 2.0), stop=Vector2D(1.0, 2.0))
    assert s.length() == 0.0

  def test_immutability(self):
    s = Segment(start=Vector2D(0.0, 0.0), stop=Vector2D(3.0, 4.0))
    with pytest.raises(FrozenInstanceError):
      s.start = Vector2D(9.0, 9.0)  # type: ignore[misc]

  def test_equality_and_hash(self):
    a = Segment(start=Vector2D(0.0, 0.0), stop=Vector2D(3.0, 4.0))
    b = Segment(start=Vector2D(0.0, 0.0), stop=Vector2D(3.0, 4.0))
    assert a == b
    assert hash(a) == hash(b)

  def test_inequality_when_endpoints_swap(self):
    a = Segment(start=Vector2D(0.0, 0.0), stop=Vector2D(3.0, 4.0))
    b = Segment(start=Vector2D(3.0, 4.0), stop=Vector2D(0.0, 0.0))
    assert a != b
