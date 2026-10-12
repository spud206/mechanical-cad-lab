# Repository agent instructions

This repository is for mechanical engineering work expressed as reproducible, reviewable code and CAD artifacts.

## Core rules

- Treat dimensions, tolerances, materials, loads and manufacturing constraints as engineering requirements, not guesses.
- Never silently invent a critical dimension. Record unknowns explicitly in the project requirements or assumptions.
- Prefer fully parametric CadQuery models over hand-edited generated geometry.
- Imported/reference CAD is source input; generated STEP/STL/DXF/SVG files are build artifacts unless a project explicitly marks them as release artifacts.
- Keep units explicit. Repository default is millimetres for geometry and SI units elsewhere.
- Preserve a clean separation between source models, source/reference CAD, generated exports and engineering documentation.
- Every geometry-changing task must add or update deterministic checks for the dimensions/properties that matter.
- Validate geometry before claiming completion: model creation, shape validity, expected bounding box/volume where meaningful, and required exports.
- Do not commit, push, merge or deploy unless explicitly instructed. Leave the working tree ready for host-side review.
- Follow the project's branch-per-coherent-change workflow.

## Multi-agent roles

The coordinating Codex agent may delegate independent work to subagents. Prefer these roles:

1. **Mechanical requirements engineer** — extracts requirements, dimensions, interfaces, assumptions, tolerances, materials, loads and manufacturing constraints. Does not edit production geometry unless asked.
2. **CAD modeller** — implements parametric CadQuery geometry from approved requirements and interfaces.
3. **CAD/query engineer** — develops reusable Python geometry queries, selectors, measurement helpers, import/export helpers and automation.
4. **Verification reviewer** — independently checks geometry, dimensions, interfaces, collisions, invariants, tests and exports; should not simply restate the modeller's reasoning.
5. **Manufacturing/drawing reviewer** — checks manufacturability, drawing completeness, tolerances, fasteners, clearances and export suitability for the intended process.

Do not make several agents edit the same file in parallel. Use parallel agents mainly for independent analysis or review, then let the coordinator integrate changes.

## Project workflow

For a new object/project, create `projects/<slug>/` and keep:

- `requirements.md` — design intent, known dimensions, constraints, assumptions and acceptance criteria;
- `references/` — STEP/DXF/STL/3MF/PDF/image inputs from suppliers or measurements;
- `models/` — project-specific CadQuery source or thin entry points using reusable code from `src/mechcad`;
- `drawings/` — drawing source/configuration and generated drawing outputs when intentionally retained;
- `exports/` — generated manufacturing/interchange files; normally ignored except selected release artifacts;
- `notes/` — calculations, design decisions and review notes.

Before implementation, ensure requirements are sufficient. When information is missing, model only what is justified and document assumptions.

## Validation

Run the smallest relevant checks during iteration. Before a branch is considered complete, run:

```bash
make check
```

For geometry changes, also generate the relevant project exports and inspect them visually in OCP CAD Viewer.

## Container-only Codex permissions

In the devcontainer, start the CLI normally with `codex`. Its container-only default permissions are installed from `.devcontainer/codex-config.toml` (see `docs/workflows/codex-permissions.md`). Never copy these settings to host-wide Codex configuration. Do not alter Git history or touch other mounted host paths unless explicitly instructed.
