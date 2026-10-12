#!/usr/bin/env bash
set -euo pipefail

# Only configure the isolated Codex home inside this devcontainer.
if [[ "${MECHCAD_DEVCONTAINER:-}" != "1" || ! -f /.dockerenv ]]; then
  echo "Not inside the mechanical CAD devcontainer" >&2
  exit 1
fi
mkdir -p "$HOME/.codex"
if [[ ! -w "$HOME/.codex" ]]; then
  echo "Codex home is not writable: $HOME/.codex; check Docker volume ownership" >&2
  exit 1
fi
cp .devcontainer/codex-config.toml "$HOME/.codex/config.toml"
chmod 600 "$HOME/.codex/config.toml"

git config --global --add safe.directory "${PWD}"
git lfs install --skip-repo >/dev/null 2>&1 || true

python - <<'PY'
import cadquery as cq
shape = cq.Workplane("XY").box(1, 2, 3)
assert shape.val().Volume() > 0
print("CadQuery smoke test OK")
PY

codex --version || true
python --version
locale
