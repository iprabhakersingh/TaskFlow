from datetime import datetime, timezone

from app.core.celery_app import celery_app
from app.db.database import SessionLocal

from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.models.notification import Notification


@celery_app.task
def create_notification(
    user_id: int,
    task_id: int,
    message: str,
):
    db = SessionLocal()

    try:
        notification = Notification(
            user_id=user_id,
            task_id=task_id,
            message=message,
        )

        db.add(notification)
        db.commit()

    finally:
        db.close()


@celery_app.task
def check_overdue_tasks():
    db = SessionLocal()

    try:
        overdue_tasks = (
            db.query(Task)
            .filter(
                Task.due_date < datetime.now(timezone.utc),
                Task.status != "Completed",
            )
            .all()
        )

        for task in overdue_tasks:
            existing_notification = (
                db.query(Notification)
                .filter(
                    Notification.task_id == task.id,
                    Notification.message == f"Task '{task.title}' is overdue.",
                )
                .first()
            )

            if existing_notification:
                continue

            notification = Notification(
                user_id=task.owner_id,
                task_id=task.id,
                message=f"Task '{task.title}' is overdue.",
            )

            db.add(notification)

        db.commit()

    finally:
        db.close()