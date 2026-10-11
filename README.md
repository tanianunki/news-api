# news-api

API mínima que devuelve las noticias de una fecha desde `data/news.json`. Es el
repositorio «paciente» de la demo *Technical Debt Automation*: su commit inicial contiene
a propósito deuda de dependencias.

| Hallazgo sembrado | Dónde | Cómo se detecta | Referencia |
|---|---|---|---|
| Dependencia vulnerable: `orjson==3.9.14` | `requirements.txt`, usada en `app/main.py` | `pip-audit -r requirements.txt` | [CVE-2024-27454](https://osv.dev/vulnerability/PYSEC-2024-40), [CVE-2025-67221](https://osv.dev/vulnerability/GHSA-hx9q-6w63-j58v) |
| API deprecada: `@app.on_event("startup")` | `app/main.py` | `python -W error::DeprecationWarning:app.main -c "import app.main"` | [FastAPI: Lifespan Events](https://fastapi.tiangolo.com/advanced/events/) |

Los tests pasan en ese estado: tests verdes no implican dependencias sanas.

## Uso

```sh
python3.12 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt pip-audit==2.10.1
uvicorn app.main:app                      # GET /health, GET /news?date=2026-03-01
python -m pytest -q                       # tests (pasan)
pip-audit -r requirements.txt             # auditoría (falla en el commit inicial)
python -W error::DeprecationWarning:app.main -c "import app.main"   # deprecación (falla)
```

Con Docker: `docker build -t news-api . && docker run --rm -p 8000:8000 news-api`.

## Juez y hueco de pruebas

`tests/test_api.py` es el **juez previo**: fija el comportamiento público y debe pasar
igual antes y después de cualquier corrección. La automatización no puede modificarlo, ni
tampoco `.github/workflows/ci.yml`.

Hueco conocido: el juez compara el JSON ya parseado, así que nadie comprueba los bytes
exactos de la respuesta (claves ordenadas), que es justo lo que produce `orjson`.

## CI

Un solo job, `verify`, ejecuta esos mismos comandos en cada pull request y en `main`.
