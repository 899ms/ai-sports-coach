---
doc_type: BAN
doc_id: BAN-010
title: Public distribution stops
status: active
purpose: Stop unauthorized source, identity, voice, secret, or client data from entering a public AI coach package.
owns:
  - public-release prohibitions
does_not_own:
  - legal advice
  - provider-specific terms
read_when:
  - publishing a repository, demo, dataset, or course
last_reviewed: 2026-08-15
---

# Public distribution stops

Stop public release when any of these are true:

- A human reference video has no preserved source URL, creator, capture date, or redistribution status.
- A real person's face or voice lacks explicit permission for the intended use.
- A clip contains a third-party logo, private setting, minor, client information, or sensitive personal data that has not been cleared.
- The package contains API keys, Authorization headers, cookies, `.env` files, signed URLs, provider job payloads with secrets, or private job state.
- The generated coach is presented as a real person without appropriate disclosure.

Publicly viewable does not mean licensed for redistribution or commercial use. Record facts in `inputs/sources.json`; do not replace unknown facts with optimistic assumptions.

For a public reusable repository, include owned or permission-cleared generated outputs and link to an already published comparison when the original reference cannot be redistributed. Keep user-supplied assets outside the skill package.

This file is an operational safety boundary, not legal advice. Verify applicable rights, provider terms, biometric rules, and platform disclosure requirements before commercial publication.
