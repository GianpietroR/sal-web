"""Autenticazione: password (PBKDF2-SHA256) e sessioni su cookie HttpOnly.

Solo librerie standard: niente dipendenze extra da mantenere.
Il cookie è SameSite=Lax + HttpOnly; l'app è raggiungibile solo dal tailnet,
quindi la superficie di attacco resta minima.
"""
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import db

COOKIE_NAME = "sal_session"
SESSION_DAYS = 30


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%fZ")


def hash_password(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000).hex()


def new_salt() -> bytes:
    return secrets.token_bytes(16)


def create_user(username: str, display_name: str, password: str) -> None:
    conn = db.get_conn()
    try:
        salt = new_salt()
        conn.execute(
            "INSERT INTO users (username, display_name, password_hash, salt) VALUES (?,?,?,?)",
            [username.lower(), display_name, hash_password(password, salt), salt.hex()],
        )
        conn.commit()
    finally:
        conn.close()


def verify_user(username: str, password: str):
    """Ritorna la riga utente o None."""
    conn = db.get_conn()
    try:
        row = conn.execute("SELECT * FROM users WHERE username=?", [username.lower()]).fetchone()
        if not row:
            return None
        if hash_password(password, bytes.fromhex(row["salt"])) != row["password_hash"]:
            return None
        return dict(row)
    finally:
        conn.close()


def create_session(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    expires = (datetime.now(timezone.utc) + timedelta(days=SESSION_DAYS)).strftime("%Y-%m-%dT%H:%M:%fZ")
    conn = db.get_conn()
    try:
        conn.execute("INSERT INTO sessions (token, user_id, expires_at) VALUES (?,?,?)", [token, user_id, expires])
        conn.commit()
    finally:
        conn.close()
    return token


def get_user_by_token(token: str):
    if not token:
        return None
    conn = db.get_conn()
    try:
        row = conn.execute(
            "SELECT u.id, u.username, u.display_name FROM sessions s JOIN users u ON u.id=s.user_id"
            " WHERE s.token=? AND s.expires_at>?",
            [token, _now_iso()],
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def delete_session(token: str) -> None:
    if not token:
        return
    conn = db.get_conn()
    try:
        conn.execute("DELETE FROM sessions WHERE token=?", [token])
        conn.commit()
    finally:
        conn.close()
