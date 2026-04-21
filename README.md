<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">

# FUGS&KI — Fuehrungsunterstuetzungssystem & KI

<em>Effizientere Notfallreaktion durch intelligente Automatisierung</em>

<!-- BADGES -->
<img src="https://img.shields.io/github/license/MKFeuer/2026-09-fugs-ki?style=flat&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
<img src="https://img.shields.io/github/last-commit/MKFeuer/2026-09-fugs-ki?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/MKFeuer/2026-09-fugs-ki?style=flat&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/MKFeuer/2026-09-fugs-ki?style=flat&color=0080ff" alt="repo-language-count">

<em>Erstellt mit folgenden Werkzeugen und Technologien:</em>

<img src="https://img.shields.io/badge/JSON-000000.svg?style=flat&logo=JSON&logoColor=white" alt="JSON">
<img src="https://img.shields.io/badge/Markdown-000000.svg?style=flat&logo=Markdown&logoColor=white" alt="Markdown">
<img src="https://img.shields.io/badge/npm-CB3837.svg?style=flat&logo=npm&logoColor=white" alt="npm">
<img src="https://img.shields.io/badge/TOML-9C4121.svg?style=flat&logo=TOML&logoColor=white" alt="TOML">
<img src="https://img.shields.io/badge/Leaflet-199900.svg?style=flat&logo=Leaflet&logoColor=white" alt="Leaflet">
<img src="https://img.shields.io/badge/Vue.js-4FC08D.svg?style=flat&logo=vuedotjs&logoColor=white" alt="Vue.js">
<img src="https://img.shields.io/badge/React-61DAFB.svg?style=flat&logo=React&logoColor=black" alt="React">
<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white" alt="Docker">
<br>
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/TypeScript-3178C6.svg?style=flat&logo=TypeScript&logoColor=white" alt="TypeScript">
<img src="https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=flat&logo=GitHub-Actions&logoColor=white" alt="GitHub%20Actions">
<img src="https://img.shields.io/badge/Zod-3E67B1.svg?style=flat&logo=Zod&logoColor=white" alt="Zod">
<img src="https://img.shields.io/badge/Vite-646CFF.svg?style=flat&logo=Vite&logoColor=white" alt="Vite">
<img src="https://img.shields.io/badge/bat-31369E.svg?style=flat&logo=bat&logoColor=white" alt="bat">
<img src="https://img.shields.io/badge/uv-DE5FE9.svg?style=flat&logo=uv&logoColor=white" alt="uv">

</div>
<br>

---

Ein KI-gestuetzter Stabsfuehrungsassistenttechnoligedemonstrator fuer den Feuerwehr-Einsatz. Entstanden beim **[Hackathon2026 der Feuerwehr Muenchen](https://www.ffw-muenchen.de/hackathon2026/)**.

FUGS&KI verbindet eine Chat-Oberflaeche mit einem grossen Sprachmodell (LLM) und gibt diesem ueber das [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) Zugriff auf Einsatzdaten, Geodaten, Wetterdaten und Nachrichtenfunktionen — so wird die KI zum Werkzeug fuer die Stabsarbeit.

## Features

- **Chat-Interface** — Streaming-Chat mit waehlbarem LLM (lokal oder remote, OpenAI-kompatibel) und Kartenansicht
- **Einsatzdaten** — Zugriff auf Einsaetze, Einsatzmittel und Alarmstichworte ueber CIMgate
- **Nachrichten** — Lesen und Senden von Einsatz-Nachrichten direkt aus dem Chat
- **Geodaten** — Entfernungsberechnung (WGS-84) und OpenStreetMap-Abfragen (Overpass API)
- **Wetterdaten** — Aktuelle Temperatur und 12h-Vorhersage vom Deutschen Wetterdienst (DWD)

### Demo

#### Waldbrand Perlacher Forst (agent)

<div align="center">

<img src="./media/demo_wildfire_perlacherforst_handover.png" alt="Waldbrand – Übergabe" style="width: 45%; margin: 0.5%; display: inline-block;">
<img src="./media/demo_wildfire_perlacher_forst_Commmandx.png" alt="Waldbrand – CommandX" style="width: 45%; margin: 0.5%; display: inline-block;">

</div>

<div align="center">

<video src="./media/demo_wildfire_perlacher_forst_Commmandx.mov" controls title="Waldbrand – CommandX" style="width: 45%; margin: 0.5%;"></video>
<video src="./media/demo_wildfire_perlacherforst_handover_comprehension.mov" controls title="Waldbrand – Übergabe & Lagebild" style="width: 45%; margin: 0.5%;"></video>
<video src="./media/demo_wildfire_perlacherforst_instagram.mov" controls title="Waldbrand – Instagram-Post" style="width: 45%; margin: 0.5%;"></video>
<video src="./media/demo_wildfire_perlacherforst_instagram_press_statement.mov" controls title="Waldbrand – Pressemitteilung" style="width: 45%; margin: 0.5%;"></video>

</div>


#### TUM Einsatz (agentv2)

<div align="center">

<img src="./media/tum-einsatz_demo-agent-chat.png" alt="Agent Chat" style="width: 22%; margin: 0.5%; display: inline-block;">
<img src="./media/tum-einsatz_demo-einsatzfahrzeuge.png" alt="Einsatzfahrzeuge" style="width: 22%; margin: 0.5%; display: inline-block;">
<img src="./media/tum-einsatz_demo-routen-planung.png" alt="Routenplanung" style="width: 22%; margin: 0.5%; display: inline-block;">
<img src="./media/tum-einsatz_demo-fullscreen.png" alt="Fullscreen" style="width: 22%; margin: 0.5%; display: inline-block;">

</div>

<div align="center">

<video src="./media/demo_hydrants_munich.mp4" controls title="Hydrants Munich" style="width: 90%; margin: 0.5%;"></video>

</div>


## Architektur

<div align="center">

<img src="./media/architecture_v1.png" alt="Architektur" style="width: 90%;">

</div>

## Quick Start

### Mit Docker Compose

```bash
# Konfiguration anlegen
cp agent/config.example.json agent/config.json
# config.json bearbeiten: LLM-Endpunkt und API-Keys eintragen

# Fuer CommandX: CIMgate-Zugangsdaten hinterlegen
cp commandx/.env.example commandx/.env
# .env bearbeiten

# Stack starten
docker compose up --build
```

Die Anwendung ist dann unter `http://localhost:3001` erreichbar.

### Manuelle Entwicklung

Voraussetzungen: [Bun](https://bun.sh), [uv](https://docs.astral.sh/uv/)

```bash
# Agent (Frontend + Backend)
cd agent && bun install && bun run dev

# Tools-Server
cd tools && uv sync && uv run python main.py

# CommandX-Server
cd commandx && uv sync && uv run python main.py
```

Ausfuehrliche Entwicklerdokumentation: [`docs/DEV-DOCS.md`](docs/DEV-DOCS.md)

## Contributors

Siehe [contributors.md](contributors.md) fuer die vollstaendige Liste aller Mitwirkenden.

<div align="center">

<img src="./media/team_fugs_ki.jpeg" alt="Team FUGS&KI" style="width: 90%;">

</div>

## Lizenz

MIT
