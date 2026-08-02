from datetime import datetime, timedelta, timezone

from app.tasks.notification_tasks import check_overdue_tasks


def test_task_reassignment_creates_notification(
    client,
    auth_headers,
    project_id,
):
    """
    Reassigning a task should create a notification.
    """

    # Create a fresh task
    create_response = client.post(
        "/tasks/",
        json={
            "title": "Notification Task",
            "description": "Testing reassignment",
            "status": "pending",
            "assignee": "old@example.com",
            "due_date": None,
            "project_id": project_id,
        },
        headers=auth_headers,
    )

    assert create_response.status_code == 200

    task_id = create_response.json()["id"]

    # Reassign it
    response = client.put(
        f"/tasks/{task_id}",
        json={
            "assignee": "newassignee@example.com"
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    # Verify notification
    response = client.get(
        "/notifications/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    notifications = response.json()

    assert any(
        "reassigned" in notification["message"].lower()
        for notification in notifications
    )


def test_overdue_task_creates_notification(
    client,
    auth_headers,
    project_id,
):
    """
    Overdue task should generate a notification.
    """

    response = client.post(
        "/tasks/",
        json={
            "title": "Overdue Task",
            "description": "Testing overdue notification",
            "status": "Pending",
            "assignee": "overdue@example.com",
            "due_date": (
                datetime.now(timezone.utc) - timedelta(days=1)
            ).isoformat(),
            "project_id": project_id,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    # Run Celery task manually during testing
    check_overdue_tasks()

    response = client.get(
        "/notifications/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    notifications = response.json()

    assert any(
        "overdue" in notification["message"].lower()
        for notification in notifications
    )