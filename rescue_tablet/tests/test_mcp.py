"""
Tests for the Mission Control Protocol (MCP) logic.
"""

import pytest
from rescue_tablet.mcp.mission_control import MissionControl
from unittest.mock import patch

@pytest.fixture
def mission_control():
    return MissionControl(environment="development")

@patch("rescue_tablet.mcp.mission_control.RescueTabletClient.create_mission")
def test_create_mission(mock_create_mission, mission_control):
    mock_create_mission.return_value = {"id": "123", "name": "New Mission"}

    mission_data = {"name": "New Mission", "status": "active"}
    response = mission_control.create_or_update_mission(mission_data)

    assert response["id"] == "123"
    assert response["name"] == "New Mission"
    mock_create_mission.assert_called_once()

@patch("rescue_tablet.mcp.mission_control.RescueTabletClient.update_mission")
def test_update_mission(mock_update_mission, mission_control):
    mock_update_mission.return_value = {"id": "123", "name": "Updated Mission"}

    mission_data = {"id": "123", "name": "Updated Mission", "status": "completed"}
    response = mission_control.create_or_update_mission(mission_data)

    assert response["id"] == "123"
    assert response["name"] == "Updated Mission"
    mock_update_mission.assert_called_once()

@patch("rescue_tablet.mcp.mission_control.RescueTabletClient.get_mission")
def test_get_mission_details(mock_get_mission, mission_control):
    mock_get_mission.return_value = {"id": "123", "name": "Test Mission"}

    response = mission_control.get_mission_details("123")

    assert response["id"] == "123"
    assert response["name"] == "Test Mission"
    mock_get_mission.assert_called_once()

@patch("rescue_tablet.mcp.mission_control.RescueTabletClient.delete_mission")
def test_delete_mission(mock_delete_mission, mission_control):
    mock_delete_mission.return_value = 204

    status_code = mission_control.delete_mission("123")

    assert status_code == 204
    mock_delete_mission.assert_called_once()