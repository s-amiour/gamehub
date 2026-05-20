import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# in-memory db for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def test_create_user_success(client):
    payload = {
        "username": "testplayer",
        "email": "testplayer@example.com",
        "password": "securepassword123"
    }
    response = client.post("/v1/users/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data

def test_create_user_duplicate_username(client):
    payload = {
        "username": "duplicate_user",
        "email": "first@example.com",
        "password": "password123"
    }
    client.post("/v1/users/", json=payload)    
    payload["email"] = "second@example.com"
    response = client.post("/v1/users/", json=payload)
    assert response.status_code >= 400 


def test_get_user_success(client):
    payload = {
        "username": "get_target",
        "email": "target@example.com",
        "password": "password"
    }
    create_resp = client.post("/v1/users/", json=payload)
    user_id = create_resp.json()["id"]
    response = client.get(f"/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id
    assert response.json()["username"] == "get_target"


def test_get_user_not_found(client):
    response = client.get("/v1/users/invalid-uuid-0000")
    assert response.status_code == 404
    assert response.json()["detail"] == "User invalid-uuid-0000 not found"


def test_list_users_pagination(client):
    client.post("/v1/users/", json={"username": "player1", "email": "p1@example.com", "password": "pass"})
    client.post("/v1/users/", json={"username": "player2", "email": "p2@example.com", "password": "pass"})
    response = client.get("/v1/users/?limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2
    assert data["limit"] == 10
    assert data["offset"] == 0