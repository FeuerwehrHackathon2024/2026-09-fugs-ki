from typing import Dict, Any
from rescue_tablet.api.client import RescueTabletClient

class MissionAttendances:
    def __init__(self, client: RescueTabletClient):
        self.client = client

    def get_file_from_mission(self, mission_id: str, file_id: str, no_redirect: bool = False) -> Dict[str, Any]:
        params = {"noRedirect": no_redirect} if no_redirect else {}
        url = f"{self.client.base_url}missions/{mission_id}/files/{file_id}"
        response = self.client._session.get(url, params=params, headers=self.client._headers())
        response.raise_for_status()
        return response.json()

    def request_file_upload(self, mission_id: str, file_id: str, file_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.client.base_url}missions/{mission_id}/files/{file_id}"
        response = self.client._session.put(url, json=file_data, headers=self.client._headers())
        response.raise_for_status()
        return response.json()