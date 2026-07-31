from app.core.celery_app import celery_app

from app.db.database import SessionLocal
from app.models.notification import Notification


@celery_app.task
def create_notification(
    user_id: int,
    task_id: int,
    message: str
):
    db = SessionLocal()

    try:
        notification = Notification(
            user_id=user_id,
            task_id=task_id,
            message=message
        )

        db.add(notification)
        db.commit()

    finally:
        db.close()