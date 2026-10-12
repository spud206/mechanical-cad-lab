from __future__ import annotations

from dataclasses import dataclass

import cadquery as cq


@dataclass(frozen=True)
class BoundingBox:
    x: float
    y: float
    z: float


def _as_shape(value: cq.Workplane | cq.Shape) -> cq.Shape:
    obj = value.val() if isinstance(value, cq.Workplane) else value
    if not isinstance(obj, cq.Shape):
        raise TypeError("Expected a CadQuery shape")
    return obj


def bounding_box(shape: cq.Workplane | cq.Shape) -> BoundingBox:
    bb = _as_shape(shape).BoundingBox()
    return BoundingBox(bb.xlen, bb.ylen, bb.zlen)


def assert_valid(shape: cq.Workplane | cq.Shape) -> None:
    if not _as_shape(shape).isValid():
        raise AssertionError("CadQuery shape is not valid")
