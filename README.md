---
doc_type: README
doc_id: README
title: AI Sports Coach Motion Control
status: active
purpose: Explain how to turn human motion references into a consistent AI digital-human sports course.
owns:
  - public repository overview
  - installation and quickest start
does_not_own:
  - exact project schemas
  - provider terms or pricing
read_when:
  - evaluating or installing the repository
last_reviewed: 2026-08-15
---

# AI Sports Coach Motion Control

Turn sports motion references into a consistent AI digital-human coach, then assemble the approved clips into a timed course with voice guidance.

把真人动作参考变成统一形象的 AI 数字人运动教练，再把通过 QA 的动作、课程时间轴和语音指导装成一节可以直接跟练的课。

This repository packages the real Da-Yul workflow as a small Codex Skill. It does not pretend that Kling's browser workflow is an API, and it does not bundle private character assets or human reference clips with unclear redistribution rights.

## See the result first

Click a frame to open the MP4 stored in this repository.

| Motion Control output | 10:35 course orchestration | Timed voice coaching |
| --- | --- | --- |
| [![Da-Yul motion output](examples/images/dayul-motion-output.png)](examples/media/dayul-motion-output.mp4) | [![Da-Yul course orchestration](examples/images/dayul-course-orchestration.png)](examples/media/dayul-course-orchestration.mp4) | [![Da-Yul timed voice coaching](examples/images/dayul-timed-voice-coaching.png)](examples/media/dayul-timed-voice-coaching.mp4) |
| One approved action clip | 20 actions across warm-up, main training, and cooldown | 198 voice events aligned to the course timeline |

For the published human-reference / AI-output comparison, see [Da-Yul demo 04 on X](https://x.com/ZhenZhu200/status/2087578938252087616). The original human clip is linked through its public demonstration instead of copied into this repository because its source URL and redistribution permission were not preserved in the first experiment.

## The production line

```text
motion source
  -> character bible
  -> Kling 3.0 Motion Control
  -> human QA
  -> course timeline
  -> timed voice coaching
```

The skill helps an agent organize every stage, prepare one generation packet per action, and stop before paid generation until the user approves.

## Quick start

Clone the repository:

```bash
git clone https://github.com/ZHENZOO/ai-sports-coach-motion-control.git
cd ai-sports-coach-motion-control
```

Copy `skills/ai-sports-coach` into your Codex skills directory, or point your agent at the skill in this repository. Then initialize a project:

```bash
python skills/ai-sports-coach/scripts/init_project.py --project-root my-coach
```

Add your own assets under `my-coach/inputs/`, then ask your agent:

```text
Use $ai-sports-coach to inspect my project, prepare Kling Motion Control generation packets, and stop before any paid generation.
```

Run the deterministic checks:

```bash
python skills/ai-sports-coach/scripts/preflight_assets.py --project-root my-coach
python skills/ai-sports-coach/scripts/build_generation_packets.py --project-root my-coach
```

Open the official Kling Motion Control workspace only after reviewing the packets:

https://kling.ai/app/video-motion-control/new

The link and observed UI behavior were verified on 2026-08-15. Provider UI, credits, limits, and availability can change.

## What the Skill fixes

- A fixed project layout for character anchors, motion sources, output clips, course manifests, and job state.
- A source ledger that separates public availability from redistribution rights.
- Short Motion Control prompts that leave motion to the video and identity to the character image.
- A one-action end-to-end proof before batch generation.
- Visual QA for body trajectory, face, clothing, hands, rackets, balls, and framing.
- Course and voice timing contracts so the result becomes a coach-led session, not a folder of MP4 files.

## What is intentionally not here

- No Kling API wrapper: this workflow uses the official browser interface.
- No paid generation without the user's approval.
- No API keys, private portraits, cloned voices, signed URLs, or client assets.
- No promise that a public video is licensed for reuse. Record the creator, source URL, capture date, and rights status before publication.

## Repository layout

```text
skills/ai-sports-coach/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
examples/
  images/
  media/
```

## License

Code and workflow text are released under the [MIT License](LICENSE). Example media remains subject to the rights stated in [examples/media-rights.json](examples/media-rights.json).
