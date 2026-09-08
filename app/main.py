from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.forms import router as forms_router

# In the Docker image, the Dockerfile stages the site under ./www (alongside
# app/). Running straight from a repo checkout (e.g. `uv run uvicorn ...`
# for local dev without Docker), that staging step hasn't happened, so fall
# back to the repo root, where the same files already live. Either way, only
# `assets/`, `index.html` and `inner-page.html` are ever exposed over HTTP —
# never the whole directory (which would otherwise leak `.env`, `app/`, etc.).
_REPO_ROOT = Path(__file__).resolve().parent.parent
WWW_DIR = _REPO_ROOT / "www" if (_REPO_ROOT / "www").is_dir() else _REPO_ROOT

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(forms_router, prefix="/api")
app.mount("/assets", StaticFiles(directory=WWW_DIR / "assets"), name="assets")


@app.get("/healthz", include_in_schema=False)
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(WWW_DIR / "index.html")


@app.get("/inner-page.html", include_in_schema=False)
async def inner_page() -> FileResponse:
    return FileResponse(WWW_DIR / "inner-page.html")


@app.get("/privacidad.html", include_in_schema=False)
async def privacidad() -> FileResponse:
    return FileResponse(WWW_DIR / "privacidad.html")


@app.get("/robots.txt", include_in_schema=False)
async def robots() -> FileResponse:
    return FileResponse(WWW_DIR / "robots.txt")


@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap() -> FileResponse:
    return FileResponse(WWW_DIR / "sitemap.xml")
