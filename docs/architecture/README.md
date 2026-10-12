# Architecture

The repository uses code-first parametric CAD.

- `src/mechcad/`: reusable CAD/query/validation/export helpers.
- `projects/`: object-specific engineering requirements, references and model entry points.
- `AGENTS.md`: authoritative instructions for Codex and its subagents.
- `.codex/roles/`: lightweight role playbooks, not a separate orchestration runtime.
- `.devcontainer/`: reproducible Linux development environment containing CadQuery and Codex.

The host owns the Git working tree. VS Code opens that host folder in the devcontainer, so `.git` is the same repository inside and outside the container. Implementation/testing happens in the container; final review, commit and push normally happen on the host.
