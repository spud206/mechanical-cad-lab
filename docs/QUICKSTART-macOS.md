# Quickstart: nieuwe macOS-ontwikkellaptop

Deze handleiding gaat uit van een lege Mac (Apple Silicon of Intel), een bestaande GitHub-repository `mechanical-cad-lab` en een werkende internetverbinding. Alle Python-, CAD- en Codex-tools draaien **in de devcontainer**. Op de Mac staan alleen de ontwikkelapplicaties en Git.

## 1. Accounts

- Een GitHub-account met toegang tot de repository.
- Een ChatGPT-account met toegang tot Codex CLI.
- Adminrechten op de Mac voor het installeren van software.

## 2. Installeer de host-applicaties

1. Installeer **Visual Studio Code** vanaf https://code.visualstudio.com/download en verplaats de applicatie naar **Programma's**.
2. Installeer **Docker Desktop for Mac** (kies Apple Silicon of Intel) vanaf https://docs.docker.com/desktop/setup/install/mac-install/. Start Docker Desktop en voltooi de eerste configuratie.
3. Installeer **Git** indien nog niet aanwezig. Open Terminal en voer `git --version` uit. macOS kan aanbieden Xcode Command Line Tools te installeren; accepteer dat. Controleer daarna opnieuw met `git --version`.
4. Installeer **Git LFS** op de host via https://git-lfs.com/ of via Homebrew als die al aanwezig is: `brew install git-lfs`. Daarna: `git lfs install`. Git LFS is nodig voor CAD-referentiebestanden die door LFS beheerd worden.
5. Controleer in Terminal `docker version` en `git --version`. Docker Desktop moet actief zijn.

**Niet installeren op de host:** Python, conda/mamba, CadQuery, OpenCascade/OCP, Node.js of Codex CLI. Die zitten in de devcontainer.

## 3. Meld je aan bij GitHub en clone op de host

1. Open Terminal **op de Mac** (niet in een container).
2. Configureer Git-identiteit (vervang de voorbeeldwaarden):

   ```bash
   git config --global user.name "Voornaam Achternaam"
   git config --global user.email "jij@example.com"
   git config --global init.defaultBranch main
   git lfs install
   ```

3. Maak een ontwikkelmap en clone de bestaande repo op de **host**:

   ```bash
   mkdir -p ~/Development
   cd ~/Development
   git clone https://github.com/spud206/mechanical-cad-lab.git
   cd mechanical-cad-lab
   git lfs pull
   ```

   Vervang `ORGANISATIE` en de repositorynaam door de daadwerkelijke GitHub-URL. Meld je aan via je GitHub-credential manager/browser wanneer Git hierom vraagt. GitHub accepteert geen gewoon accountwachtwoord voor HTTPS Git-operaties.

## 4. Configureer VS Code

1. Open VS Code en ga naar **Extensions** (`Cmd+Shift+X`).
2. Installeer **Dev Containers** van Microsoft (`ms-vscode-remote.remote-containers`).
3. Open de Command Palette (`Cmd+Shift+P`), typ **Shell Command: Install 'code' command in PATH** en voer dit uit als die opdracht beschikbaar is. Dit is optioneel; VS Code kan de repo ook via **File > Open Folder** openen.
4. De repositoryconfiguratie installeert de extra Python-, Jupyter-, Ruff- en CAD-viewerextensies automatisch in de container.



4. Controleer dat `.git` op de host aanwezig is: `git status -sb`. Gebruik **niet** de VS Code-optie 'Clone Repository in Container Volume'; we willen één working tree op de Mac.

## 5. Start de devcontainer

1. Open op de Mac de hostmap `~/Development/mechanical-cad-lab` in VS Code (`code .` vanuit die map of File > Open Folder).
2. `Cmd+Shift+P` → **Dev Containers: Reopen in Container**.
3. VS Code bouwt de Docker-image en installeert de ontwikkeltools. Eerste build kan afhankelijk van netwerk en hardware langer duren.
4. Open **Terminal > New Terminal**. Deze terminal hoort nu in Linux te draaien. Controleer:

   ```bash
   pwd
   echo "$MECHCAD_DEVCONTAINER"
   python --version
   python -c 'import cadquery; print(cadquery.__version__)'
   codex --version
   git status -sb
   locale
   date +'%Z %z'
   ```

   Verwacht: workspace onder `/workspaces/`, marker `1`, Python/CadQuery/Codex beschikbaar, timezone Europe/Amsterdam en dezelfde Git branch als de host.

## 6. Codex aanmelden met normale browser-OAuth op de Mac

Codex draait in de **devcontainer**, terwijl Safari op **macOS** draait. De normale browserlogin gebruikt `http://localhost:1455/auth/callback` (eventueel fallbackpoort `1457`). VS Code moet die lokale callback doorsturen naar Codex in de container. Daarom staan beide poorten in `.devcontainer/devcontainer.json` onder `forwardPorts`, met `requireLocalPort` aan. Publiceer de callback niet op het LAN/internet.

1. Open de repository via **Dev Containers: Reopen in Container**. Open daarna in VS Code **Ports** (Terminal-paneel → Ports). Controleer dat poort **1455** doorgestuurd is naar lokale poort **1455** op de Mac. Controleer ook poort **1457** als fallback. Als de poort nog niet actief is: kies **Forward a Port**, voer `1455` in, en verifieer dat de lokale poort gelijk blijft. VS Code kan dit pas beschikbaar maken wanneer een proces daadwerkelijk luistert.
2. Zorg dat geen andere lokale Codex-app, ander devcontainer-loginproces of service poort 1455 op je Mac bezet houdt. Als VS Code de poort stilzwijgend naar 1456 hernummerd heeft, werkt de OAuth-redirect niet; beëindig het conflicterende proces en stel forwarding op **1455 → 1455** in.
3. Voer in de **devcontainerterminal** uit:

   ```bash
   codex login
   ```

4. Open de getoonde ChatGPT/OpenAI-aanmeldlink in **Safari op de Mac**. Rond het inloggen af. De browser stuurt de callback naar `localhost:1455`; VS Code routeert deze naar de actieve Codex-loginserver in de container.
5. Controleer in de **devcontainerterminal**:

   ```bash
   codex login status
   codex
   ```

**Geen device-code-login**: gebruik niet `--device-auth`. Kopieer geen OAuth-tokens of `auth.json` tussen host en container. De container gebruikt een eigen persistent Docker-volume voor `/home/vscode/.codex`, waardoor de login doorgaans behouden blijft na rebuilds zolang het volume bestaat. De host-`~/.codex` is niet gemount.

**Als de browser meldt dat localhost niet bereikbaar is:** laat `codex login` draaien; controleer de VS Code Ports-weergave (geen willekeurige andere lokale poort), of de loginserver actief is en of je niet per ongeluk host-Codex gestart hebt. Eventueel in een tweede containerterminal: `ss -lnt | grep -E ':1455|:1457'`. Begin een nieuwe login als de eerdere poging verlopen is. De callback-URL kan tijdelijke tokens bevatten: deel die URL niet en plak hem niet in logs of tickets.

## 7. Toestemmingen, bubblewrap en beveiliging

De repositoryconfiguratie installeert containerlokaal `~/.codex/config.toml` met:

```toml
approval_policy = "never"
sandbox_mode = "danger-full-access"
```

Dit is een **bewuste uitzondering binnen deze specifieke devcontainer**: Codex vraagt niet telkens goedkeuring en hoeft niet op een geneste bubblewrap-sandbox te vertrouwen. Codex kan echter alle bestanden benaderen waartoe de Linux-container toegang heeft, inclusief de gemounte repository en zijn eigen authenticatiegegevens. Er wordt geen Docker-socket, `--privileged` of brede host-home-mount gebruikt.

`AGENTS.md` spreekt af dat Codex niet zelf commit/push doet zonder expliciete instructie, maar dat is een **werkafspraak**, geen technische blokkade. Controleer de mounts voordat je onbetrouwbare code draait; laat geen secrets in de repository staan.

## 8. Eerste checks en CAD-weergave

In de devcontainer:

```bash
make check
make export-example
```

Open OCP CAD Viewer in VS Code of gebruik de apart geconfigureerde viewer op poort 3939. Voor Jupyter is poort 8888 beschikbaar. Voer CAD-modellen en tests in de container uit; controleer afmetingen en visuele geometrie vóór vrijgave.

## 9. Dagelijkse Git-werkwijze

1. Maak op de **Mac** een nieuwe branch (`git switch -c feature/naam`).
2. Open/reopen de repo in Dev Containers; gebruik in de container gewoon `codex`.
3. Codex past Python/CAD/tests/documentatie aan en valideert, **zonder automatisch te committen**.
4. Controleer CAD-exports en visuele geometrie.
5. Review wijzigingen en `git status` op de Mac; commit/push vanaf de **host**.
6. Open een Pull Request in GitHub, laat checks draaien en merge via GitHub.

## 10. Veelvoorkomende problemen

- **Docker draait niet:** start Docker Desktop en controleer `docker version`.
- **Container build faalt:** kies in Command Palette **Dev Containers: Rebuild Container** en bekijk **Dev Containers: Show Container Log**.
- **OAuth-callback bereikt de container niet:** controleer of VS Code poort 1455 (of fallback 1457) lokaal exact naar dezelfde poort in de devcontainer forwardt, zonder poortconflict op de Mac. Start zo nodig `codex login` opnieuw.
- **Toestemmingsvragen/bubblewrap:** verifieer `cat ~/.codex/config.toml` en `echo "$MECHCAD_DEVCONTAINER"`; gebruik de CLI **in** de container, niet een host-Codex of afzonderlijke IDE-extensieconfiguratie.
- **Vreemde Git branch:** controleer `pwd`, `git rev-parse --show-toplevel` en of de hostmap in VS Code geopend is.
- **Geen GitHub-toegang:** meld je aan op de host; wijzig geen permissies van de gehele host of mount geen volledige SSH-home in de container.
- **CAD-viewer toont niets:** controleer of de extensie binnen de container is geïnstalleerd en of de viewer start; de geometrie-export werkt ook zonder GUI.

## Officiële bronnen

- VS Code Dev Containers: https://code.visualstudio.com/docs/devcontainers/tutorial
- Docker Desktop voor Mac: https://docs.docker.com/desktop/setup/install/mac-install/
- Codex-authenticatie: https://developers.openai.com/codex/auth
- GitHub clone: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
