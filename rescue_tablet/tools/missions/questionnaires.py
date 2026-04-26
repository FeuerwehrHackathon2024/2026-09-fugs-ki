from typing import Dict, Any
from rescue_tablet.api.client import RescueTabletClient

class MissionQuestionnaires:
    def __init__(self, client: RescueTabletClient):
        self.client = client

    def create_questionnaire(self, mission_id: str, questionnaire_id: str, questionnaire_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.client.base_url}missions/{mission_id}/questionnaires/{questionnaire_id}"
        response = self.client._session.put(url, json=questionnaire_data, headers=self.client._headers())
        response.raise_for_status()
        return response.json()

    def remove_questionnaire(self, mission_id: str, questionnaire_id: str) -> Dict[str, Any]:
        url = f"{self.client.base_url}missions/{mission_id}/questionnaires/{questionnaire_id}"
        response = self.client._session.delete(url, headers=self.client._headers())
        response.raise_for_status()
        return response.json()