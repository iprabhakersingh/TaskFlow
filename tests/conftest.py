import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    """
    FastAPI test client.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def user_data():
    """
    Unique user for testing.
    """
    unique = uuid.uuid4().hex[:8]

    return {
        "username": f"testuser_{unique}",
        "email": f"test_{unique}@example.com",
        "password": "Test@123",
    }


@pytest.fixture(scope="session")
def auth_headers(client, user_data):
    """
    Register a user and return JWT authorization headers.
    """

    # Register
    client.post(
        "/auth/signup",
        json=user_data,
    )

    # Login
    response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture(scope="session")
def project_id(client, auth_headers):
    """
    Create a project and return its ID.
    """

    response = client.post(
        "/projects/",
        json={
            "name": "Test Project",
            "description": "Project created for testing",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    return response.json()["id"]


@pytest.fixture(scope="session")
def task_id(client, auth_headers, project_id):
    """
    Create a task and return its ID.
    """

    response = client.post(
        "/tasks/",
        json={
            "title": "Sample Task",
            "description": "Task created for testing",
            "status": "pending",
            "assignee": "aman@example.com",
            "due_date": None,
            "project_id": project_id,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    return response.json()["id"]