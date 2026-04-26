"""
Tests for the Rescue Tablet API client.
"""

import pytest
from rescue_tablet.api.client import RescueTabletClient
from unittest.mock import patch

@pytest.fixture
def client():
    return RescueTabletClient(environment="development")

@patch("rescue_tablet.api.client.requests.post")
def test_create_mission(mock_post, client):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {"id": "123", "name": "Test Mission"}

    mission_data = {"name": "Test Mission", "status": "active"}
    response = client.create_mission(mission_data)

    assert response["id"] == "123"
    assert response["name"] == "Test Mission"
    mock_post.assert_called_once()

@patch("rescue_tablet.api.client.requests.get")
def test_get_mission(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"id": "123", "name": "Test Mission"}

    response = client.get_mission("123")

    assert response["id"] == "123"
    assert response["name"] == "Test Mission"
    mock_get.assert_called_once()

@patch("rescue_tablet.api.client.requests.put")
def test_update_mission(mock_put, client):
    mock_put.return_value.status_code = 200
    mock_put.return_value.json.return_value = {"id": "123", "name": "Updated Mission"}

    mission_data = {"name": "Updated Mission", "status": "completed"}
    response = client.update_mission("123", mission_data)

    assert response["id"] == "123"
    assert response["name"] == "Updated Mission"
    mock_put.assert_called_once()

@patch("rescue_tablet.api.client.requests.delete")
def test_delete_mission(mock_delete, client):
    mock_delete.return_value.status_code = 204

    status_code = client.delete_mission("123")

    assert status_code == 204
    mock_delete.assert_called_once()