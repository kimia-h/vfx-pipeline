import pytest
from vfx_pipeline.versioning import register_asset, lock_asset, is_locked, get_version_history
from vfx_pipeline.db import get_connection


def cleanup(filepath):
    conn = get_connection()
    conn.execute("DELETE FROM assets WHERE filepath = ?", (filepath,))
    conn.execute("DELETE FROM versions WHERE filepath = ?", (filepath,))
    conn.commit()
    conn.close()


PARSED = {
    "project": "TST",
    "sequence": "sq010",
    "shot": "sh0010",
    "asset_type": "model",
    "asset_name": "body",
    "version": "v001",
    "extension": ".abc"
}
FILEPATH = "/fake/path/TST_sq010_sh0010_model_body_v001.abc"
FILENAME = "TST_sq010_sh0010_model_body_v001.abc"


def test_register_asset():
    cleanup(FILEPATH)
    register_asset(FILENAME, FILEPATH, PARSED, "abc123")
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM assets WHERE filepath = ?", (FILEPATH,)
    ).fetchone()
    conn.close()
    assert row is not None
    assert row["version"] == "v001"
    cleanup(FILEPATH)


def test_lock_asset():
    cleanup(FILEPATH)
    register_asset(FILENAME, FILEPATH, PARSED, "abc123")
    lock_asset(FILEPATH)
    assert is_locked(FILEPATH) is True
    cleanup(FILEPATH)


def test_lock_already_locked():
    cleanup(FILEPATH)
    register_asset(FILENAME, FILEPATH, PARSED, "abc123")
    lock_asset(FILEPATH)
    with pytest.raises(ValueError, match="already locked"):
        lock_asset(FILEPATH)
    cleanup(FILEPATH)


def test_lock_nonexistent_asset():
    with pytest.raises(ValueError, match="not found"):
        lock_asset("/fake/path/nonexistent.abc")


def test_version_history():
    cleanup(FILEPATH)
    register_asset(FILENAME, FILEPATH, PARSED, "abc123")
    history = get_version_history(FILEPATH)
    assert len(history) >= 1
    assert history[0]["version"] == "v001"
    cleanup(FILEPATH)