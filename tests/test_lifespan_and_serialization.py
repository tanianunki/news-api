"""Regresión: carga de datos en el lifespan y serialización orjson determinista."""

import json

from fastapi.testclient import TestClient

from app.main import NEWS, app


def test_news_loaded_on_startup_via_lifespan():
    NEWS.clear()
    with TestClient(app):
        assert len(NEWS) > 0


def test_response_bytes_have_sorted_keys_and_utf8():
    with TestClient(app) as client:
        first = client.get("/news", params={"date": "2026-03-01"})
        second = client.get("/news", params={"date": "2026-03-01"})
    assert first.status_code == 200
    assert first.headers["content-type"] == "application/json"
    assert first.content == second.content

    body = first.json()
    expected = json.dumps(
        body, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    assert first.content == expected
    assert "línea".encode("utf-8") in first.content
