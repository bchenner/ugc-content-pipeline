# BRoll Tab Pattern

Each B-roll clip has start frame, end frame, and video generation.

## Wiring Diagram (per clip)

```
── START FRAME ──
[Prompt: start] + [ReferenceImage: product] → [NanobananaAPI] → [Approval: start]
                                                                       │
                                                          ┌────────────┤
                                                          ↓            ↓
── END FRAME ──                                    (to Veo3     (to end frame
[Prompt: end] + [ReferenceImage: product] ──→ [NanobananaAPI] → [Approval: end]  start frame)   NanobananaAPI
                + Approval start output ────→      ↑                   │           as reference)
                                                                       ↓
── VIDEO ──                                                     (to Veo3
[Prompt: video] + Approval start (start frame) + Approval end (end frame) → [Veo3] → [Approval(video)]
                                                                               end frame)
```

**Critical**: The end frame NanobananaAPI receives the start frame Approval output as an additional image reference input. This maintains visual consistency between start and end frames.

**B-roll Veo3** uses `mode: "frames-to-video"` with BOTH `start frame` and `end frame` connected. The Veo3 output connects to a video Approval node for review.

## Reference Images

- Each B-roll clip's start frame NanobananaAPI gets 1 reference image (product only)
- The end frame NanobananaAPI gets 2-3: product reference + start frame Approval output (as consistency reference)
- One ReferenceImage node per connection — if the same product image feeds both start and end frame NanobananaAPIs, use separate ReferenceImage nodes for each (or a single one with multiple output links)

## Input Required

- `brolls[]` — Array of B-roll clips, each with:
  - `startPrompt` — Start frame image prompt JSON (stringified)
  - `endPrompt` — End frame image prompt JSON (stringified)
  - `videoPrompt` — Video prompt JSON (stringified)
  - `duration` — `"4"` typically (string)
  - `requires` — Reference images for start frame (e.g., `["product image"]`)

## Construction (per B-roll clip)

**Step 1: Start frame**
- 1 ReferenceImage node (product) — shared between start and end frame NanobananaAPIs
- 1 Prompt node (start frame text)
- 1 NanobananaAPI node (imageCount = number of reference images, typically 1)
- 1 Approval node (start)

Wire: Prompt → NanobananaAPI slot 0, ReferenceImage → NanobananaAPI slot 1, NanobananaAPI → Approval

**Step 2: End frame**
- 1 Prompt node (end frame text)
- 1 NanobananaAPI node (imageCount = number of image inputs: reference image + start Approval output, typically 2-3)
- 1 Approval node (end)

Wire: Prompt → NanobananaAPI slot 0, ReferenceImage → NanobananaAPI slot 1, Start Approval output → NanobananaAPI slot 2, NanobananaAPI → Approval

**Step 3: Video**
- 1 Prompt node (video prompt)
- 1 Veo3 node (mode: "frames-to-video", durationSeconds)
- 1 Approval node (video review)

Wire: Prompt → Veo3 slot 0, Start Approval output → Veo3 slot 1 (start frame), End Approval output → Veo3 slot 2 (end frame), Veo3 → video Approval

## End Frame Reference Chaining

The start frame's Approval output serves double duty:
1. Goes to Veo3 as `start frame` (slot 1)
2. Goes to end frame NanobananaAPI as a reference image input (for visual consistency)

The start Approval's output `links` array will have 2 link IDs — one to Veo3 slot 1, one to end NanobananaAPI slot 2.

## B-Roll Without End Frames

If a B-roll clip only has a start frame (no end frame prompt), skip Step 2 and wire the start Approval directly to the Veo3 start frame slot. Leave Veo3 end frame as null.

## Layout

Each B-roll clip occupies a vertical band. Clips stack vertically with ~1200px spacing.

```
Per-clip X positions (approximate):
  ReferenceImages:    -1200 to -820
  Prompts (start):     -960 to -660
  Prompts (end):       -670 to -530
  NanobananaAPI start:  -340 to 150
  NanobananaAPI end:     130 to 360
  Approval start:        140 to 780
  Approval end:          760 to 940
  Prompt (video):        970 to 1190
  Veo3:                 1440 to 1620

Y offset per clip: clipBaseY + clipIndex * 1200
```
