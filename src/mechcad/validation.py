from __future__ import annotations

from dataclasses import dataclass

import cadquery as cq


@dataclass(frozen=True)
class BoundingBox:
    x: float
    y: float
    z: float


def bounding_box(shape: cq.Workplane | cq.Shape) -> BoundingBox:
    obj = shape.val() if isinstance(shape, cq.Workplane) else shape
    bb = obj.BoundingBox()
    return BoundingBox(bb.xlen, bb.ylen, bb.zlen)


def assert_valid(shape: cq.Workplane | cq.Shape) -> None:
    obj = shape.val() if isinstance(shape, cq.Workplane) else shape
    if not obj.isValid():
        raise AssertionError("CadQuery shape is not valid")
