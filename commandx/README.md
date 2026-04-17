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
