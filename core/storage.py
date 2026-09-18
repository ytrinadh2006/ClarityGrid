from __future__ import annotations

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(".claritygrid") / "history.db"


def _connect():
    DB_PATH.parent.mkdir(exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute("CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT, created_at TEXT, payload TEXT)")
    return con


def save_session(filename: str, payload: dict, created_at: str) -> None:
    with _connect() as con:
        con.execute("INSERT INTO sessions(filename, created_at, payload) VALUES (?, ?, ?)", (filename, created_at, json.dumps(payload, default=str)))


def recent_sessions(limit: int = 10) -> list[dict]:
    with _connect() as con:
        rows = con.execute("SELECT id, filename, created_at, payload FROM sessions ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [{"id": r[0], "filename": r[1], "created_at": r[2], "payload": json.loads(r[3])} for r in rows]
