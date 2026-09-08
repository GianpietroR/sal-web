"""SAL Web — applicazione FastAPI.

Serve l'API REST sotto /api e la SPA React precompilata (frontend/dist)
su tutte le altre rotte, così l'app è raggiungibile con un solo processo.
"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(title="SAL Web", version="0.1.0", lifespan=lifespan)


@app.get("/api/health")
def health():
    return {"stato": "ok", "app": "sal-web"}


# La SPA React: monta per ultima così le rotte /api hanno la precedenza.
DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if DIST.exists():
    app.mount("/", StaticFiles(directory=DIST, html=True), name="static")
