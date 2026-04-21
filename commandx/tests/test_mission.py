"""Tests für create_mission: Payload-Shape, Auto-Takeover, Fehlerbehandlung."""
from __future__ import annotations

from typing import Any

import pytest

from tools import mission as mission_mod
from tools._writes import CommandXWriteError, ZERO_GUID


class FakeClient:
    """Ersetzt den echten CIMgateClient in Tests.

    Speichert alle Calls. POST/PUT-Responses werden per Queue definiert.
    GETs werden per Mapping definiert.
    """

    def __init__(
        self,
        post_responses: list[Any] | None = None,
        put_responses: list[Any] | None = None,
        get_responses: dict[str, Any] | None = None,
    ):
        self.post_responses = post_responses or []
        self.put_responses = put_responses or []
        self.get_responses = get_responses or {}
        self.posts: list[tuple[str, dict]] = []
        self.puts: list[tuple[str, dict]] = []
        self.gets: list[str] = []

        class _S:
            commandx_default_department_id = ""
            commandx_default_department_name = "Hackathon"

        self.settings = _S()

    def post(self, path: str, json: dict):
        self.posts.append((path, json))
        if not self.post_responses:
            raise AssertionError(f"Unerwarteter POST {path}")
        return self.post_responses.pop(0)

    def put(self, path: str, json: dict):
        self.puts.append((path, json))
        if not self.put_responses:
            return {"success": True}
        return self.put_responses.pop(0)

    def get(self, path: str, params=None):  # noqa: ARG002
        self.gets.append(path)
        if path in self.get_responses:
            return self.get_responses[path]
        # Fallback: leere Liste (für Department-Lookup z.B.)
        return []


@pytest.fixture
def fake_client(monkeypatch):
    fc = FakeClient()
    monkeypatch.setattr(mission_mod, "client", fc)
    # Department-Cache reset, damit Tests unabhängig laufen
    monkeypatch.setattr(mission_mod, "_department_cache", None)
    return fc


def test_create_mission_happy_path(fake_client, monkeypatch):
    new_id = "11111111-2222-3333-4444-555555555555"
    fake_client.post_responses = [{"id": new_id, "success": True, "message": "ok"}]
    fake_client.get_responses = {
        "Department": [{"id": "dept-hack", "name": "Hackathon"}],
        f"Mission/{new_id}": {
            "id": new_id,
            "alarmKeyword": "HOCHWASSER",
            "missionState": "Active",
            "missionCategory": "Mission",
            "mainDepartmentStationId": "dept-hack",
            "startDate": "2026-04-21T08:30:00Z",
            "city": "Freiburg",
            "description": "Starkregen, überflutete Keller",
        },
    }

    result = mission_mod.create_mission(
        alarm_keyword="HOCHWASSER",
        alarm_detail="Keller unter Wasser, ca. 40 cm",
        description="Starkregen, überflutete Keller",
        mission_type=3,
        city="Freiburg",
        start_date="2026-04-21T10:30:00+02:00",
    )

    # POST-Payload prüfen
    assert len(fake_client.posts) == 1
    path, payload = fake_client.posts[0]
    assert path == "Mission"
    assert payload["alarmKeyword"] == "HOCHWASSER"
    assert payload["alarmDetail"] == "Keller unter Wasser, ca. 40 cm"
    assert payload["description"] == "Starkregen, überflutete Keller"
    assert payload["missionType"] == 3
    assert payload["missionCategory"] == 4  # hart ELS
    assert payload["missionState"] == 1
    assert payload["startDate"] == "2026-04-21T08:30:00Z"  # UTC-konvertiert
    assert payload["city"] == "Freiburg"

    # PUT wurde aufgerufen: Takeover + Dept
    assert len(fake_client.puts) == 1
    put_path, put_body = fake_client.puts[0]
    assert put_path == f"Mission/{new_id}"
    assert put_body["isElsTakenover"] is True
    assert put_body["mainDepartmentStationId"] == "dept-hack"
    assert put_body["missionCategory"] == 4

    # Rückgabe ist der finale GET-Zustand
    assert result["id"] == new_id
    assert result["mainDepartmentStationId"] == "dept-hack"
    assert result["missionState"] == "Active"


def test_create_mission_raises_on_zero_guid(fake_client):
    fake_client.post_responses = [
        {"id": ZERO_GUID, "success": False, "message": "alarmKeyword is required"}
    ]
    with pytest.raises(CommandXWriteError) as exc:
        mission_mod.create_mission(
            alarm_keyword="",
            alarm_detail="Detail",
            description="desc",
            mission_type=3,
            city="X",
        )
    assert "alarmKeyword is required" in str(exc.value)
    # Bei Fehler wird KEIN PUT abgesetzt
    assert fake_client.puts == []


def test_create_mission_auto_takeover_disabled(fake_client):
    new_id = "aaaa-bbbb"
    fake_client.post_responses = [{"id": new_id, "success": True}]
    fake_client.get_responses = {
        "Department": [{"id": "dept-hack", "name": "Hackathon"}],
        f"Mission/{new_id}": {"id": new_id},
    }
    mission_mod.create_mission(
        alarm_keyword="TEST",
        alarm_detail="x",
        description="y",
        mission_type=1,
        city="X",
        auto_takeover=False,
    )
    # PUT wurde trotzdem abgesetzt (Dept-Zuweisung), aber ohne isElsTakenover
    assert len(fake_client.puts) == 1
    _, put_body = fake_client.puts[0]
    assert "isElsTakenover" not in put_body
    assert put_body["mainDepartmentStationId"] == "dept-hack"


def test_create_mission_explicit_department_overrides_lookup(fake_client):
    new_id = "cccc-dddd"
    fake_client.post_responses = [{"id": new_id, "success": True}]
    fake_client.get_responses = {f"Mission/{new_id}": {"id": new_id}}
    mission_mod.create_mission(
        alarm_keyword="TEST",
        alarm_detail="x",
        description="y",
        mission_type=1,
        city="X",
        department_id="explicit-dept-uuid",
    )
    # Department-Endpoint sollte gar nicht aufgerufen worden sein
    assert "Department" not in fake_client.gets
    _, put_body = fake_client.puts[0]
    assert put_body["mainDepartmentStationId"] == "explicit-dept-uuid"


def test_create_mission_without_department_name_match_keeps_no_dept(fake_client):
    """Wenn Hackathon-Dept nicht gefunden wird und keine explizite ID gesetzt ist,
    bleibt `mainDepartmentStationId` weg → CIMgate nimmt sein Default."""
    new_id = "eeee-ffff"
    fake_client.post_responses = [{"id": new_id, "success": True}]
    fake_client.get_responses = {
        "Department": [{"id": "other", "name": "Irgendwas"}],
        f"Mission/{new_id}": {"id": new_id},
    }
    mission_mod.create_mission(
        alarm_keyword="TEST",
        alarm_detail="x",
        description="y",
        mission_type=1,
        city="X",
    )
    _, put_body = fake_client.puts[0]
    assert "mainDepartmentStationId" not in put_body


def test_create_mission_takeover_failure_does_not_mask_success(fake_client, caplog):
    """Wenn der Takeover-PUT fehlschlägt, bleibt der Einsatz trotzdem angelegt —
    das Tool wirft NICHT, sondern loggt warning und gibt den Einsatz zurück."""
    new_id = "gggg-hhhh"
    fake_client.post_responses = [{"id": new_id, "success": True}]
    fake_client.put_responses = [
        {"id": ZERO_GUID, "success": False, "message": "takeover failed"}
    ]
    fake_client.get_responses = {f"Mission/{new_id}": {"id": new_id, "missionState": "Active"}}

    result = mission_mod.create_mission(
        alarm_keyword="TEST",
        alarm_detail="x",
        description="y",
        mission_type=1,
        city="X",
    )
    assert result["id"] == new_id
