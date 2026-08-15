#!/usr/bin/env python3
"""Create a non-destructive AI sports coach project skeleton."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DIRECTORIES = (
    "inputs/character",
    "inputs/motions",
    "work/generation-packets",
    "outputs/motion",
    "outputs/audio",
    "outputs/course",
)


def write_json_if_missing(path: Path, payload: dict) -> str:
    if path.exists():
        return "kept"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return "created"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    args = parser.parse_args()

    root = args.project_root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    for relative in DIRECTORIES:
        (root / relative).mkdir(parents=True, exist_ok=True)

    files = {
        root / "inputs/sources.json": {
            "sources": []
        },
        root / "inputs/course.json": {
            "project": root.name,
            "character": {
                "name": "",
                "anchor_image": "inputs/character/anchor.png",
                "face_reference": ""
            },
            "course": {
                "title": "",
                "target_duration_seconds": None
            },
            "actions": []
        },
        root / "work/job-state.json": {
            "project": root.name,
            "status": "draft",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "approved_action_ids": [],
            "generations": []
        },
    }

    for path, payload in files.items():
        status = write_json_if_missing(path, payload)
        print(f"[{status}] {path.relative_to(root)}")

    print(f"[ready] {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
