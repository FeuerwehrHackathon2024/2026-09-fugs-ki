"""Tests für tools/_dates.to_utc_iso."""
from __future__ import annotations

import re
from datetime import datetime, timezone

from tools._dates import to_utc_iso

UTC_ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def test_none_returns_now_utc():
    result = to_utc_iso(None)
    assert UTC_ISO_RE.match(result)
    # darf nicht mehr als ein paar Sekunden in der Zukunft/Vergangenheit liegen
    parsed = datetime.strptime(result, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    delta = abs((parsed - datetime.now(timezone.utc)).total_seconds())
    assert delta < 5


def test_empty_string_returns_now_utc():
    assert UTC_ISO_RE.match(to_utc_iso(""))


def test_now_literal_returns_now_utc():
    assert UTC_ISO_RE.match(to_utc_iso("now"))
    assert UTC_ISO_RE.match(to_utc_iso("NOW"))


def test_iso_with_z_passes_through():
    assert to_utc_iso("2026-04-21T08:30:00Z") == "2026-04-21T08:30:00Z"


def test_iso_with_tz_offset_converted_to_utc():
    # +02:00 → 2h abziehen
    assert to_utc_iso("2026-04-21T10:30:00+02:00") == "2026-04-21T08:30:00Z"
    # -05:00 → 5h draufaddieren
    assert to_utc_iso("2026-04-21T03:30:00-05:00") == "2026-04-21T08:30:00Z"


def test_invalid_date_returned_raw():
    # ungültige Eingaben werden mit Warnung unverändert zurückgegeben
    assert to_utc_iso("kein datum") == "kein datum"
