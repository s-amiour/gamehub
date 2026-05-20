import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

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

BASE_PAYLOAD = {
    "title": "Default game",
    "genre": "Default genre",
    "platform": "Default platfor"
}


def test_create_game_success(client):
    payload = {
        **BASE_PAYLOAD, 
        "title": "Hollow Knight",
        "genre": "Metroidvania",
        "release_year": 2017
    }
    response = client.post("/v1/games/", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Hollow Knight"
    assert data["genre"] == "Metroidvania"
    assert "id" in data
    assert "created_at" in data
    assert data["cover_url"] is None


def test_get_game_success(client):
    payload = {**BASE_PAYLOAD, "title": "Celeste"}
    create_resp = client.post("/v1/games/", json=payload)
    game_id = create_resp.json()["id"]
    
    response = client.get(f"/v1/games/{game_id}")
    
    assert response.status_code == 200
    assert response.json()["id"] == game_id
    assert response.json()["title"] == "Celeste"


def test_get_game_not_found(client):
    response = client.get("/v1/games/non-existent-uuid")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Game non-existent-uuid not found"


def test_list_games_pagination(client):
    client.post("/v1/games/", json={**BASE_PAYLOAD, "title": "Game 1"})
    client.post("/v1/games/", json={**BASE_PAYLOAD, "title": "Game 2"})
    
    response = client.get("/v1/games/?limit=10&offset=0")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_search_games(client):
    client.post("/v1/games/", json={**BASE_PAYLOAD, "title": "The Legend of Zelda"})
    client.post("/v1/games/", json={**BASE_PAYLOAD, "title": "Zelda II"})
    client.post("/v1/games/", json={**BASE_PAYLOAD, "title": "Super Mario Odyssey"})
    
    response = client.get("/v1/games/search?q=zelda")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2
    
    titles = [item["title"] for item in data["items"]]
    assert "The Legend of Zelda" in titles
    assert "Zelda II" in titles
