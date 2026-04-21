"""Helfer für schreibende CIMgate-Operationen.

CIMgate liefert bei POST häufig einen Envelope `{id, success, message}`
mit HTTP 201 zurück — auch wenn `success=false` ist. Diese Helfer sorgen
dafür, dass solche "stillen" Fehler als Exception geworfen werden, damit
der Agent sie nicht übersieht. Zusätzlich wird nach jedem erfolgreichen
Write über `readback_from_list` der tatsächlich persistierte Datensatz
aus einer Listen-API rausgelesen und als Rückgabewert geliefert.
"""
from __future__ import annotations

import logging
from typing import Any

log = logging.getLogger("commandx")

ZERO_GUID = "00000000-0000-0000-0000-000000000000"


class CommandXWriteError(RuntimeError):
    """Geworfen, wenn CIMgate einen Write-Request mit Fehler quittiert."""


def ensure_success(result: Any, *, label: str) -> dict:
    """Prüft eine CIMgate-POST/PUT-Antwort und wirft bei Fehlern.

    - Envelope `{success: false}`       → `CommandXWriteError`
    - Envelope mit id == ZERO_GUID      → `CommandXWriteError`
    - alles andere wird durchgereicht.
    """
    if not isinstance(result, dict):
        return {"result": result}
    if result.get("success") is False:
        raise CommandXWriteError(
            f"{label}: CIMgate meldet Fehler: {result.get('message') or '(keine Meldung)'}"
        )
    if result.get("id") == ZERO_GUID:
        raise CommandXWriteError(
            f"{label}: CIMgate hat keine gültige ID vergeben "
            f"(message: {result.get('message') or '—'})"
        )
    return result


def readback_from_list(
    client: Any,
    list_path: str,
    entity_id: str,
    *,
    label: str,
    envelope: dict | None = None,
) -> dict:
    """Rücklesung: listet `list_path` auf und gibt den Eintrag mit `id==entity_id` zurück.

    Dient als Bestätigung, dass der neu angelegte Datensatz wirklich persistiert
    wurde. Wenn die Liste den Eintrag nicht enthält, geben wir dennoch die
    Envelope-Antwort zurück (mit zusätzlichem `_readback` Hinweis), statt zu
    werfen — CIMgate-Listen-Endpoints sind nicht alle stabil genug, um daraus
    einen harten Fehler zu machen.
    """
    try:
        items = client.get(list_path)
    except Exception as e:  # noqa: BLE001
        log.warning("%s: Readback-GET %s fehlgeschlagen: %s", label, list_path, e)
        base = dict(envelope or {})
        base.setdefault("id", entity_id)
        base["_readback"] = f"failed: {e!r}"
        return base

    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict) and item.get("id") == entity_id:
                return item

    log.warning("%s: Readback fand id=%s nicht in %s", label, entity_id, list_path)
    base = dict(envelope or {})
    base.setdefault("id", entity_id)
    base["_readback"] = "not_found_in_list"
    return base
