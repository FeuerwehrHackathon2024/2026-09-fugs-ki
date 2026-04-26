"""
API client for interacting with the Rescue Tablet API.

Authentication:
- Pass an API key in the HTTP header `Authorization` as `Bearer <api-key>`.
- API keys are environment-specific.

Base URLs:
- Production: https://missions-api.rescuetablet.com/
- Development: https://missions-api-dev.rescuetablet.com/
"""

import requests
from rescue_tablet.config import get_config

class RescueTabletClient:
    def __init__(self, environment="development"):
        config = get_config(environment)
        self.base_url = config.get("base_url")
        self.api_key = config.get("api_key")
        if not self.base_url or not self.api_key:
            raise ValueError("API configuration is incomplete.")

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def create_mission(self, mission_data):
        """Create or update a mission."""
        url = f"{self.base_url}missions"
        response = requests.post(url, json=mission_data, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def get_mission(self, mission_id):
        """Retrieve a mission by its ID."""
        url = f"{self.base_url}missions/{mission_id}"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def update_mission(self, mission_id, mission_data):
        """Update an existing mission."""
        url = f"{self.base_url}missions/{mission_id}"
        response = requests.put(url, json=mission_data, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def delete_mission(self, mission_id):
        """Delete a mission by its ID."""
        url = f"{self.base_url}missions/{mission_id}"
        response = requests.delete(url, headers=self._headers())
        response.raise_for_status()
        return response.status_code