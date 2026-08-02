from app.core.redis_client import redis_client


def test_get_tasks_creates_cache(
    client,
    auth_headers,
):
    """
    GET /tasks should create a Redis cache entry.
    """

    # Clear existing cache
    for key in redis_client.scan_iter("tasks:*"):
        redis_client.delete(key)

    response = client.get(
        "/tasks/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    cache_keys = list(redis_client.scan_iter("tasks:*"))

    assert len(cache_keys) > 0


def test_update_task_invalidates_cache(
    client,
    auth_headers,
    task_id,
):
    """
    Updating a task should invalidate the Redis cache.
    """

    # Create cache
    client.get(
        "/tasks/",
        headers=auth_headers,
    )

    cache_keys = list(redis_client.scan_iter("tasks:*"))

    assert len(cache_keys) > 0

    # Update task
    response = client.put(
        f"/tasks/{task_id}",
        json={
            "status": "Pending"
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    cache_keys = list(redis_client.scan_iter("tasks:*"))

    assert len(cache_keys) == 0


def test_create_task_invalidates_cache(
    client,
    auth_headers,
    project_id,
):
    """
    Creating a task should invalidate cached task lists.
    """

    # Create cache
    client.get(
        "/tasks/",
        headers=auth_headers,
    )

    assert len(list(redis_client.scan_iter("tasks:*"))) > 0

    response = client.post(
        "/tasks/",
        json={
            "title": "Cache Test",
            "description": "Testing Redis",
            "status": "Pending",
            "assignee": "cache@example.com",
            "due_date": None,
            "project_id": project_id,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    assert len(list(redis_client.scan_iter("tasks:*"))) == 0


def test_delete_task_invalidates_cache(
    client,
    auth_headers,
    project_id,
):
    """
    Deleting a task should invalidate cached task lists.
    """

    response = client.post(
        "/tasks/",
        json={
            "title": "Delete Cache",
            "description": "Delete",
            "status": "Pending",
            "assignee": "delete@example.com",
            "due_date": None,
            "project_id": project_id,
        },
        headers=auth_headers,
    )

    task_id = response.json()["id"]

    # Create cache
    client.get(
        "/tasks/",
        headers=auth_headers,
    )

    assert len(list(redis_client.scan_iter("tasks:*"))) > 0

    response = client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    assert len(list(redis_client.scan_iter("tasks:*"))) == 0