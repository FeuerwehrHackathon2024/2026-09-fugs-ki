from typing import Dict, Any
from rescue_tablet.api.client import RescueTabletClient

class MissionAttendances:
    def __init__(self, client: RescueTabletClient):
        self.client = client

    def add_report_to_mission(self, mission_id: str, report_id: str, report_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.client.base_url}missions/{mission_id}/reports/{report_id}"
        response = self.client._session.put(url, json=report_data, headers=self.client._headers())
        response.raise_for_status()
        return response.json()

    def update_report_publication_status(self, mission_id: str, report_id: str, status_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.client.base_url}missions/{mission_id}/reports/{report_id}/publication/status"
        response = self.client._session.put(url, json=status_data, headers=self.client._headers())
        response.raise_for_status()
        return response.json()