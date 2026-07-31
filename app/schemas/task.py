from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "Pending"
    project_id: int


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    project_id: int
    owner_id: int

    class Config:
        from_attributes = True