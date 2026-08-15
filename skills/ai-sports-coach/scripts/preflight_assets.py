#!/usr/bin/env python3
"""Validate local assets, source provenance, and public-release readiness."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".m4v"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
RIGHTS = {"owned", "licensed", "permission-granted", "research-only", "unknown"}
REDISTRIBUTION = {"allowed", "not-allowed", "unknown"}


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.is_file():
        errors.append(f"missing JSON: {path}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"JSON root must be an object: {path}")
        return {}
    return value


def resolve_inside(root: Path, relative: object, label: str, errors: list[str]) -> Path | None:
    if not isinstance(relative, str) or not relative.strip():
        errors.append(f"{label} must be a non-empty relative path")
        return None
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        errors.append(f"{label} escapes project root: {relative}")
        return None
    return candidate


def media_duration(path: Path) -> float | None:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return None
    result = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    if result.returncode != 0:
        return None
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument(
        "--public-release",
        action="store_true",
        help="Fail when a referenced source is not cleared for redistribution.",
    )
    args = parser.parse_args()

    root = args.project_root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    checked_files: set[Path] = set()

    if not root.is_dir():
        print(f"ERROR: project root does not exist: {root}")
        return 1

    sources_data = load_json(root / "inputs/sources.json", errors)
    course_data = load_json(root / "inputs/course.json", errors)
    sources = sources_data.get("sources", [])
    actions = course_data.get("actions", [])

    if not isinstance(sources, list) or not sources:
        errors.append("inputs/sources.json must contain at least one source record")
        sources = []
    if not isinstance(actions, list) or not actions:
        errors.append("inputs/course.json must contain at least one action")
        actions = []

    ledger_paths: set[str] = set()
    required_source_fields = ("id", "path", "source_url", "creator", "captured_at", "rights_status", "redistribution_status")
    for index, source in enumerate(sources):
        label = f"sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{label} must be an object")
            continue
        for field in required_source_fields:
            if not isinstance(source.get(field), str) or not source[field].strip():
                errors.append(f"{label}.{field} is required")
        rights = source.get("rights_status")
        redistribution = source.get("redistribution_status")
        if rights not in RIGHTS:
            errors.append(f"{label}.rights_status must be one of {sorted(RIGHTS)}")
        if redistribution not in REDISTRIBUTION:
            errors.append(f"{label}.redistribution_status must be one of {sorted(REDISTRIBUTION)}")
        if args.public_release and redistribution != "allowed":
            errors.append(f"{label} is not cleared for public redistribution")
        if args.public_release and rights not in {"owned", "licensed", "permission-granted"}:
            errors.append(f"{label}.rights_status is not sufficient for public release")
        elif redistribution != "allowed":
            warnings.append(f"{label} redistribution is {redistribution}; do not copy it into a public package")

        relative = source.get("path")
        if isinstance(relative, str):
            ledger_paths.add(relative.replace("\\", "/"))
        path = resolve_inside(root, relative, f"{label}.path", errors)
        if path is None:
            continue
        if not path.is_file():
            errors.append(f"missing source file: {relative}")
            continue
        checked_files.add(path)
        if path.suffix.lower() not in VIDEO_EXTENSIONS | IMAGE_EXTENSIONS:
            warnings.append(f"unusual source extension: {relative}")
        if path.suffix.lower() in VIDEO_EXTENSIONS:
            duration = media_duration(path)
            if duration is None:
                warnings.append(f"could not read duration: {relative}")
            elif duration < 3 or duration > 30:
                warnings.append(f"motion clip outside preferred 3-30s range: {relative} ({duration:.2f}s)")

    character = course_data.get("character", {})
    if not isinstance(character, dict):
        errors.append("course.character must be an object")
        character = {}
    relative = character.get("anchor_image")
    path = resolve_inside(root, relative, "character.anchor_image", errors)
    if path is not None:
        if not path.is_file():
            errors.append(f"missing character file: {relative}")
        elif path.suffix.lower() not in IMAGE_EXTENSIONS:
            errors.append(f"unsupported character image extension: {relative}")
        else:
            checked_files.add(path)

    face_relative = character.get("face_reference")
    if isinstance(face_relative, str) and face_relative.strip():
        path = resolve_inside(root, face_relative, "character.face_reference", errors)
        if path is None:
            pass
        elif not path.is_file():
            errors.append(f"missing character file: {face_relative}")
        elif path.suffix.lower() not in IMAGE_EXTENSIONS:
            errors.append(f"unsupported character image extension: {face_relative}")
        else:
            checked_files.add(path)
    else:
        warnings.append("character.face_reference is not provided; face binding remains optional")

    for index, action in enumerate(actions):
        label = f"actions[{index}]"
        if not isinstance(action, dict):
            errors.append(f"{label} must be an object")
            continue
        for field in ("reference_video", "character_image"):
            relative = action.get(field)
            path = resolve_inside(root, relative, f"{label}.{field}", errors)
            if path is None:
                continue
            if not path.is_file():
                errors.append(f"missing action asset: {relative}")
            else:
                checked_files.add(path)
        reference = action.get("reference_video")
        if isinstance(reference, str) and reference.replace("\\", "/") not in ledger_paths:
            errors.append(f"{label}.reference_video has no matching source ledger record: {reference}")

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"SUMMARY: files={len(checked_files)} warnings={len(warnings)} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
