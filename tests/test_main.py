import pytest
from httpx import AsyncClient
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_serve_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Maa" in response.text

@pytest.mark.asyncio
async def test_mcq_submit_valid():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/mcq-submit", json={"answers": ["Slept like a log", "Ate properly", "On track"]})
    assert response.status_code == 200
    data = response.json()
    assert "mood" in data
    assert "maa_initial_message" in data

@pytest.mark.asyncio
async def test_mcq_submit_invalid():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/mcq-submit", json={})
    assert response.status_code == 422 # Unprocessable Entity

@pytest.mark.asyncio
async def test_chat_valid():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/chat", json={
            "message": "I am worried",
            "context": "Stressed",
            "history": []
        })
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data

@pytest.mark.asyncio
async def test_insights_valid():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/insights", json={
            "history": [{"role": "user", "content": "I can't sleep"}, {"role": "assistant", "content": "Beta calm down"}]
        })
    assert response.status_code == 200
    data = response.json()
    assert "hidden_triggers" in data
    assert "cognitive_distortions" in data
    assert "emotional_pattern" in data
    assert "wellness_score" in data
    assert "action_plan" in data
