---
name: ai-sports-coach
description: Build an AI digital-human sports coach from authorized motion-reference videos and character images, using Kling Motion Control generation packets, visual QA, course orchestration, and timed voice coaching. Use when an agent is asked to reproduce exercise or sports movements with a consistent digital character, prepare a Character Bible, organize Kling browser inputs and prompts, validate source rights and assets, turn approved clips into a warm-up/main/cooldown course, or align coaching cues to a training timeline.
---

# AI Sports Coach

Use this workflow to turn motion references into a reusable course system. Keep motion, identity, QA, course timing, and voice timing as separate contracts.

Do not treat this skill as a Kling API wrapper. It prepares deterministic packets for the official browser workflow and records results after the user performs or authorizes generation.

## Core rule

Preserve this order:

```text
source ledger -> character bible -> one-action packet -> Kling generation
-> human QA -> course timeline -> timed voice coaching
```

Never batch before one representative action passes the entire line.

## 1. Initialize and inspect

If the project has no standard layout, run:

```bash
python scripts/init_project.py --project-root <project>
```

Read `references/SPEC-010-project-contract.md`, then inspect `inputs/sources.json`, `inputs/course.json`, character images, and motion clips. Do not invent missing rights or provenance.

Run the asset preflight before preparing generation:

```bash
python scripts/preflight_assets.py --project-root <project>
```

Stop on missing files, invalid JSON, or source records without a usable URL and rights status. Warnings about clip duration or unknown redistribution rights may be resolved without changing the underlying source facts.

## 2. Build the character bible

Separate identity anchors by job:

- full-body horizontal and vertical anchors for framing;
- turnaround views for direction changes;
- head views for face consistency;
- T-pose or pose sheet for body proportions;
- outfit details for clothing, props, and materials.

Use the Character Bible prompt in `references/SOP-010-kling-motion-control.md`. Keep the user's character identity and only borrow the layout and viewing directions from any reference grids.

## 3. Prepare Motion Control packets

Populate `inputs/course.json`, then run:

```bash
python scripts/build_generation_packets.py --project-root <project>
```

Review every Markdown packet under `work/generation-packets/`. Each packet must identify one action, one reference clip, one character image, the orientation mode, a short prompt, the expected output path, and QA risks.

Read `references/SOP-010-kling-motion-control.md` before using the official Kling workspace:

https://kling.ai/app/video-motion-control/new

Treat generation as a paid external action. Obtain explicit user approval before the first paid generation in a run. Generate one representative high-risk action first; do not start the batch until it passes QA.

## 4. Run human QA

Compare the full time sequence, not one attractive frame. Check preparation, weight transfer, joint trajectory, prop behavior, face identity, outfit continuity, framing, and finish.

Read `references/TASTE-010-course-voice-qa.md` for the acceptance checklist. Reject or rerun failures; never hide a motion error behind editing.

Record approved output paths and generation notes in the project state. Preserve the human reference as a fallback when product rights allow it.

## 5. Build the course timeline

Only approved actions enter a course. Arrange them into `warmup`, `main`, and `cooldown`, add preparation steps, and calculate actual duration from events rather than headline estimates.

Keep runtime deterministic: play reviewed MP4 and audio assets instead of calling a generative model during training. Use a fallback chain such as approved AI clip -> authorized human clip -> static action card.

## 6. Add timed voice coaching

Write short cues for setup, technique, correction, encouragement, countdown, and transition. Attach each cue to an offset in the action timeline. One breath, one correction, one moment.

Read `references/TASTE-010-course-voice-qa.md` before final timing review. Require explicit voice consent before cloning or publishing a real coach's voice.

## Public distribution

Read `references/BAN-010-public-safety.md` before publishing a repository, dataset, demo, or finished course. A video being publicly viewable is not evidence that it can be redistributed or used commercially.

Do not bundle secrets, private portraits, voice samples, client outputs, signed URLs, or unknown-rights human clips.

## References

- `references/SPEC-010-project-contract.md` for folder and JSON contracts.
- `references/SOP-010-kling-motion-control.md` for Character Bible prompts, packet fields, and the verified browser workflow.
- `references/TASTE-010-course-voice-qa.md` for visual, course, and voice acceptance.
- `references/BAN-010-public-safety.md` for consent, provenance, redistribution, and public-release stops.
