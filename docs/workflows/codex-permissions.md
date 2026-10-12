# Codex permissions inside the devcontainer

Start Codex **normally** from the VS Code devcontainer terminal using `codex`. Container-local settings in `/home/vscode/.codex/config.toml` are installed by `.devcontainer/post-create.sh` from `.devcontainer/codex-config.toml`:

```toml
approval_policy = "never"
sandbox_mode = "danger-full-access"
```

This avoids approval prompts and the nested Linux bubblewrap sandbox. Codex still follows `AGENTS.md`: **do not commit or push unless specifically requested**. Those are instructions, not enforced Git permissions.

The container uses a **named Docker volume** (`mechanical-cad-lab-codex-home`) for its Codex home. It does not mount the host's `~/.codex`, so the host configuration is not changed or inherited. On first use, run `codex login` inside the container and finish standard OAuth in the host browser. VS Code must forward localhost port 1455 (fallback 1457) to the same port in the container; see `docs/QUICKSTART-macOS.md`. Authentication persists across container rebuilds via the volume. Do not put credentials into the repository or Docker image.

The macOS checkout is bind-mounted as the workspace by Dev Containers, so edits to that checkout are visible on the host. Because `danger-full-access` disables Codex's second sandbox, the container's mounts and network permissions define the real boundary. Never mount the host home, SSH keys or Docker socket. Do not use Docker privileged mode to work around bubblewrap.

Verify:

```bash
echo "$MECHCAD_DEVCONTAINER"
cat "$HOME/.codex/config.toml"
codex --version
mount | grep '/home/vscode/.codex' || true
```

The intended result is a normal `codex` command with container-local permissions. If the IDE extension is used, verify its runtime is the *remote container* rather than the macOS extension host; its approval policy and managed restrictions may differ.
