import re

import pytest
from dataclasses import FrozenInstanceError

from terracoil.geometry import Curve, Vector2D


class TestCurveConstruction:
  def test_basic(self):
    c = Curve(start=Vector2D(0.0, 0.0), control=Vector2D(1.0, 1.0), end=Vector2D(2.0, 0.0))
    assert c.start == Vector2D(0.0, 0.0)
    assert c.control == Vector2D(1.0, 1.0)
    assert c.end == Vector2D(2.0, 0.0)

  def test_is_gap_default_false(self):
    c = Curve(start=Vector2D(0.0, 0.0), control=Vector2D(0.0, 0.0), end=Vector2D(0.0, 0.0))
    assert c.is_gap is False

  def test_is_gap_explicit_true(self):
    c = Curve(
      start=Vector2D(0.0, 0.0),
      control=Vector2D(0.0, 0.0),
      end=Vector2D(0.0, 0.0),
      is_gap=True,
    )
    assert c.is_gap is True

  def test_immutability(self):
    c = Curve(start=Vector2D(0.0, 0.0), control=Vector2D(1.0, 1.0), end=Vector2D(2.0, 0.0))
    with pytest.raises(FrozenInstanceError):
      c.start = Vector2D(9.0, 9.0)  # type: ignore[misc]

  def test_equality_and_hash(self):
    a = Curve(start=Vector2D(0.0, 0.0), control=Vector2D(1.0, 1.0), end=Vector2D(2.0, 0.0))
    b = Curve(start=Vector2D(0.0, 0.0), control=Vector2D(1.0, 1.0), end=Vector2D(2.0, 0.0))
    assert a == b
    assert hash(a) == hash(b)


class TestCurveToMxQuad:
  def test_format(self):
    c = Curve(
      start=Vector2D(0.0, 0.0),
      control=Vector2D(1.234567, 2.345678),
      end=Vector2D(3.456789, 4.567890),
    )
    assert re.fullmatch(r"Q 1\.235 2\.346 3\.457 4\.568", c.to_mx_quad())

  def test_three_decimals(self):
    c = Curve(
      start=Vector2D(0.0, 0.0),
      control=Vector2D(1.0, 2.0),
      end=Vector2D(3.0, 4.0),
    )
    assert c.to_mx_quad() == "Q 1.000 2.000 3.000 4.000"
