from typing import Dict, Any
from rescue_tablet.api.client import RescueTabletClient

class MissionSections:
    def __init__(self, client: RescueTabletClient):
        self.client = client

    def create_section(self, mission_id: str, section_id: str, section_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.client.base_url}missions/{mission_id}/sections/{section_id}"
        response = self.client._session.put(url, json=section_data, headers=self.client._headers())
        response.raise_for_status()
        return response.json()

    def update_section(self, mission_id: str, section_id: str, section_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.client.base_url}missions/{mission_id}/sections/{section_id}"
        response = self.client._session.patch(url, json=section_data, headers=self.client._headers())
        response.raise_for_status()
        return response.json()

    def remove_section(self, mission_id: str, section_id: str) -> Dict[str, Any]:
        url = f"{self.client.base_url}missions/{mission_id}/sections/{section_id}"
        response = self.client._session.delete(url, headers=self.client._headers())
        response.raise_for_status()
        return response.json()