from datetime import datetime
from .db import get_connection


def register_asset(filename: str, filepath: str, parsed: dict, checksum: str):
    conn = get_connection()
    conn.execute("""
        INSERT OR IGNORE INTO assets 
        (filename, filepath, project, sequence, shot, asset_type, version, checksum, ingested_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        filename,
        filepath,
        parsed["project"],
        parsed["sequence"],
        parsed["shot"],
        parsed["asset_type"],
        parsed["version"],
        checksum,
        datetime.now().isoformat()
    ))
    conn.execute("""
        INSERT INTO versions (filepath, version, checksum, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        filepath,
        parsed["version"],
        checksum,
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()


def lock_asset(filepath: str):
    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM assets WHERE filepath = ?", (filepath,)
    )
    asset = cursor.fetchone()

    if not asset:
        conn.close()
        raise ValueError(f"Asset not found in registry: {filepath}")

    if asset["locked"]:
        conn.close()
        raise ValueError(f"Asset is already locked: {filepath}")

    conn.execute(
        "UPDATE assets SET locked = 1 WHERE filepath = ?", (filepath,)
    )
    conn.commit()
    conn.close()


def get_version_history(filepath: str) -> list:
    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM versions WHERE filepath = ? ORDER BY created_at ASC",
        (filepath,)
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def is_locked(filepath: str) -> bool:
    conn = get_connection()
    cursor = conn.execute(
        "SELECT locked FROM assets WHERE filepath = ?", (filepath,)
    )
    row = cursor.fetchone()
    conn.close()
    return bool(row["locked"]) if row else False