#!/usr/bin/env python3
"""Validate a course manifest and render one Kling Motion Control packet per action."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ACTION_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
PHASES = {"warmup", "main", "cooldown"}
ORIENTATIONS = {"match-video", "match-image"}
OFFICIAL_WORKSPACE = "https://kling.ai/app/video-motion-control/new"


def load_object(path: Path, errors: list[str]) -> dict[str, Any]:
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


def require_text(item: dict[str, Any], field: str, label: str, errors: list[str]) -> str:
    value = item.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}.{field} must be non-empty text")
        return ""
    return value.strip()


def validate_action(action: object, index: int, seen: set[str], errors: list[str]) -> dict[str, Any] | None:
    label = f"actions[{index}]"
    if not isinstance(action, dict):
        errors.append(f"{label} must be an object")
        return None

    action_id = require_text(action, "id", label, errors)
    require_text(action, "title", label, errors)
    require_text(action, "reference_video", label, errors)
    require_text(action, "character_image", label, errors)
    require_text(action, "prompt", label, errors)
    require_text(action, "output_video", label, errors)

    if action_id and not ACTION_ID.fullmatch(action_id):
        errors.append(f"{label}.id must use lowercase letters, digits, and hyphens")
    if action_id in seen:
        errors.append(f"duplicate action id: {action_id}")
    seen.add(action_id)

    phase = action.get("phase")
    if phase not in PHASES:
        errors.append(f"{label}.phase must be one of {sorted(PHASES)}")
    orientation = action.get("orientation")
    if orientation not in ORIENTATIONS:
        errors.append(f"{label}.orientation must be one of {sorted(ORIENTATIONS)}")

    duration = action.get("duration_seconds")
    if not isinstance(duration, (int, float)) or isinstance(duration, bool) or duration <= 0:
        errors.append(f"{label}.duration_seconds must be a positive number")
        duration = 0

    cues = action.get("voice_cues", [])
    if not isinstance(cues, list):
        errors.append(f"{label}.voice_cues must be a list")
        cues = []
    for cue_index, cue in enumerate(cues):
        cue_label = f"{label}.voice_cues[{cue_index}]"
        if not isinstance(cue, dict):
            errors.append(f"{cue_label} must be an object")
            continue
        offset = cue.get("offset_seconds")
        if not isinstance(offset, (int, float)) or isinstance(offset, bool):
            errors.append(f"{cue_label}.offset_seconds must be a number")
        elif offset < 0 or offset > duration:
            errors.append(f"{cue_label}.offset_seconds must be between 0 and {duration}")
        require_text(cue, "type", cue_label, errors)
        require_text(cue, "text", cue_label, errors)

    return action


def packet_markdown(action: dict[str, Any], character: dict[str, Any]) -> str:
    cues = action.get("voice_cues", [])
    cue_lines = [
        f"- `{cue['offset_seconds']}s` · **{cue['type']}** · {cue['text']}"
        for cue in cues
    ] or ["- No voice cues defined yet."]
    face_reference = character.get("face_reference") or "Not provided"
    return "\n".join(
        [
            f"# {action['id']} · {action['title']}",
            "",
            f"Kling workspace: {OFFICIAL_WORKSPACE}",
            "",
            "## Inputs",
            "",
            f"- Phase: `{action['phase']}`",
            f"- Reference motion: `{action['reference_video']}`",
            f"- Character image: `{action['character_image']}`",
            f"- Face reference: `{face_reference}`",
            f"- Orientation: `{action['orientation']}`",
            f"- Reference duration: `{action['duration_seconds']}s`",
            f"- Expected output: `{action['output_video']}`",
            "",
            "## Prompt",
            "",
            action["prompt"].strip(),
            "",
            "## Voice cues",
            "",
            *cue_lines,
            "",
            "## Human QA",
            "",
            "- [ ] Preparation, weight transfer, key trajectory, and finish match the reference.",
            "- [ ] Face identity, body proportions, and outfit stay consistent.",
            "- [ ] Hands, feet, and required props remain usable.",
            "- [ ] Full body and critical props stay in frame.",
            "- [ ] Source ledger and intended use have been reviewed.",
            "- [ ] User approved the first paid generation in this run.",
            "",
        ]
    )


def write_text(path: Path, text: str, overwrite: bool, errors: list[str]) -> None:
    if path.exists() and not overwrite:
        errors.append(f"output exists; rerun with --overwrite to replace it: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--course", type=Path, help="Defaults to <project>/inputs/course.json")
    parser.add_argument("--out-dir", type=Path, help="Defaults to <project>/work/generation-packets")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    root = args.project_root.resolve()
    course_path = (args.course or root / "inputs/course.json").resolve()
    out_dir = (args.out_dir or root / "work/generation-packets").resolve()
    errors: list[str] = []
    data = load_object(course_path, errors)

    project = data.get("project")
    if not isinstance(project, str) or not project.strip():
        errors.append("project must be non-empty text")
    character = data.get("character")
    if not isinstance(character, dict):
        errors.append("character must be an object")
        character = {}
    require_text(character, "name", "character", errors)
    require_text(character, "anchor_image", "character", errors)

    actions = data.get("actions")
    if not isinstance(actions, list) or not actions:
        errors.append("actions must contain at least one action")
        actions = []

    seen: set[str] = set()
    valid_actions: list[dict[str, Any]] = []
    for index, action in enumerate(actions):
        validated = validate_action(action, index, seen, errors)
        if validated is not None:
            valid_actions.append(validated)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"SUMMARY: packets=0 errors={len(errors)}")
        return 1

    index_items: list[dict[str, str]] = []
    for action in valid_actions:
        packet_path = out_dir / f"{action['id']}.md"
        index_items.append(
            {
                "id": action["id"],
                "phase": action["phase"],
                "packet": packet_path.name,
                "output_video": action["output_video"],
            }
        )

    index_path = out_dir / "index.json"
    planned_outputs = [out_dir / f"{action['id']}.md" for action in valid_actions] + [index_path]
    if not args.overwrite:
        conflicts = [path for path in planned_outputs if path.exists()]
        if conflicts:
            for path in conflicts:
                print(f"ERROR: output exists; rerun with --overwrite to replace it: {path}")
            print(f"SUMMARY: packets=0 errors={len(conflicts)}")
            return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    write_errors: list[str] = []
    for action in valid_actions:
        packet_path = out_dir / f"{action['id']}.md"
        write_text(packet_path, packet_markdown(action, character), args.overwrite, write_errors)

    index_text = json.dumps(
        {"project": project, "workspace": OFFICIAL_WORKSPACE, "actions": index_items},
        ensure_ascii=False,
        indent=2,
    ) + "\n"
    write_text(index_path, index_text, args.overwrite, write_errors)

    if write_errors:
        for error in write_errors:
            print(f"ERROR: {error}")
        print(f"SUMMARY: packets=0 errors={len(write_errors)}")
        return 1

    print(f"SUMMARY: packets={len(valid_actions)} out={out_dir} errors=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
