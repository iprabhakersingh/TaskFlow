from fastapi import FastAPI

from app.db.database import Base, engine
from app.models.user import User
from app.api.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "TaskFlow API is running"}