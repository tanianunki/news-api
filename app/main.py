"""news-api: devuelve las noticias de una fecha desde un archivo JSON local."""

import datetime
import json
from pathlib import Path

import orjson
from fastapi import FastAPI, HTTPException, Response

DATA_FILE = Path(__file__).parent.parent / "data" / "news.json"
NEWS: list[dict] = []

app = FastAPI(title="news-api")


@app.on_event("startup")
def load_news() -> None:
    NEWS.clear()
    NEWS.extend(json.loads(DATA_FILE.read_text(encoding="utf-8")))


def as_json(payload: dict) -> Response:
    # Claves ordenadas: la misma petición devuelve siempre los mismos bytes.
    body = orjson.dumps(payload, option=orjson.OPT_SORT_KEYS)
    return Response(body, media_type="application/json")


@app.get("/health")
def health() -> Response:
    return as_json({"status": "ok"})


@app.get("/news")
def news(date: str) -> Response:
    try:
        day = datetime.date.fromisoformat(date)
    except ValueError:
        raise HTTPException(status_code=400, detail="date must be YYYY-MM-DD")
    items = [item for item in NEWS if item["date"] == day.isoformat()]
    return as_json({"date": day.isoformat(), "news": sorted(items, key=lambda item: item["id"])})
