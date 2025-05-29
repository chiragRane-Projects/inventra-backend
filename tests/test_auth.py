import pytest
from fastapi.testclient import TestClient
from app.db.mongo import user_collection
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    user_collection.delete_many({"username": {"$in": ["testuser@inventra", "adminuser@inventra"]}})
    yield
    user_collection.delete_many({"username": {"$in": ["testuser@inventra", "adminuser@inventra"]}})

def test_register_login_and_access():
    register_payload = {
        "name": "Test User",
        "username": "testuser@inventra",
        "email": "testuser@example.com",
        "password": "test_password",
        "role": "staff"
    }
    # Register user
    response = client.post("/api/auth/register", json=register_payload)
    assert response.status_code == 200
    assert "id" in response.json()

    # Login user
    login_payload = {
        "username": "testuser@inventra",
        "password": "test_password"
    }
    response = client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens and "refresh_token" in tokens

    access_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Access /me endpoint
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser@inventra"
    assert data["role"] == "staff"

    # Staff user accessing staff endpoint - should pass
    response = client.get("/test/staff-data", headers=headers)
    assert response.status_code == 200
    assert response.json() == ["Staff data"]


    # Staff user accessing admin endpoint - should fail
    response = client.get("/test/admin-data", headers=headers)
    assert response.status_code == 403

def test_admin_access():
    # Register admin user
    admin_payload = {
        "name": "Admin User",
        "username": "adminuser@inventra",
        "email": "adminuser@example.com",
        "password": "admin_password",
        "role": "admin"
    }
    response = client.post("/api/auth/register", json=admin_payload)
    assert response.status_code == 200

    # Login admin user
    login_payload = {
        "username": "adminuser@inventra",
        "password": "admin_password"
    }
    response = client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 200
    tokens = response.json()
    access_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Admin user accessing /me endpoint
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "adminuser@inventra"
    assert data["role"] == "admin"

    # Admin user accessing admin endpoint - should pass
    response = client.get("/test/admin-data", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"secret": "only for admins"}

    # Admin user accessing staff endpoint - should pass
    response = client.get("/test/staff-data", headers=headers)
    assert response.status_code == 200

def test_protected_routes_require_auth():
    # No auth header
    response = client.get("/api/auth/me")
    assert response.status_code == 401

    response = client.get("/test/admin-data")
    assert response.status_code == 401

    response = client.get("/test/staff-data")
    assert response.status_code == 401

def test_invalid_login():
    login_payload = {
        "username": "nonexistentuser",
        "password": "wrong_password"
    }
    response = client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 401