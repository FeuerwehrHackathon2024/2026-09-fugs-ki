from typing import Dict, Any
from rescue_tablet.api.client import RescueTabletClient

class MissionMapElements:
    def __init__(self, client: RescueTabletClient):
        self.client = client

    def create_map_element(self, mission_id: str, element_id: str, element_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.client.base_url}missions/{mission_id}/map-elements/{element_id}"
        response = self.client._session.put(url, json=element_data, headers=self.client._headers())
        response.raise_for_status()
        return response.json()

    def remove_map_element(self, mission_id: str, element_id: str) -> Dict[str, Any]:
        url = f"{self.client.base_url}missions/{mission_id}/map-elements/{element_id}"
        response = self.client._session.delete(url, headers=self.client._headers())
        response.raise_for_status()
        return response.json()