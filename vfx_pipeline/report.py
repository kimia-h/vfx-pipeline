from datetime import datetime
from .db import get_connection


def generate_report() -> dict:
    conn = get_connection()

    assets = conn.execute("SELECT * FROM assets").fetchall()
    assets = [dict(a) for a in assets]

    total = len(assets)
    locked = sum(1 for a in assets if a["locked"])
    unlocked = total - locked

    by_type = {}
    for a in assets:
        t = a["asset_type"]
        by_type[t] = by_type.get(t, 0) + 1

    by_shot = {}
    for a in assets:
        shot = f"{a['sequence']}_{a['shot']}"
        by_shot[shot] = by_shot.get(shot, 0) + 1

    failed = conn.execute(
        "SELECT COUNT(*) as c FROM assets WHERE checksum IS NULL"
    ).fetchone()["c"]

    conn.close()

    return {
        "generated_at": datetime.now().isoformat(),
        "total_assets": total,
        "locked": locked,
        "unlocked": unlocked,
        "by_type": by_type,
        "by_shot": by_shot,
        "validation_failures": failed,
    }