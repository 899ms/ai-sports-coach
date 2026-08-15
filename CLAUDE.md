---
doc_type: CLAUDE
doc_id: CLAUDE
title: Claude adapter for AI Sports Coach Motion Control
status: active
purpose: Route Claude-compatible sessions to the shared repository instructions.
owns:
  - Claude-specific entry routing
does_not_own:
  - shared workflow or safety policy
read_when:
  - Claude starts work in this repository
last_reviewed: 2026-08-15
---

# Claude adapter

Read `AGENTS.md`, then follow `skills/ai-sports-coach/SKILL.md`. Translate file, shell, browser, and user-approval steps to the tools available in the current runtime without changing the workflow gates.
