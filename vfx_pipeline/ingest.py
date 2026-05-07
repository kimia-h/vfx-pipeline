import hashlib
from pathlib import Path
from .validator import validate_filename
from .versioning import register_asset, is_locked


def compute_checksum(filepath: Path) -> str:
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5.update(chunk)
    return md5.hexdigest()


def ingest_directory(directory: str) -> dict:
    path = Path(directory)

    if not path.exists() or not path.is_dir():
        raise ValueError(f"Directory not found: {directory}")

    results = {"passed": [], "failed": [], "skipped": []}

    for filepath in path.iterdir():
        if not filepath.is_file():
            continue

        filename = filepath.name
        result = validate_filename(filename)

        if not result.valid:
            results["failed"].append({
                "filename": filename,
                "error": result.error
            })
            continue

        if is_locked(str(filepath)):
            results["skipped"].append({
                "filename": filename,
                "reason": "Asset is locked"
            })
            continue

        checksum = compute_checksum(filepath)
        register_asset(filename, str(filepath), result.parsed, checksum)
        results["passed"].append({"filename": filename, "parsed": result.parsed})

    return results