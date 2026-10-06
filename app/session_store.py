import json
import os
import sqlite3
from contextlib import closing

from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("SESSION_DB_PATH", "sessions.db")


def _connect():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def _init():
    if os.path.dirname(DB_PATH):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with closing(_connect()) as conn, conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL)""")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_messages_session ON messages (session_id, id)")
        conn.execute("""CREATE TABLE IF NOT EXISTS traces (
            session_id TEXT PRIMARY KEY,
            trace TEXT NOT NULL)""")


_init()


def get_messages(s):
    with closing(_connect()) as conn:
        rows = conn.execute("SELECT role, content FROM messages WHERE session_id = ? ORDER BY id", (s,)).fetchall()
    return [{"role": role, "content": content} for role, content in rows]


def append_message(s, role, content):
    with closing(_connect()) as conn, conn:
        conn.execute("INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)", (s, role, content))


def save_trace(s, t):
    # Keep only the latest request's trace, as before.
    with closing(_connect()) as conn, conn:
        conn.execute("INSERT OR REPLACE INTO traces (session_id, trace) VALUES (?, ?)", (s, json.dumps(t, default=str)))


def get_trace(s):
    with closing(_connect()) as conn:
        row = conn.execute("SELECT trace FROM traces WHERE session_id = ?", (s,)).fetchone()
    return json.loads(row[0]) if row else []
