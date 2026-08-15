---
doc_type: TASTE
doc_id: TASTE-010
title: Motion, course, and voice quality
status: active
purpose: Define what an acceptable AI sports coaching clip and timed course feel like.
owns:
  - visual motion quality
  - course flow and voice timing judgment
does_not_own:
  - project JSON fields
  - publishing permission
read_when:
  - reviewing a generated clip, course, or coaching timeline
last_reviewed: 2026-08-15
---

# Course and voice QA

## Motion QA

Review the complete sequence beside the reference. Accept only when:

- preparation, weight transfer, key trajectory, and finish remain recognizable;
- the face stays the same person through turns and occlusion;
- body proportions and outfit do not jump between frames;
- hands, feet, rackets, balls, bands, or exercise balls do not break the action;
- the full body and critical prop remain in frame;
- the background and camera remain stable enough for a course library.

A beautiful still frame does not compensate for a wrong trajectory. If a failure affects coaching safety or technique, reject the clip.

## Course QA

A course is not a playlist. It should:

- begin with preparation and warm-up, build into the main skill, then cool down;
- give the user enough transition time to change stance, side, or prop;
- avoid unexplained repetition and abrupt difficulty jumps;
- report real duration from the timeline;
- use only approved action assets;
- preserve a deterministic fallback when the preferred clip is missing.

## Voice cue types

- `setup`: stance, starting position, or equipment.
- `technique`: one current movement instruction.
- `correction`: one likely error and the smallest fix.
- `encouragement`: specific feedback, not generic noise.
- `countdown`: remaining time or repetitions.
- `transition`: next side, action, rest, or phase.

Write one breath per cue. Start with a verb when possible. Tell the user what to do at this second, not the whole theory of the movement.

## Timing QA

- Put setup before the movement needs to happen.
- Do not stack two cues that cannot be spoken in the available interval.
- Keep the most important correction audible during the relevant motion.
- Leave silence when the user needs concentration or recovery.
- End countdown and transition cues before the next visual state begins.
- Edit one cue independently instead of regenerating the motion clip.

The target experience is: the visual shows the action, while the voice carries the user through the session.
