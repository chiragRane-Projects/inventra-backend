import pytest
from fastapi.testclient import TestClient
from app.db.mongo import user_collection
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    user_collection.delete_many({})
        
def test_register_user_success():
    payload = {
        "name": "Test User",
        "username": "testuser@inventra",
        "email": "testuser@example.com",
        "password": "test_password",
        "role": "staff"
    }
    
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data and data['message'] == "User created successfully"
    assert "id" in data
    
def test_register_user_duplicate():
    payload = {
        "name": "Test User",
        "username": "testuser@inventra",
        "email": "testuser@example.com",
        "password": "test_password",
        "role": "staff"
    }
    
    client.post("/api/auth/register", json=payload)
    
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already exists"}

def test_login_success():
    register_payload = {
        "name": "Test User",
        "username": "testuser@inventra",
        "email": "testuser@example.com",
        "password": "test_password",
        "role": "staff"
    }
    client.post("/api/auth/register", json=register_payload)
    
    login_payload = {
        "username": "testuser@inventra",
        "password": "test_password",
    }
    
    response = client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert  "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    
def test_login_invald_password():
    register_payload = {
        "name": "Test User",
        "username": "testuser@inventra",
        "email": "testuser@example.com",
        "password": "test_password",
        "role": "staff"
    }
    client.post("/api/auth/register", json=register_payload)
    
    
    login_payload = {
        "username": "testuser@inventra",
        "password": "paspseie",
    }
    
    response = client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username or password"}

def test_login_nonexistent_user():
    login_payload = {
        "username": "nosuchuser",
        "password": "password"
    }
    response = client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username or password"}