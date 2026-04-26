from typing import Dict, Any
from rescue_tablet.api.client import RescueTabletClient

class MissionPatients:
    def __init__(self, client: RescueTabletClient):
        self.client = client

    def create_patient(self, mission_id: str, patient_id: str, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.client.base_url}missions/{mission_id}/patients/{patient_id}"
        response = self.client._session.put(url, json=patient_data, headers=self.client._headers())
        response.raise_for_status()
        return response.json()

    def update_patient(self, mission_id: str, patient_id: str, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.client.base_url}missions/{mission_id}/patients/{patient_id}"
        response = self.client._session.patch(url, json=patient_data, headers=self.client._headers())
        response.raise_for_status()
        return response.json()

    def remove_patient(self, mission_id: str, patient_id: str) -> Dict[str, Any]:
        url = f"{self.client.base_url}missions/{mission_id}/patients/{patient_id}"
        response = self.client._session.delete(url, headers=self.client._headers())
        response.raise_for_status()
        return response.json()