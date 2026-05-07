import pytest
from pathlib import Path
from vfx_pipeline.ingest import ingest_directory


def test_ingest_valid_directory(tmp_path):
    (tmp_path / "SPM_sq010_sh0020_model_body_v001.abc").touch()
    (tmp_path / "SPM_sq010_sh0020_texture_skin_v001.exr").touch()
    results = ingest_directory(str(tmp_path))
    assert len(results["passed"]) == 2
    assert len(results["failed"]) == 0


def test_ingest_invalid_files(tmp_path):
    (tmp_path / "my_bad_file.abc").touch()
    (tmp_path / "another_wrong.exr").touch()
    results = ingest_directory(str(tmp_path))
    assert len(results["failed"]) == 2
    assert len(results["passed"]) == 0


def test_ingest_mixed(tmp_path):
    (tmp_path / "SPM_sq010_sh0020_model_body_v002.abc").touch()
    (tmp_path / "broken_filename.abc").touch()
    results = ingest_directory(str(tmp_path))
    assert len(results["passed"]) == 1
    assert len(results["failed"]) == 1


def test_ingest_nonexistent_directory():
    with pytest.raises(ValueError, match="not found"):
        ingest_directory("/fake/directory/that/doesnt/exist")