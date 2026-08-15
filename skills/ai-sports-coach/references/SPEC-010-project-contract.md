---
doc_type: SPEC
doc_id: SPEC-010
title: AI sports coach project contract
status: active
purpose: Define the project layout and the source and course JSON fields consumed by the helper scripts.
owns:
  - project folders
  - sources.json and course.json fields
does_not_own:
  - qualitative motion acceptance
  - Kling browser operating steps
read_when:
  - initializing, validating, or repairing a project
last_reviewed: 2026-08-15
---

# Project contract

## Layout

```text
project/
  inputs/
    character/
      anchor.png
      face-reference.png
    motions/
      action-001.mp4
    sources.json
    course.json
  work/
    generation-packets/
    job-state.json
  outputs/
    motion/
    audio/
    course/
```

Paths inside JSON are relative to the project root and use `/` separators.

## `inputs/sources.json`

Each record describes one externally sourced or self-produced input:

```json
{
  "sources": [
    {
      "id": "motion-001",
      "path": "inputs/motions/action-001.mp4",
      "source_url": "https://example.com/original-post",
      "creator": "Creator name or self",
      "captured_at": "2026-08-15",
      "rights_status": "owned",
      "redistribution_status": "allowed",
      "notes": "Single full-body movement, fixed camera"
    }
  ]
}
```

Accepted `rights_status` values are `owned`, `licensed`, `permission-granted`, `research-only`, and `unknown`. Accepted `redistribution_status` values are `allowed`, `not-allowed`, and `unknown`.

`research-only` and `unknown` inputs may be used only within the limits chosen by the user. They must not be copied into a public package.

## `inputs/course.json`

```json
{
  "project": "my-ai-coach",
  "character": {
    "name": "Coach",
    "anchor_image": "inputs/character/anchor.png",
    "face_reference": ""
  },
  "course": {
    "title": "Tennis movement session",
    "target_duration_seconds": 600
  },
  "actions": [
    {
      "id": "warmup-001",
      "title": "Lunge rotation",
      "phase": "warmup",
      "reference_video": "inputs/motions/action-001.mp4",
      "character_image": "inputs/character/anchor.png",
      "orientation": "match-video",
      "duration_seconds": 8.0,
      "prompt": "Perform one controlled lunge rotation. Fixed tripod, full body in frame.",
      "output_video": "outputs/motion/warmup-001.mp4",
      "voice_cues": [
        {
          "offset_seconds": 0.0,
          "type": "setup",
          "text": "Step forward and brace your core."
        }
      ]
    }
  ]
}
```

`face_reference` is optional; leave it empty when no authorized face subject is available. Accepted phases are `warmup`, `main`, and `cooldown`. Accepted orientations are `match-video` and `match-image`. Cue types are free text, but prefer `setup`, `technique`, `correction`, `encouragement`, `countdown`, and `transition`.

Every action ID must be unique. Cue offsets must be between zero and the action duration.

## `work/job-state.json`

The initializer creates an empty state envelope. Record provider task IDs, output paths, approval state, and failure reasons without secrets or signed URLs.
