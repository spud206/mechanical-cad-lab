# Mechanical CAD Lab — reusable engineering template

A code-first mechanical engineering **template repository** for CadQuery, supplier/reference CAD files, drawings, tests, exports and Codex-assisted engineering in a VS Code devcontainer.

## For new engineers: create your own project repository

**Do not develop your personal CAD project directly in this repository.** Create your own repository using **Use this template → Create a new repository**, then clone **your own** repository onto the Mac and open it in VS Code Dev Containers.

Read the [full macOS quickstart](docs/QUICKSTART-macOS.md), covering VS Code, Docker Desktop, Git LFS, repo creation, browser-based Codex OAuth (forwarded localhost port 1455), a first CAD object and host-side Git workflow.

This template is the source for project bootstrapping; it does **not** automatically synchronize changes to already created project repositories.

## Repository structure and tooling

- `.devcontainer/`: Ubuntu 24.04, Python 3.12/Conda, CadQuery/OCP, viewer, Jupyter, Codex CLI and developer tooling
- `.codex/roles/` and `AGENTS.md`: agent roles and engineering/review contracts
- `projects/`: separate objects, requirements, reference CAD, Python models, drawings and generated exports
- `src/mechcad/`: shared engineering helpers
- `tests/`: deterministic geometry and software checks
- `docs/workflows/`: modeling and security guidance

In your **own devcontainer**:

```bash
python -c 'import cadquery; print(cadquery.__version__)'
codex --version
make check
make export-example
```

Use the OCP CAD Viewer VS Code extension, or `make viewer` (port 3939). `make jupyter` opens JupyterLab (port 8888).

## Codex and Git boundaries

Codex is launched with `codex` in the devcontainer. Normal browser-based `codex login` uses a forwarded localhost OAuth callback, and container-local Codex settings avoid recurring approval prompts/nested bubblewrap. Review [permissions and security](docs/workflows/codex-permissions.md): broad in-container permissions are intentional and must be bounded by mounts and Docker isolation.

The **host Mac** owns the project's Git working tree. Codex edits/tests in the devcontainer, while final review, commit and push normally take place on the host; see `AGENTS.md`. Do not clone the repository a second time inside the container.
