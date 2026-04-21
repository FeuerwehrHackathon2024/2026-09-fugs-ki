"""Tests für tools/_writes: envelope-check + readback."""
from __future__ import annotations

import pytest

from tools._writes import (
    CommandXWriteError,
    ZERO_GUID,
    ensure_success,
    readback_from_list,
)


# ---------- ensure_success ----------


def test_ensure_success_passes_normal_envelope():
    env = {"id": "abc-123", "success": True, "message": "ok"}
    assert ensure_success(env, label="test") is env


def test_ensure_success_passes_without_success_key():
    # CIMgate liefert gelegentlich nur {id}
    env = {"id": "abc-123"}
    assert ensure_success(env, label="test") is env


def test_ensure_success_raises_on_success_false():
    env = {"id": ZERO_GUID, "success": False, "message": "Pflichtfeld fehlt"}
    with pytest.raises(CommandXWriteError) as exc:
        ensure_success(env, label="create_mission")
    assert "create_mission" in str(exc.value)
    assert "Pflichtfeld fehlt" in str(exc.value)


def test_ensure_success_raises_on_zero_guid_even_without_success_false():
    env = {"id": ZERO_GUID, "message": "irgendwas schiefgelaufen"}
    with pytest.raises(CommandXWriteError) as exc:
        ensure_success(env, label="add_mission_resource")
    assert "add_mission_resource" in str(exc.value)
    assert "irgendwas schiefgelaufen" in str(exc.value)


def test_ensure_success_raises_with_none_message():
    env = {"id": ZERO_GUID, "success": False, "message": None}
    with pytest.raises(CommandXWriteError):
        ensure_success(env, label="x")


def test_ensure_success_wraps_non_dict_result():
    # etwa wenn die API mal eine Liste zurückgibt
    assert ensure_success([1, 2, 3], label="x") == {"result": [1, 2, 3]}
    assert ensure_success("ok", label="x") == {"result": "ok"}


# ---------- readback_from_list ----------


class FakeClient:
    def __init__(self, response):
        self._response = response
        self.calls: list[str] = []

    def get(self, path):
        self.calls.append(path)
        if isinstance(self._response, Exception):
            raise self._response
        return self._response


def test_readback_returns_matching_entry():
    items = [
        {"id": "other-1", "name": "X"},
        {"id": "abc-123", "name": "Ziel", "foo": "bar"},
    ]
    client = FakeClient(items)
    result = readback_from_list(client, "mission/m1/message", "abc-123", label="t", envelope={"id": "abc-123"})
    assert result == {"id": "abc-123", "name": "Ziel", "foo": "bar"}
    assert client.calls == ["mission/m1/message"]


def test_readback_not_found_returns_envelope_with_marker():
    client = FakeClient([{"id": "other-1"}])
    env = {"id": "abc-123", "success": True}
    result = readback_from_list(client, "mission/m1/victim", "abc-123", label="t", envelope=env)
    assert result["id"] == "abc-123"
    assert result["_readback"] == "not_found_in_list"


def test_readback_get_raises_returns_envelope_with_failed_marker():
    client = FakeClient(RuntimeError("connection reset"))
    env = {"id": "abc-123"}
    result = readback_from_list(client, "foo", "abc-123", label="t", envelope=env)
    assert result["id"] == "abc-123"
    assert result["_readback"].startswith("failed:")
    assert "connection reset" in result["_readback"]


def test_readback_handles_non_list_response():
    # Wenn CIMgate ein Dict zurückgibt statt einer Liste, soll nicht gecrashed werden
    client = FakeClient({"not": "a list"})
    result = readback_from_list(client, "foo", "abc-123", label="t", envelope={"id": "abc-123"})
    assert result["_readback"] == "not_found_in_list"


def test_readback_without_envelope_uses_entity_id():
    client = FakeClient([{"id": "nope"}])
    result = readback_from_list(client, "foo", "abc-123", label="t")
    assert result == {"id": "abc-123", "_readback": "not_found_in_list"}
