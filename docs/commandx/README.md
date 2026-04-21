## CommandX MCP Starter

Schnelles FastMCP-Template mit ausgelagerten Tool-Modulen.

### Struktur

- `main.py`: erstellt den `FastMCP`-Server und startet ihn
- `generic/__init__.py`: bündelt Tool-Registrierungen
- `generic/time.py`: Beispiel für ein ausgelagertes Tool-Modul

### Starten

```bash
uv run python main.py
```

### Tests

Tests liegen in `tests/` und werden mit [pytest](https://pytest.org) ausgeführt.

```bash
uv run --group dev pytest tests/
```

Einzelnen Test ausführen:

```bash
uv run --group dev pytest tests/test_time.py
```

Mit ausführlicher Ausgabe:

```bash
uv run --group dev pytest tests/ -v
```

### Neue Tools hinzufügen

Lege eine neue Datei an, z. B. `generic/foo.py`:

```python
from mcp.server.fastmcp import FastMCP


def my_tool() -> str:
    return "ok"


def register_tools(mcp: FastMCP) -> None:
    mcp.add_tool(my_tool, name="my_tool")
```

Dann in `generic/__init__.py` registrieren:

```python
from .foo import register_tools as register_foo_tools


def register_generic_tools(mcp: FastMCP) -> None:
    register_foo_tools(mcp)
```

### CIMgate-Schreib-Tools: Contract

Alle schreibenden CommandX-MCP-Tools folgen demselben Muster:

1. **Payload bauen**, Dates via [`tools/_dates.py`](../../commandx/tools/_dates.py) → UTC-ISO mit `Z`.
2. **POST/PUT absetzen** über [`CIMgateClient`](../../commandx/client.py).
3. **`ensure_success(result, label=…)`** aus [`tools/_writes.py`](../../commandx/tools/_writes.py): prüft CIMgate-Envelope `{id, success, message}`. `success=false` oder Zero-GUID `00000000-…` → `CommandXWriteError`.
4. **Readback** via `readback_from_list(client, list_path, id, label=…, envelope=env)`: holt den tatsächlich persistierten Datensatz aus der Listen-API und gibt ihn zurück. Bei Problemen setzt er `_readback` im Ergebnis (`failed: …` / `not_found_in_list`), ohne zu werfen.

Resultat: Die Tools geben dem Agent immer **den echten Server-Zustand** zurück — keine „optimistischen" Bestätigungen.

#### `create_mission` — Spezialfall

CIMgate erfordert mehrere Schritte, damit ein Einsatz in der Standard-Einsatzliste landet:

- `missionCategory` ist hart auf `4` (ELS) gepinnt — andere Werte werden serverseitig mit „MissionCategory must be ELS" abgelehnt.
- Nach `POST /Mission` führt das Tool automatisch `PUT /Mission/{id}` mit `mainDepartmentStationId=<Hackathon-Dept-GUID>` + `isElsTakenover=true` aus. Erst damit wechselt die Kategorie intern auf `Mission` und der Einsatz wird für die konfigurierte Feuerwehr sichtbar.
- Das Ziel-Department wird über `COMMANDX_DEFAULT_DEPARTMENT_ID` bzw. `COMMANDX_DEFAULT_DEPARTMENT_NAME` (Default: `Hackathon`) aufgelöst.
- Am Ende liefert das Tool `GET /Mission/{id}` zurück (id, State, Dept, Adresse, Startzeit …).

#### Zeitstempel

- CIMgate speichert UTC-Werte, die WebUI rechnet lokale Zeitzone drauf.
- `to_utc_iso("now")` → aktueller UTC-Zeitpunkt mit `Z`-Suffix.
- Naive ISO-Strings werden als `Europe/Berlin` interpretiert.
- `PUT /message/{id}` liefert **405** — Nachrichten sind nach dem Absenden **nicht mehr editierbar**. Timestamps also beim Erzeugen korrekt setzen.

#### Fehlerkatalog (beobachtet)

| Symptom | Ursache | Maßnahme |
|---|---|---|
| HTTP 201, `success=false`, Zero-GUID | Pflichtfeld fehlt / falscher Enum-Wert | `ensure_success` wirft — Fehlermeldung aus `message` dem Nutzer zeigen |
| „MissionCategory must be ELS" | `missionCategory != 4` | `create_mission` setzt immer `4` — LLM kann den Wert nicht mehr überschreiben |
| Einsatz nicht in Liste sichtbar | `isElsTakenover=false` oder falsches Dept | `create_mission` erledigt Takeover + Dept-Zuweisung automatisch |
| HTTP 400 bei `add_organogram_damage` | `symbolId` oder Kombination inkompatibel | Fehler transparent an den Nutzer melden, nicht blind retryen |
| Endpoint `alarm-keyword` 404 | Pfad heißt `alarmkeyword` | bereits korrigiert in `tools/other.py` |

