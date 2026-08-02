import uuid

def test_user_signup(client):
    unique = uuid.uuid4().hex[:8]

    user = {
        "username": f"user_{unique}",
        "email": f"user_{unique}@example.com",
        "password": "Test@123",
    }

    response = client.post(
        "/auth/signup",
        json=user,
    )

    assert response.status_code == 200
    assert response.json()["email"] == user["email"]


def test_user_login(client, user_data):
    client.post(
        "/auth/signup",
        json=user_data,
    )

    response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_projects(client, auth_headers, project_id):
    response = client.get(
        "/projects/",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert any(
        project["id"] == project_id
        for project in response.json()
    )


def test_get_tasks(client, auth_headers, task_id):
    response = client.get(
        "/tasks/",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert any(
        task["id"] == task_id
        for task in response.json()
    )


def test_update_task(client, auth_headers, task_id):
    response = client.put(
        f"/tasks/{task_id}",
        json={
            "status": "completed",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_delete_task(client, auth_headers, task_id):
    response = client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200