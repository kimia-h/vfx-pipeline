import pytest
from vfx_pipeline.validator import validate_filename


def test_valid_filename():
    result = validate_filename("SPM_sq010_sh0020_model_body_v001.abc")
    assert result.valid is True
    assert result.parsed["project"] == "SPM"
    assert result.parsed["sequence"] == "sq010"
    assert result.parsed["shot"] == "sh0020"
    assert result.parsed["asset_type"] == "model"
    assert result.parsed["version"] == "v001"


def test_valid_texture():
    result = validate_filename("SPM_sq020_sh0030_texture_skin_v003.exr")
    assert result.valid is True
    assert result.parsed["asset_type"] == "texture"


def test_missing_version():
    result = validate_filename("SPM_sq010_sh0020_model_body.abc")
    assert result.valid is False
    assert "pattern" in result.error.lower()


def test_wrong_extension_for_type():
    result = validate_filename("SPM_sq010_sh0020_model_body_v001.exr")
    assert result.valid is False
    assert "extension" in result.error.lower()


def test_unknown_asset_type():
    result = validate_filename("SPM_sq010_sh0020_anim_body_v001.abc")
    assert result.valid is False
    assert "asset type" in result.error.lower()


def test_bad_naming_no_pattern():
    result = validate_filename("my_asset_final_FINAL.abc")
    assert result.valid is False


def test_lowercase_project_code_fails():
    result = validate_filename("spm_sq010_sh0020_model_body_v001.abc")
    assert result.valid is False


def test_version_format():
    result = validate_filename("SPM_sq010_sh0020_model_body_v1.abc")
    assert result.valid is False