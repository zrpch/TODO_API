from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_register_user(client: TestClient, db: Session):
    response = client.post(
        "/users/register/",
        json={
            "username": "testuser",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


def test_login_user(client: TestClient, db: Session):
    client.post(
        "/users/register/",
        json={
            "username": "testuser",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    response = client.post(
        "/users/login/",
        json={"username": "testuser", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_read_users_unauthenticated(client: TestClient):
    response = client.get("/users/")
    assert response.status_code == 401


def test_read_users_authenticated(client: TestClient, db: Session):
    client.post(
        "/users/register/",
        json={
            "username": "testuser",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    response = client.post(
        "/users/login/",
        json={"username": "testuser", "password": "password123"},
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200


def test_register_existing_user(client: TestClient, db: Session):
    client.post(
        "/users/register/",
        json={
            "username": "testuser",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    response = client.post(
        "/users/register/",
        json={
            "username": "testuser",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    assert response.status_code == 400


def test_login_user_with_wrong_password(client: TestClient, db: Session):
    client.post(
        "/users/register/",
        json={
            "username": "testuser",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    response = client.post(
        "/users/login/",
        json={"username": "testuser", "password": "wrongpassword"},
    )
    assert response.status_code == 400
