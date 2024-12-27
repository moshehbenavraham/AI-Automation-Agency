from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ProjectStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ProjectCreate(BaseModel):
    title: str
    description: str
    ai_service: str
    requirements: str

class Project(ProjectCreate):
    id: int
    client_id: int
    status: ProjectStatus
    cost: float = 0.0
    created_at: datetime
    updated_at: datetime