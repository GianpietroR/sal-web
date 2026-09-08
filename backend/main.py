"""SAL Web — applicazione FastAPI.

Serve l'API REST sotto /api e la SPA React precompilata (frontend/dist)
su tutte le altre rotte: un solo processo, un solo punto di accesso.
"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import auth
import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(title="SAL Web", version="0.1.0", lifespan=lifespan)


class LoginIn(BaseModel):
    username: str
    password: str


class CantiereIn(BaseModel):
    nome: str
    committente: str = ""
    impresa: str = ""
    tecnico: str = ""
    oggetto: str = ""


def current_user(request: Request) -> dict:
    """Dipendenza di autenticazione per tutte le rotte /api (tranne health/login)."""
    user = auth.get_user_by_token(request.cookies.get(auth.COOKIE_NAME))
    if not user:
        raise HTTPException(status_code=401, detail="Non autenticato")
    return user


@app.get("/api/health")
def health():
    return {"stato": "ok", "app": "sal-web"}


# --- Autenticazione -------------------------------------------------------

@app.post("/api/login")
def login(payload: LoginIn):
    user = auth.verify_user(payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenziali non valide")
    token = auth.create_session(user["id"])
    resp = JSONResponse({"username": user["username"], "display_name": user["display_name"]})
    resp.set_cookie(
        auth.COOKIE_NAME,
        token,
        max_age=auth.SESSION_DAYS * 86400,
        httponly=True,
        samesite="lax",
    )
    return resp


@app.post("/api/logout")
def logout(request: Request):
    auth.delete_session(request.cookies.get(auth.COOKIE_NAME))
    resp = JSONResponse({"ok": True})
    resp.delete_cookie(auth.COOKIE_NAME)
    return resp


@app.get("/api/me")
def me(user: dict = Depends(current_user)):
    return {"username": user["username"], "display_name": user["display_name"]}


# --- Cantiere (schede) ----------------------------------------------------

@app.get("/api/cantieri")
def list_cantieri(user: dict = Depends(current_user)):
    conn = db.get_conn()
    try:
        rows = conn.execute("SELECT id, nome FROM cantieri ORDER BY id").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


@app.post("/api/cantieri")
def create_cantiere(payload: CantiereIn, user: dict = Depends(current_user)):
    if not payload.nome.strip():
        raise HTTPException(status_code=422, detail="Il nome del cantiere è obbligatorio")
    conn = db.get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO cantieri (nome, committente, impresa, tecnico, oggetto) VALUES (?,?,?,?,?)",
            [payload.nome.strip(), payload.committente, payload.impresa, payload.tecnico, payload.oggetto],
        )
        conn.commit()
        return {"id": cur.lastrowid}
    finally:
        conn.close()


# --- SPA React -------------------------------------------------------------

DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if DIST.exists():
    app.mount("/", StaticFiles(directory=DIST, html=True), name="static")
