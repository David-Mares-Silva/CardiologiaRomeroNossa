from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.forms import router as forms_router

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(forms_router, prefix="/api")


@app.get("/healthz", include_in_schema=False)
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


app.mount("/", StaticFiles(directory="www", html=True), name="site")
