from fastapi import FastAPI

from app.db.database import Base, engine
from app.models.user import User
from app.api.auth import router as auth_router
from app.models.project import Project
from app.api.project import router as project_router
from app.api.tasks import router as task_router
from app.models.task import Task
from app.api import notification
from app.api import health

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

app.include_router(auth_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(notification.router)
app.include_router(health.router)

@app.get("/")
def root():
    return {"message": "TaskFlow API is running"}