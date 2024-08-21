from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_task(client: TestClient, db: Session):
    client.post(
        "/users/register/",
        json={
            "username": "testuser",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    login_response = client.post(
        "/users/login/",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/tasks/",
        headers=headers,
        json={"title": "Test Task", "description": "Task description", "status": "New"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "New"


def test_update_task(client: TestClient, db: Session):
    client.post(
        "/users/register/",
        json={
            "username": "testuser",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    login_response = client.post(
        "/users/login/",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/tasks/",
        headers=headers,
        json={"title": "Test Task", "description": "Task description", "status": "New"},
    )
    task_id = create_response.json()["id"]

    update_response = client.put(
        f"/tasks/{task_id}/",
        headers=headers,
        json={
            "title": "Updated Task",
            "description": "Updated description",
            "status": "In Progress",
        },
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["title"] == "Updated Task"
    assert data["status"] == "In Progress"


def test_delete_task(client: TestClient, db: Session):
    client.post(
        "/users/register/",
        json={
            "username": "testuser",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    login_response = client.post(
        "/users/login/",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/tasks/",
        headers=headers,
        json={"title": "Test Task", "description": "Task description", "status": "New"},
    )
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}/", headers=headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}/", headers=headers)
    assert get_response.status_code == 404


def test_get_tasks_unauthenticated(client: TestClient):
    response = client.get("/tasks/")
    assert response.status_code == 401


def test_get_tasks_authenticated(client: TestClient, db: Session):
    client.post(
        "/users/register/",
        json={
            "username": "testuser",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    login_response = client.post(
        "/users/login/",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 200


def test_filter_tasks_by_status(client: TestClient, db: Session):
    client.post(
        "/users/register/",
        json={
            "username": "testuser",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    login_response = client.post(
        "/users/login/",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/tasks/", headers=headers, json={"title": "Task 1", "status": "New"})
    client.post(
        "/tasks/", headers=headers, json={"title": "Task 2", "status": "In Progress"}
    )

    response = client.get("/tasks/status/New", headers=headers)
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task 1"


def test_update_task_by_another_user(client: TestClient, db: Session):
    client.post(
        "/users/register/",
        json={
            "username": "user1",
            "password": "password123",
            "first_name": "User",
            "last_name": "One",
        },
    )
    login_response = client.post(
        "/users/login/", json={"username": "user1", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/tasks/", headers=headers, json={"title": "Task", "status": "New"}
    )
    task_id = create_response.json()["id"]

    client.post(
        "/users/register/",
        json={
            "username": "user2",
            "password": "password12345",
            "first_name": "User",
            "last_name": "Two",
        },
    )
    login_response = client.post(
        "/users/login/", json={"username": "user2", "password": "password12345"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    update_response = client.put(
        f"/tasks/{task_id}/",
        headers=headers,
        json={
            "title": "Updated Task",
            "description": "Updated description",
            "status": "In Progress",
        },
    )
    assert update_response.status_code == 403
