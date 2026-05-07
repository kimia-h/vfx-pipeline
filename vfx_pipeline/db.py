import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "pipeline.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL UNIQUE,
            project TEXT,
            sequence TEXT,
            shot TEXT,
            asset_type TEXT,
            version TEXT,
            checksum TEXT,
            locked INTEGER DEFAULT 0,
            ingested_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filepath TEXT NOT NULL,
            version TEXT NOT NULL,
            checksum TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()