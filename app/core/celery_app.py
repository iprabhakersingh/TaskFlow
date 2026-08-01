from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "taskflow",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=False,
)

celery_app.conf.imports = (
    "app.tasks.notification_tasks",
)

celery_app.conf.beat_schedule = {
    "check-overdue-tasks-every-minute": {
        "task": "app.tasks.notification_tasks.check_overdue_tasks",
        "schedule": crontab(minute="*"),
    },
}