"""
Mission Control Protocol (MCP) logic for Rescue Tablet integration.
"""

from rescue_tablet.api.client import RescueTabletClient
from rescue_tablet.models.mission import Mission

class MissionControl:
    def __init__(self, environment="development"):
        self.client = RescueTabletClient(environment=environment)

    def create_or_update_mission(self, mission_data):
        """Create or update a mission based on the provided data."""
        mission = Mission(**mission_data)
        if mission.id:
            return self.client.update_mission(mission.id, mission.dict())
        return self.client.create_mission(mission.dict())

    def get_mission_details(self, mission_id):
        """Retrieve mission details by ID."""
        return self.client.get_mission(mission_id)

    def delete_mission(self, mission_id):
        """Delete a mission by ID."""
        return self.client.delete_mission(mission_id)