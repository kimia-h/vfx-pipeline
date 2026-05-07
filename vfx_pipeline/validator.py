import re
from dataclasses import dataclass
from typing import Optional

VALID_ASSET_TYPES = {"model", "rig", "texture", "render", "cache", "layout"}
VALID_EXTENSIONS = {
    "model": [".abc", ".fbx", ".obj", ".usd"],
    "rig": [".ma", ".mb"],
    "texture": [".exr", ".png", ".tif", ".jpg"],
    "render": [".exr", ".png", ".tif"],
    "cache": [".abc", ".vdb"],
    "layout": [".ma", ".mb", ".usd"],
}

NAME_PATTERN = re.compile(
    r"^(?P<project>[A-Z]{2,6})"
    r"_(?P<sequence>sq\d{3})"
    r"_(?P<shot>sh\d{4})"
    r"_(?P<asset_type>[a-z]+)"
    r"_(?P<asset_name>[a-z0-9]+)"
    r"_(?P<version>v\d{3})"
    r"(?P<extension>\.[a-z]+)$"
)

@dataclass
class ValidationResult:
    valid: bool
    filename: str
    error: Optional[str] = None
    parsed: Optional[dict] = None

def validate_filename(filename: str) -> ValidationResult:
    match = NAME_PATTERN.match(filename)

    if not match:
        return ValidationResult(
            valid=False,
            filename=filename,
            error=(
                "Filename does not match required pattern: "
                "PROJECT_sq###_sh####_assettype_assetname_v###.ext "
                "(e.g. SPM_sq010_sh0020_model_body_v001.abc)"
            )
        )

    parts = match.groupdict()
    asset_type = parts["asset_type"]
    extension = parts["extension"]

    if asset_type not in VALID_ASSET_TYPES:
        return ValidationResult(
            valid=False,
            filename=filename,
            error=f"Unknown asset type '{asset_type}'. Must be one of: {', '.join(VALID_ASSET_TYPES)}"
        )

    if extension not in VALID_EXTENSIONS[asset_type]:
        return ValidationResult(
            valid=False,
            filename=filename,
            error=f"Extension '{extension}' is not valid for asset type '{asset_type}'. "
                  f"Expected one of: {', '.join(VALID_EXTENSIONS[asset_type])}"
        )

    return ValidationResult(
        valid=True,
        filename=filename,
        parsed=parts
    )