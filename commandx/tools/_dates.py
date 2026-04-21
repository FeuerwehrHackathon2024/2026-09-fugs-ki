"""Hilfsfunktion: alle Datumsfelder werden vor dem Senden nach UTC konvertiert.

CIMgate ignoriert die Zeitzoneninfo beim Speichern und interpretiert die
Wallclock-Zeit als UTC. Sendet man "+02:00" zeigt die WebUI alles 2h zu spät.
Lösung: immer als UTC mit "Z"-Suffix senden.
"""
from __future__ import annotations

from datetime import datetime, timezone
import logging

log = logging.getLogger("commandx")


def to_utc_iso(value: str | None) -> str | None:
    """ISO-8601-Zeit nach UTC konvertieren ('YYYY-MM-DDTHH:MM:SSZ').

    - None / "" / "now"  → aktueller Zeitpunkt UTC
    - String mit TZ      → in UTC umrechnen
    - String ohne TZ     → als lokale Systemzeit interpretieren, dann UTC
    - ungültig           → unverändert (mit Warnung)
    """
    if value is None or not value or str(value).lower() == "now":
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        log.warning("Ungültiges Datum '%s' – sende roh weiter", value)
        return value
    if parsed.tzinfo is None:
        parsed = parsed.astimezone()
    return parsed.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
