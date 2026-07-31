from fastapi import APIRouter
from sqlalchemy import text

from app.db.database import engine
from app.core.redis_client import redis_client

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/")
def health_check():
    status = {
        "api": "healthy",
        "database": "healthy",
        "redis": "healthy"
    }

    # PostgreSQL
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        status["database"] = "unhealthy"

    # Redis
    try:
        redis_client.ping()
    except Exception:
        status["redis"] = "unhealthy"

    status["status"] = (
        "healthy"
        if status["database"] == "healthy"
        and status["redis"] == "healthy"
        else "unhealthy"
    )

    return status