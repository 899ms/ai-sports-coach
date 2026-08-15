---
doc_type: AGENTS
doc_id: AGENTS
title: AI Sports Coach Motion Control agent entry
status: active
purpose: Route agents to the repository skill and define public-safety boundaries.
owns:
  - repository agent entry and hard boundaries
  - command routing
does_not_own:
  - detailed production workflow
  - project schemas and prompt examples
read_when:
  - any agent starts work in this repository
last_reviewed: 2026-08-15
---

# Agent entry

Read `skills/ai-sports-coach/SKILL.md` before building or reviewing an AI sports coach project. Load only the referenced resource needed for the current stage.

Hard boundaries:

- Treat Kling generation as a paid external action. Stop for explicit user approval before the first paid generation in a run.
- Do not claim browser-only behavior is an API integration.
- Do not commit secrets, private character assets, cloned voices, client media, temporary URLs, or job state from real projects.
- Do not publish a human reference clip unless its source ledger marks redistribution as allowed.
- Prove one representative action end to end before preparing a batch.

Primary commands:

```text
python skills/ai-sports-coach/scripts/init_project.py --project-root <project>
python skills/ai-sports-coach/scripts/preflight_assets.py --project-root <project>
python skills/ai-sports-coach/scripts/build_generation_packets.py --project-root <project>
```
