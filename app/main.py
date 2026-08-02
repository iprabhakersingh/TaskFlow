from fastapi import FastAPI

from app.db.database import Base, engine
from app.models.user import User              # noqa: F401
from app.models.project import Project        # noqa: F401
from app.models.task import Task              # noqa: F401

from app.api.auth import router as auth_router
from app.api.project import router as project_router
from app.api.tasks import router as task_router
from app.api import notification
from app.api import health
from app.api import metrics

from app.middleware.metrics import MetricsMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

app.add_middleware(MetricsMiddleware)

app.include_router(auth_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(notification.router)
app.include_router(health.router)
app.include_router(metrics.router)


@app.get("/")
def root():
    return {"message": "TaskFlow API is running"}