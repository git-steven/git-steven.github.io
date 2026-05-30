from __future__ import annotations
from dataclasses import dataclass
from .vector2d import Vector2D


@dataclass(frozen=True, slots=True)
class Curve:
    """
    Quadratic curve segment usable for mxGraph-style `quadTo` output.

    If `is_gap` is True, this segment represents empty spacing between
    visible rack/teeth segments.
    """

    start: Vector2D
    control: Vector2D
    end: Vector2D
    is_gap: bool = False

    def to_mx_quad(self) -> str:
        return f"Q {self.control.x:.3f} {self.control.y:.3f} {self.end.x:.3f} {self.end.y:.3f}"
