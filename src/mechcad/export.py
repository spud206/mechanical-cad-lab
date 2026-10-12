from __future__ import annotations

from pathlib import Path

import cadquery as cq


def export_step(shape: cq.Workplane | cq.Shape, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(shape, str(path), exportType="STEP")
    return path


def export_stl(shape: cq.Workplane | cq.Shape, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(shape, str(path), exportType="STL")
    return path
