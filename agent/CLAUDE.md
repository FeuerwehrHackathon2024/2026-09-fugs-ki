# CLAUDE.md

## Project Overview

Chat MVP using AI SDK v6 with a local Gemma 4 model and MCP tool integration.

## Technology Stack

- **Frontend**: React 19 + Vite + Tailwind CSS v4
- **Backend**: Bun.serve (single file, no framework)
- **AI**: AI SDK v6 (`ai`, `@ai-sdk/openai-compatible`, `@ai-sdk/mcp`, `@ai-sdk/react`)
- **LLM**: Gemma 4 26B Q8_0 via llama.cpp at `http://192.168.188.24:8080`
- **MCP Servers**: configurable remote servers via SSE or Streamable HTTP (see `config.json`)
- **Code Quality**: Biome (linting, formatting)
- **Package Manager**: Bun

## Architecture

- `server/index.ts` — Bun.serve backend: MCP clients init at startup, POST /api/chat streams via AI SDK
- `src/App.tsx` — React chat UI using `useChat` from `@ai-sdk/react`
- `config.json` — LLM endpoint and remote MCP server list (gitignored, copy from `config.example.json`)
- `Dockerfile` — Multi-stage build (bun install + vite build → slim production image)
- No database, no auth, no message persistence

## Commands

- `bun dev` — Start frontend (Vite :5173) + backend (Bun :3001) in parallel
- `bun run build` — Production build
- `bun start` — Production server (serves static + API)
- `bun run check` — Biome lint + format check
- `bun run typecheck` — TypeScript type checking

## Key Notes

- Backend uses `toUIMessageStreamResponse()` (Web standard Response, not Node.js ServerResponse)
- Set `idleTimeout: 255` on Bun.serve and `server.timeout(req, 0)` per streaming request
- MCP clients are long-lived (created once at startup, closed on SIGINT/SIGTERM)
- Remote MCP servers configured in `config.json` — supports `"sse"` and `"http"` transports
- System prompt injects current time as a reminder before each request
- Uses full AI SDK UI protocol (UIMessage + parts) for future tool approval flows
- Docker: `docker compose up` from repo root; config is bind-mounted for easy editing

## CommandX-Write-Tools (Learnings)

Schreibzugriffe auf CIMgate haben ein paar Fallstricke — die MCP-Tools in `commandx/tools/` kapseln das, aber der Agent sollte sie kennen:

- **Envelope-Antworten**: `POST /Mission` & Co. liefern HTTP 201 mit `{id, success, message}`. Ein HTTP-200/201 bedeutet NICHT Erfolg! `tools/_writes.py::ensure_success` prüft `success=false` und Zero-GUID (`00000000-…`) und wirft `CommandXWriteError`. Alle `add_*` / `send_*` Tools wenden diese Prüfung an — der Agent bekommt also echte Fehler sichtbar zurück.
- **Readback nach jedem Write**: Nach `ensure_success` ruft `readback_from_list(client, list_path, id)` den Listen-Endpoint nochmal ab und gibt den tatsächlich persistierten Datensatz zurück. Bei fehlgeschlagener Rücklesung ist `_readback` im Ergebnis gesetzt (`"failed: …"` oder `"not_found_in_list"`) — der Agent kann das im Chat-Output prüfen.
- **`create_mission` ist hart abgesichert**:
  - `missionCategory` ist intern fest auf `4` (ELS) gepinnt — CIMgate lehnt alles andere ab ("MissionCategory must be ELS").
  - Nach dem POST wird automatisch `PUT /Mission/{id}` mit `mainDepartmentStationId = Hackathon` + `isElsTakenover=true` ausgeführt, damit der Einsatz in der regulären Einsatzliste (nicht im ELS-Eingang) landet.
  - Department-Auflösung: ENV `COMMANDX_DEFAULT_DEPARTMENT_ID` → Name-Lookup (`COMMANDX_DEFAULT_DEPARTMENT_NAME`, default `Hackathon`) → CIMgate-Default.
  - Das Tool gibt abschließend `GET /Mission/{id}` zurück (id, state, dept, startDate, address, …).
- **Zeitstempel**: Alle Datumseingaben laufen durch `tools/_dates.py::to_utc_iso()`. CIMgate speichert wallclock-as-UTC, die WebUI rechnet lokal drauf. Interne Konvertierung: naive Eingaben werden als Europe/Berlin interpretiert und mit `Z` gesendet. `"now"` oder `None` → aktuelle Systemzeit.
- **Messages sind nicht editierbar**: `PUT /message/{id}` liefert 405. Falsche Timestamps lassen sich nachträglich nicht korrigieren — also beim Absenden richtig setzen.
- **Damage-POST**: verlangt `external_id` (Pflicht). `symbolId` ist optional, aber der Server weist manche Kombinationen mit 400 ab — dann im Chat sauber melden, nicht retryen.
- **Alarm-Keyword-Endpoint** heißt `alarmkeyword` (zusammengeschrieben, nicht `alarm-keyword`).

## Agent-Workflow bei Einsatzanlage

System-Prompt hat eine „Notfallabfrage" (W-Fragen: WAS/WO/WANN/WER/Wieviele/Befehlsstelle). Pflichtfelder für `create_mission`:

- `alarm_keyword` + `description`
- `city` ODER `map_latitude`+`map_longitude` (sonst erst nachfragen)

Optional aber wertvoll: `street`+`street_number`+`post_code`, `object_name`, `reporter_contact_person`, `additional_information`, `start_date` (sonst „now"). Das Tool legt nicht mit Platzhaltern an.

