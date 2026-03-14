"""
Minimal FastAPI backend for ASYLUM MVP.
Uses SQLite by default (DATABASE_URL not set); set DATABASE_URL for PostgreSQL.
"""
from pathlib import Path
import json
import time
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os
import sqlite3

app = FastAPI(title="ASYLUM API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# #region agent log
@app.middleware("http")
async def _log_request(request: Request, call_next):
    resp = await call_next(request)
    if request.url.path == "/" or resp.status_code == 404:
        _debug_log("request", {"method": request.method, "path": request.url.path, "status": resp.status_code}, "H2")
    return resp
# #endregion

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./asylum.db")
USE_SQLITE = DATABASE_URL.startswith("sqlite")

# #region agent log
def _debug_log(message: str, data: dict, hypothesis_id: str = ""):
    try:
        log_path = Path(__file__).resolve().parent / "debug-5ed34e.log"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"sessionId": "5ed34e", "location": "api/main.py", "message": message, "data": data, "hypothesisId": hypothesis_id, "timestamp": int(time.time() * 1000)}) + "\n")
    except Exception:
        pass
# #endregion

# ----- SQLite in-memory DB for quick preview -----
def get_conn():
    if USE_SQLITE:
        # Use file path from DATABASE_URL or default
        path = DATABASE_URL.replace("sqlite:///", "").strip() or "./asylum.db"
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        return conn
    import psycopg2
    return psycopg2.connect(DATABASE_URL)


def init_sqlite():
    if not USE_SQLITE:
        return
    conn = sqlite3.connect(DATABASE_URL.replace("sqlite:///", "").strip() or "./asylum.db")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS help_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            help_type VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            language VARCHAR(50) NOT NULL,
            contact_info VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS ngos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            services VARCHAR(500) NOT NULL,
            location VARCHAR(255) NOT NULL,
            contact_info VARCHAR(500) NOT NULL
        );
    """)
    conn.commit()
    conn.close()


# ----- Pydantic models -----
class HelpRequestCreate(BaseModel):
    name: str
    location: str
    help_type: str
    description: str
    language: str
    contact_info: Optional[str] = None


class NGOCreate(BaseModel):
    name: str
    services: str
    location: str
    contact_info: str


# ----- Helpers for DB (SQLite vs Postgres) -----
def run_insert(conn, sql, params, returning_id=True):
    cur = conn.cursor()
    cur.execute(sql, params)
    if returning_id:
        if USE_SQLITE:
            pk = cur.lastrowid
        else:
            pk = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return pk if returning_id else None


def run_select(conn, sql, params=None):
    cur = conn.cursor()
    cur.execute(sql, params or [])
    rows = cur.fetchall()
    cur.close()
    return rows


# ----- Endpoints -----
@app.on_event("startup")
def startup():
    global _APP_HTML
    # #region agent log
    _debug_log("ASYLUM app startup", {"module": "api.main"}, "H5")
    # #endregion
    _APP_HTML = _load_app_html()
    init_sqlite()
    # Port is set by run_server.py or uvicorn CLI
print("ASYLUM server running. Check the URL above for the port (e.g. http://127.0.0.1:8001).", flush=True)


def _load_app_html() -> str:
    """Load app HTML once at startup so root route never does file I/O at request time."""
    index_path = Path(__file__).resolve().parent / "static" / "index.html"
    try:
        if index_path.exists():
            return index_path.read_text(encoding="utf-8")
    except Exception:
        pass
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>ASYLUM</title></head><body>"
        "<h1>ASYLUM</h1><p>API is running. <a href='/docs'>Open API docs</a>.</p></body></html>"
    )


_APP_HTML: str = ""


def _serve_app():
    """Serve the app HTML from disk so updates to static/index.html show without restart."""
    index_path = Path(__file__).resolve().parent / "static" / "index.html"
    try:
        if index_path.exists():
            return HTMLResponse(index_path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return HTMLResponse(_APP_HTML or _load_app_html())


@app.get("/", response_class=HTMLResponse)
def root():
    """Serve the app UI at http://localhost:8000"""
    # #region agent log
    _debug_log("root() called for /", {"path": "/"}, "H1")
    # #endregion
    return _serve_app()


@app.post("/help-request")
def create_help_request(body: HelpRequestCreate):
    conn = get_conn()
    if USE_SQLITE:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO help_requests (name, location, help_type, description, language, contact_info)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (body.name, body.location, body.help_type, body.description, body.language, body.contact_info or "")
        )
        pk = cur.lastrowid
        cur.execute("SELECT id, name, location, help_type, description, language, contact_info, created_at FROM help_requests WHERE id = ?", (pk,))
        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {"id": row[0], "name": row[1], "location": row[2], "help_type": row[3], "description": row[4], "language": row[5], "contact_info": row[6], "created_at": row[7]}
    else:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO help_requests (name, location, help_type, description, language, contact_info)
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING id, name, location, help_type, description, language, contact_info, created_at""",
            (body.name, body.location, body.help_type, body.description, body.language, body.contact_info or "")
        )
        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {"id": row[0], "name": row[1], "location": row[2], "help_type": row[3], "description": row[4], "language": row[5], "contact_info": row[6], "created_at": row[7].isoformat()}


@app.get("/help-requests")
def list_help_requests(
    location: Optional[str] = Query(None),
    help_type: Optional[str] = Query(None)
):
    conn = get_conn()
    q = "SELECT id, name, location, help_type, description, language, contact_info, created_at FROM help_requests WHERE 1=1"
    params = []
    if location:
        q += " AND LOWER(location) LIKE LOWER(?)" if USE_SQLITE else " AND LOWER(location) LIKE LOWER(%s)"
        params.append(f"%{location}%")
    if help_type:
        q += " AND LOWER(help_type) = LOWER(?)" if USE_SQLITE else " AND LOWER(help_type) = LOWER(%s)"
        params.append(help_type)
    q += " ORDER BY created_at DESC"
    rows = run_select(conn, q, params or None)
    conn.close()
    items = []
    for r in rows:
        created = r[7]
        if hasattr(created, "isoformat"):
            created = created.isoformat()
        items.append({"id": r[0], "name": r[1], "location": r[2], "help_type": r[3], "description": r[4], "language": r[5], "contact_info": r[6], "created_at": created})
    return {"items": items}


@app.get("/help-requests/{id}")
def get_help_request(id: int):
    conn = get_conn()
    ph = "?" if USE_SQLITE else "%s"
    rows = run_select(conn, f"SELECT id, name, location, help_type, description, language, contact_info, created_at FROM help_requests WHERE id = {ph}", (id,))
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Not found")
    r = rows[0]
    created = r[7]
    if hasattr(created, "isoformat"):
        created = created.isoformat()
    return {"id": r[0], "name": r[1], "location": r[2], "help_type": r[3], "description": r[4], "language": r[5], "contact_info": r[6], "created_at": created}


@app.post("/ngo")
def create_ngo(body: NGOCreate):
    conn = get_conn()
    if USE_SQLITE:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO ngos (name, services, location, contact_info) VALUES (?, ?, ?, ?)",
            (body.name, body.services, body.location, body.contact_info)
        )
        pk = cur.lastrowid
        cur.execute("SELECT id, name, services, location, contact_info FROM ngos WHERE id = ?", (pk,))
        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {"id": row[0], "name": row[1], "services": row[2], "location": row[3], "contact_info": row[4]}
    else:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO ngos (name, services, location, contact_info) VALUES (%s, %s, %s, %s) RETURNING id, name, services, location, contact_info",
            (body.name, body.services, body.location, body.contact_info)
        )
        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {"id": row[0], "name": row[1], "services": row[2], "location": row[3], "contact_info": row[4]}


@app.get("/ngos")
def list_ngos(location: Optional[str] = Query(None)):
    conn = get_conn()
    q = "SELECT id, name, services, location, contact_info FROM ngos WHERE 1=1"
    params = []
    if location:
        ph = "?" if USE_SQLITE else "%s"
        q += f" AND LOWER(location) LIKE LOWER({ph})"
        params.append(f"%{location}%")
    rows = run_select(conn, q, params or None)
    conn.close()
    items = [{"id": r[0], "name": r[1], "services": r[2], "location": r[3], "contact_info": r[4]} for r in rows]
    return {"items": items}


@app.get("/ngos/nearby")
def ngos_nearby(location: Optional[str] = Query(None)):
    return list_ngos(location)


@app.get("/stats")
def stats():
    conn = get_conn()
    ph = "?" if USE_SQLITE else "%s"
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM help_requests")
    requests_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM ngos")
    ngos_count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return {"help_requests": requests_count, "ngos": ngos_count}


@app.post("/seed")
def seed_demo():
    """Insert demo data for hackathon showcase (idempotent: only if empty)."""
    conn = get_conn()
    cur = conn.cursor()
    if USE_SQLITE:
        cur.execute("SELECT COUNT(*) FROM help_requests")
    else:
        cur.execute("SELECT COUNT(*) FROM help_requests")
    if cur.fetchone()[0] > 0:
        cur.close()
        conn.close()
        return {"message": "Already seeded", "help_requests": 0, "ngos": 0}
    # Seed help requests
    requests = [
        ("Fatima", "Berlin", "housing", "Need temporary housing for family of 4. We speak Arabic and English.", "Arabic", "fatima@example.com"),
        ("Ahmed", "Athens", "legal", "Asylum application support and legal advice needed.", "Arabic", ""),
        ("Maria", "Berlin", "medical", "Need access to healthcare for chronic condition.", "Spanish", "maria+help@mail.org"),
    ]
    ngos = [
        ("Refugee Welcome Berlin", "housing,legal,food", "Berlin", "contact@refugeewelcome.de"),
        ("Solidarity Athens", "legal,medical", "Athens", "info@solidarity-athens.org"),
        ("First Aid NGO", "medical,food", "Berlin", "hello@firstaid-berlin.org"),
    ]
    if USE_SQLITE:
        for r in requests:
            cur.execute(
                "INSERT INTO help_requests (name, location, help_type, description, language, contact_info) VALUES (?,?,?,?,?,?)", r
            )
        for n in ngos:
            cur.execute("INSERT INTO ngos (name, services, location, contact_info) VALUES (?,?,?,?)", n)
    else:
        for r in requests:
            cur.execute(
                "INSERT INTO help_requests (name, location, help_type, description, language, contact_info) VALUES (%s,%s,%s,%s,%s,%s)", r
            )
        for n in ngos:
            cur.execute("INSERT INTO ngos (name, services, location, contact_info) VALUES (%s,%s,%s,%s)", n)
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Demo data seeded", "help_requests": len(requests), "ngos": len(ngos)}


# Serve the same app UI for these paths (so bookmarks/refresh work). Do not add /ngos — that is the API.
@app.get("/submit", response_class=HTMLResponse)
def app_submit():
    return _serve_app()


@app.get("/requests", response_class=HTMLResponse)
def app_requests():
    return _serve_app()
