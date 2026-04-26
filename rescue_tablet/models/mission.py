"""
Data models for Rescue Tablet missions.
"""

from pydantic import BaseModel
from typing import Optional, List

class Mission(BaseModel):
    id: Optional[str]
    name: str
    description: Optional[str]
    status: str
    created_at: Optional[str]
    updated_at: Optional[str]

class MissionList(BaseModel):
    missions: List[Mission]