from pathlib import Path
import importlib.util

from mechcad.export import export_step, export_stl
from mechcad.validation import assert_valid

model_path = Path("projects/example_bracket/models/bracket.py")
spec = importlib.util.spec_from_file_location("example_bracket", model_path)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
shape = module.build()
assert_valid(shape)
export_step(shape, Path("projects/example_bracket/exports/bracket.step"))
export_stl(shape, Path("projects/example_bracket/exports/bracket.stl"))
print("Exported example bracket")
