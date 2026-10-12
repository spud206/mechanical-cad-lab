from __future__ import annotations

from dataclasses import dataclass

import cadquery as cq


@dataclass(frozen=True)
class BracketParams:
    width: float = 40.0
    depth: float = 30.0
    thickness: float = 4.0
    height: float = 28.0
    hole_diameter: float = 5.5


def build(params: BracketParams = BracketParams()) -> cq.Workplane:
    base = cq.Workplane("XY").box(params.width, params.depth, params.thickness)
    upright = (
        cq.Workplane("XZ")
        .workplane(offset=-params.depth / 2 + params.thickness / 2)
        .box(params.width, params.height, params.thickness)
    )
    result = base.union(upright)
    result = (
        result.faces(">Z")
        .workplane()
        .pushPoints([(-params.width / 4, 0), (params.width / 4, 0)])
        .hole(params.hole_diameter)
    )
    return result
