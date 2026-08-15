---
doc_type: SOP
doc_id: SOP-010
title: Kling Motion Control browser workflow
status: active
purpose: Prepare Character Bible assets and execute one reviewed Motion Control packet in the official browser interface.
owns:
  - Character Bible prompt template
  - Motion Control packet procedure
does_not_own:
  - provider pricing or API contracts
  - course and voice acceptance
read_when:
  - preparing or executing a Kling Motion Control generation
last_reviewed: 2026-08-15
---

# Kling Motion Control browser workflow

Official workspace, verified 2026-08-15:

https://kling.ai/app/video-motion-control/new

The UI, credits, limits, and model availability may change. Recheck the official workspace before a paid batch.

## Character Bible prompt

Give the agent one owned character image plus layout references, then use:

```text
基于我的角色全身图，只参考所附模板的布局与视角方位，不复制模板人物。

请为同一个角色分别整理：
1. 转身多视角：正面、左右 45°、左右侧面、背面与后侧 45°；
2. 头部多视角：固定五官、脸型、发型与肤色；
3. T-pose / 动作姿态：固定身高、肩宽、四肢长度与身体比例；
4. 服装细节：上衣、下装、鞋袜、配饰、材质、颜色与标记位置。

保持身份、身体比例、服装、光线和摄影质感一致。不要新增品牌 Logo、文字、水印或未提供的配饰。输出前先列出每张图负责锚定的内容。
```

Prepare separate horizontal and vertical anchors. Choose the anchor whose direction and framing are closest to the reference motion.

## Packet fields

Each packet generated under `work/generation-packets/` must contain:

- action ID and title;
- reference motion path;
- character image and optional face reference;
- `match-video` or `match-image` orientation;
- duration and intended output path;
- one short positive prompt;
- action-specific QA risks;
- source-rights reminder.

## Browser steps

1. Open the official workspace and select the current Motion Control model requested by the user.
2. Upload one reference motion video. Prefer one person, full body, one action, fixed camera, clear start and finish, and roughly 3–30 seconds.
3. Upload the character image with the closest direction and target aspect ratio.
4. Choose orientation:
   - `match-video` when movement direction and complex body trajectory should follow the clip;
   - `match-image` when character framing or image-led camera behavior matters more.
5. Bind the authorized face subject when available.
6. Paste the packet prompt, review model, resolution, duration, and credit cost, then stop for user approval before the first paid generation.
7. Download the result to the packet's output path and record the provider task information in job state.

## Prompt pattern

Keep the prompt short because the inputs already divide responsibility:

- reference video: motion;
- character image and face subject: identity;
- prompt: action clarification, prop, scene, camera, and exclusions.

```text
[Action name and one critical trajectory].
[Required prop, hand, side, or stance].
Clean warm-white cyclorama studio, soft daylight from upper left.
Fixed tripod, full body visible, no zoom, no shake.
Photorealistic skin and fabric, no text, no watermark, no extra person.
```

Do not restate every joint in the prompt when the reference clip already shows it. Long prompts can compete with the motion source.

## Validate one action before batching

Choose a representative high-risk action involving turning, balance, or a prop. Generate, download, decode-check, and run human QA. Adjust the source, anchor, orientation, or prompt based on the actual failure before preparing the remaining batch.
