# New object workflow

1. Create a focused Git branch on the host.
2. Create `projects/<slug>/requirements.md` and add source/reference CAD under `references/`.
3. Ask Codex to have a requirements role extract interfaces, unknowns and acceptance criteria.
4. Implement the model with the CAD modeller role.
5. Add reusable geometry/query functionality under `src/mechcad/` only when it is genuinely reusable.
6. Add deterministic geometry tests.
7. Generate STEP/STL/DXF/other required exports.
8. Inspect visually in OCP CAD Viewer.
9. Run an independent verification/manufacturing review when the part matters mechanically.
10. Run `make check`, then review/commit/push on the host.
