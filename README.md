# Mechanical CAD Lab

A reproducible code-first mechanical engineering repository for CadQuery models, supplier/reference CAD, engineering notes, generated drawings/exports and Codex-assisted workflows.

## New developer onboarding

See [Quickstart for a clean macOS laptop](docs/QUICKSTART-macOS.md), including GitHub, VS Code, Docker Desktop, Dev Containers and normal browser-based ChatGPT OAuth login via forwarded localhost callback (1455/1457).

## Start

1. Clone/create the repository on the **host Mac**.
2. Open the host repository folder in VS Code.
3. Choose **Dev Containers: Reopen in Container**.
4. The host working tree (including `.git`) is mounted as the devcontainer workspace; do not make a second clone inside the container.
5. Check:

```bash
python -c 'import cadquery; print(cadquery.__version__)'
codex --version
make check
make export-example
```

For visualization, use the OCP CAD Viewer VS Code extension or run `make viewer` and forward port 3939. JupyterLab is available with `make jupyter` on port 8888.

## Environment

- Ubuntu 24.04 devcontainer
- Python 3.12 in a Miniforge/conda environment
- CadQuery / OpenCascade stack
- OCP CAD Viewer + standalone viewer
- JupyterLab
- pytest, Ruff, mypy
- NumPy/SciPy/trimesh/meshio and common engineering helpers
- Git, Git LFS, GitHub CLI
- Codex CLI
- timezone `Europe/Amsterdam`; UTF-8 locales installed

See `AGENTS.md` and `docs/workflows/new-object.md` before starting engineering work.

## Codex permissions and bubblewrap

In the **devcontainer terminal**, start Codex simply with `codex`. This enables no-approval, unrestricted execution **within the Docker container** and avoids relying on nested bubblewrap. Read [the security trade-offs](docs/workflows/codex-permissions.md) before use. The VS Code Codex extension has separate permissions controls.

