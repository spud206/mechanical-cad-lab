# Quickstart — eigen CAD-repository vanaf de mechanical-cad-lab-template (macOS)

Deze handleiding is bedoeld voor een **mechanical engineer met een nieuwe Mac**. `spud206/mechanical-cad-lab` is uitsluitend de gedeelde *basis/template*. Elke engineer maakt een **eigen GitHub-repository** voor CAD-projecten, met eigen Git-geschiedenis, branches, modellen en exports. Werk en push nooit rechtstreeks naar de template, tenzij je de template zelf onderhoudt.

## 1. Accounts en hostsoftware

Benodigd: een GitHub-account (met toegang tot de template als die privé is), een ChatGPT-account met Codex-toegang, adminrechten op macOS en voldoende schijfruimte voor Docker en CAD-dependencies.

1. Installeer [Visual Studio Code](https://code.visualstudio.com/download) en de Microsoft-extensie **Dev Containers** (`ms-vscode-remote.remote-containers`).
2. Installeer [Docker Desktop voor macOS](https://docs.docker.com/desktop/setup/install/mac-install/) voor Apple Silicon of Intel en start Docker Desktop.
3. Controleer op de Mac in Terminal `git --version`; installeer zo nodig Apple Command Line Tools met `xcode-select --install`.
4. Installeer [Homebrew](https://brew.sh/) als het ontbreekt; voer vervolgens uit:

```bash
brew install git-lfs
git lfs install
git lfs version
```

5. Optioneel: installeer GitHub CLI met `brew install gh` en voer `gh auth login` uit. GitHub-toegang via HTTPS en browser kan ook.

**Niet op macOS installeren:** Python, CadQuery, Conda of Codex CLI. Die draaien in de devcontainer.

## 2. Maak je eigen repository vanuit de template

**Voorkeur: GitHub Template Repository**

1. Open https://github.com/spud206/mechanical-cad-lab.
2. Kies **Use this template → Create a new repository**. De eigenaar moet de bronrepository hiervoor eerst als template instellen via **Settings → General → Template repository**.
3. Kies je eigen GitHub-account of organisatie, een projectspecifieke naam zoals `sensor-enclosure-cad`, en de gewenste zichtbaarheid. Gebruik normaal alleen de standaardbranch.
4. Open de aangemaakte repository. Je repository moet de mappen `.devcontainer/`, `docs/`, `projects/` en `AGENTS.md` bevatten. Je repo heeft een eigen geschiedenis en `origin`.

**Fallback als de templateknop nog niet beschikbaar is**

Maak op GitHub een **lege** repository zonder README/.gitignore/licentie en voer op macOS uit (pas beide placeholders aan):

```bash
mkdir -p ~/Development
cd ~/Development
git clone https://github.com/EIGEN_ACCOUNT/EIGEN_CAD_PROJECT.git
cd EIGEN_CAD_PROJECT
TEMP_DIR="$(mktemp -d)"
git clone https://github.com/spud206/mechanical-cad-lab.git "$TEMP_DIR/source"
git -C "$TEMP_DIR/source" lfs pull
rsync -a --exclude='.git/' "$TEMP_DIR/source/" ./
rm -rf "$TEMP_DIR"
git remote -v
git add .
git diff --cached --stat
git commit -m "chore: bootstrap CAD project from template"
git push -u origin main
```

Kopieer **nooit** de `.git`-map van de bronrepo. Je `origin` moet naar de **eigen** GitHub-repository verwijzen.

## 3. Clone jouw project en open de devcontainer

Als je GitHub's **Use this template** hebt gebruikt, clone dan je nieuwe repo op de Mac:

```bash
mkdir -p ~/Development
cd ~/Development
git clone https://github.com/EIGEN_ACCOUNT/EIGEN_CAD_PROJECT.git
cd EIGEN_CAD_PROJECT
git lfs install
git remote -v
git status --short --branch
```

Open deze **eigen repo** in VS Code met **File → Open Folder** (of `code .`, indien beschikbaar). Zorg dat Docker Desktop actief is en kies **Cmd+Shift+P → Dev Containers: Reopen in Container**.

De eerste build downloadt de CAD-toolchain en kan veel ruimte gebruiken. Open daarna een VS Code-terminal **in de container** en controleer:

```bash
pwd
whoami
date
git remote -v
git status --short --branch
python -c 'import cadquery; print(cadquery.__version__)'
codex --version
```

De repository op macOS is gemount als de container-workspace; er wordt **geen tweede Git-clone** in de container gemaakt. De locale en tijdzone worden door de devcontainer ingesteld.

## 4. Codex via normale browser-OAuth in Safari

Start **binnen de container**:

```bash
codex login
```

Open de getoonde link in Safari op de Mac en log in met ChatGPT. De OAuth-callback naar `localhost:1455` (eventueel fallback `1457`) moet via het **Ports**-paneel in VS Code naar **dezelfde poort** in de devcontainer worden doorgestuurd. Controleer poortconflicten als de callback faalt. Gebruik voor deze workflow **geen device-code-login**.

Controleer na aanmelden:

```bash
codex login status
codex
```

Codex gebruikt een **containerlokale configuratie** en een persistent Docker-volume voor zijn login. De containerconfiguratie heeft brede uitvoeringsrechten en is bedoeld om herhaalde toestemmingvragen en nested bubblewrap-problemen te vermijden. Lees `docs/workflows/codex-permissions.md`, inspecteer mounts en plaats geen onnodige secrets in de container. `AGENTS.md` verbiedt commit/push zonder expliciete opdracht als **workflowregel**, niet als technische Git-blokkade.

## 5. Controleer de CAD-toolchain

In de container:

```bash
make check
make export-example
```

Inspecteer het gegenereerde object met de **OCP CAD Viewer** in VS Code of de standalone viewer (`make viewer`, poort 3939). JupyterLab kan via `make jupyter` (poort 8888). Controleer oriëntatie en geometrie visueel, naast tests.

## 6. Start je eigen mechanical engineering-project

1. Lees `AGENTS.md`, `docs/workflows/new-object.md` en de Codex-agentrollen in `.codex/roles/`.
2. Maak een projectspecifieke map `projects/<objectnaam>/`; leg **afmetingen, toleranties, materiaal, productieproces en aannames** vast in `requirements.md`.
3. Plaats leveranciersmodellen (bijv. STEP) in `references/`; maak parametrische CadQuery-Pythonbronnen in `models/` en relevante geometrische tests.
4. Genereer STEP/STL/DXF vanuit de code. Commit alleen relevante, expliciet bedoelde bronbestanden of vrijgegeven CAD-artifacts; automatisch gegenereerde exports zijn doorgaans build-output.
5. Laat Codex implementeren en testen binnen de container. Controleer relevante pasmaten en productieaspecten voordat je een ontwerp vrijgeeft.

## 7. Dagelijkse Git-workflow

Maak voor een nieuwe wijziging op de **Mac-host** een gerichte branch:

```bash
git switch -c feature/first-enclosure
```

Werk met Codex in de devcontainer, voer tests uit en controleer de CAD-geometrie. Daarna **op de host**:

```bash
git status
git diff --check
git add <specifieke-bestanden>
git diff --cached --stat
git commit -m "feat: add parametric enclosure"
git push -u origin feature/first-enclosure
```

Open een Pull Request naar de standaardbranch van **je eigen repository**. Template-updates komen niet automatisch in reeds gemaakte repositories terecht.

## Problemen oplossen

- `git lfs` is onbekend: voer op de Mac `brew install git-lfs && git lfs install` uit.
- Docker of devcontainer start niet: controleer Docker Desktop, beschikbare schijfruimte en de Dev Containers-extensie; bekijk de buildlogs.
- Browser-OAuth rondt niet af: controleer of VS Code de containerpoort 1455 (eventueel 1457) forwardt naar dezelfde lokale poort, en dat geen ander proces de poort bezet.
- `origin` verwijst naar de template: stop vóór push en corrigeer de remote naar je eigen repo.
- CadQuery import faalt: controleer devcontainer-build en actieve Conda-omgeving voordat je dependencies verandert.
- Viewer toont niets: controleer of het model is gegenereerd en of de VS Code-viewer/poortforwarding actief is.

Deze handleiding hoort bij de **gedeelde template**. Projectspecificaties en engineeringresultaten horen in de **eigen projectrepository** van de engineer.
