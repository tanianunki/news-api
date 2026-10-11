"""Juez previo: comportamiento público de la API.

Debe pasar igual antes y después de cualquier corrección. La automatización
no puede modificar este archivo.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_news_for_a_date(client):
    response = client.get("/news", params={"date": "2026-03-01"})
    assert response.status_code == 200
    body = response.json()
    assert body["date"] == "2026-03-01"
    assert [item["id"] for item in body["news"]] == [1, 2, 3]
    assert body["news"][0]["title"] == "La ciudad inaugura su primera línea de tranvía"


def test_date_without_news(client):
    response = client.get("/news", params={"date": "2026-03-03"})
    assert response.status_code == 200
    assert response.json() == {"date": "2026-03-03", "news": []}


def test_invalid_date(client):
    response = client.get("/news", params={"date": "ayer"})
    assert response.status_code == 400
