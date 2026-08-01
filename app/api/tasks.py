import json
from app.core.redis_client import redis_client
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.task import Task
from app.models.project import Project
from app.models.user import User

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.core.dependencies import get_current_user

from typing import Optional
from datetime import datetime
from app.tasks.notification_tasks import create_notification

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(
        Project.id == task.project_id,
        Project.owner_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        assignee=task.assignee,
        due_date=task.due_date,
        project_id=task.project_id,
        owner_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Invalidate cached task lists for this user
    for key in redis_client.scan_iter(f"tasks:{current_user.id}:*"):
        redis_client.delete(key)

    return new_task

@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    status: Optional[str] = None,
    assignee: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cache_key = (
        f"tasks:{current_user.id}:"
        f"{status}:{assignee}:{start_date}:{end_date}:{skip}:{limit}"
    )

    cached_tasks = redis_client.get(cache_key)

    if cached_tasks:
        return json.loads(cached_tasks)

    query = db.query(Task).filter(Task.owner_id == current_user.id)

    if status:
        query = query.filter(Task.status == status)

    if assignee:
        query = query.filter(Task.assignee == assignee)

    if start_date:
        query = query.filter(Task.due_date >= start_date)

    if end_date:
        query = query.filter(Task.due_date <= end_date)

    tasks = query.offset(skip).limit(limit).all()

    response = [
        TaskResponse.model_validate(task).model_dump(mode="json")
        for task in tasks
    ]

    redis_client.setex(
        cache_key,
        60,
        json.dumps(response)
    )

    return response

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.owner_id == current_user.id
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Store old status before updating
    old_status = task.status
    old_assignee = task.assignee

    update_data = task_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    # Trigger background notification if status changed
    if (
        "status" in update_data
        and old_status != task.status
    ):
        create_notification.delay(
            user_id=current_user.id,
            task_id=task.id,
            message=(
                f"Task '{task.title}' status changed "
                f"from '{old_status}' to '{task.status}'."
            ),
        )


    if (
        "assignee" in update_data
        and old_assignee != task.assignee
    ):
        create_notification.delay(
            user_id=current_user.id,
            task_id=task.id,
            message=(
                f"Task '{task.title}' was reassigned "
                f"from '{old_assignee}' to '{task.assignee}'."
            ),
        )
        
    for key in redis_client.scan_iter(f"tasks:{current_user.id}:*"):
        redis_client.delete(key)
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.owner_id == current_user.id
        )
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    for key in redis_client.scan_iter(f"tasks:{current_user.id}:*"):
        redis_client.delete(key)

    return {"message": "Task deleted successfully"}