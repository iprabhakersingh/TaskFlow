import uuid


def create_user(client):
    """
    Register a unique user and return auth headers.
    """

    unique = uuid.uuid4().hex[:8]

    user = {
        "username": f"user_{unique}",
        "email": f"user_{unique}@example.com",
        "password": "Test@123",
    }

    client.post(
        "/auth/signup",
        json=user,
    )

    response = client.post(
        "/auth/login",
        data={
            "username": user["email"],
            "password": user["password"],
        },
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_user_cannot_access_another_users_projects(client, auth_headers):
    """
    User B should not see User A's projects.
    """

    # User A creates project
    client.post(
        "/projects/",
        json={
            "name": "Private Project",
            "description": "Secret",
        },
        headers=auth_headers,
    )

    # User B
    user_b_headers = create_user(client)

    response = client.get(
        "/projects/",
        headers=user_b_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 0


def test_user_cannot_update_another_users_task(
    client,
    auth_headers,
    task_id,
):
    """
    User B cannot update User A's task.
    """

    user_b_headers = create_user(client)

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "status": "Completed",
        },
        headers=user_b_headers,
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_task(
    client,
    auth_headers,
    task_id,
):
    """
    User B cannot delete User A's task.
    """

    user_b_headers = create_user(client)

    response = client.delete(
        f"/tasks/{task_id}",
        headers=user_b_headers,
    )

    assert response.status_code == 404