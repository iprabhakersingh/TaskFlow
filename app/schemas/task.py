from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "Pending"
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    project_id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    assignee: Optional[str]
    due_date: Optional[datetime]
    project_id: int
    owner_id: int

    class Config:
        from_attributes = True