from typing import Dict, Any
from rescue_tablet.api.client import RescueTabletClient

class MissionAttendances:
    def __init__(self, client: RescueTabletClient):
        self.client = client

    def create_attendance(self, mission_id: str, attendance_id: str, attendance_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.client.base_url}missions/{mission_id}/attendances/{attendance_id}"
        response = self.client._session.put(url, json=attendance_data, headers=self.client._headers())
        response.raise_for_status()
        return response.json()

    def update_attendance(self, mission_id: str, attendance_id: str, attendance_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.client.base_url}missions/{mission_id}/attendances/{attendance_id}"
        response = self.client._session.patch(url, json=attendance_data, headers=self.client._headers())
        response.raise_for_status()
        return response.json()

    def remove_attendance(self, mission_id: str, attendance_id: str) -> Dict[str, Any]:
        url = f"{self.client.base_url}missions/{mission_id}/attendances/{attendance_id}"
        response = self.client._session.delete(url, headers=self.client._headers())
        response.raise_for_status()
        return response.json()