from typing import Dict, Any
from rescue_tablet.api.client import RescueTabletClient

class MissionGroups:
    def __init__(self, client: RescueTabletClient):
        self.client = client

    def get_mission_groups(self) -> Dict[str, Any]:
        url = f"{self.client.base_url}groups"
        response = self.client._session.get(url, headers=self.client._headers())
        response.raise_for_status()
        return response.json()

    def set_mission_group(self, group_id: str, group_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.client.base_url}groups/{group_id}"
        response = self.client._session.put(url, json=group_data, headers=self.client._headers())
        response.raise_for_status()
        return response.json()

    def get_group_missions(self, group_id: str, expand: str = None) -> Dict[str, Any]:
        params = {"expand": expand} if expand else {}
        url = f"{self.client.base_url}groups/{group_id}/missions"
        response = self.client._session.get(url, params=params, headers=self.client._headers())
        response.raise_for_status()
        return response.json()

    def add_mission_to_group(self, group_id: str, mission_data: Dict[str, Any]) -> None:
        url = f"{self.client.base_url}groups/{group_id}/missions"
        response = self.client._session.post(url, json=mission_data, headers=self.client._headers())
        response.raise_for_status()