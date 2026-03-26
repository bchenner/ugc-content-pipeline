# Mainbody Tab Pattern

The Mainbody tab contains **all speaking content**: scene videos AND hook variations. Hooks share the same image generation group as scenes — they use the same Founder Approval as their start frame reference.

## Image Generation Groups

One per distinct reference image:

```
[Prompt: image prompt] ──────────────→ [NanobananaAPI] ──→ [Approval(image)]
[ReferenceImage: avatar] ────────────→      ↑                     │
[ReferenceImage: product] ───────────→      ↑                     │
                                                                  ↓
                                            ┌──── Approval fans out ────┐
                                            ↓          ↓                ↓
                                    [Veo3 S1]    [Veo3 S2]       [Veo3 S5]
                                       ↑    │       ↑    │          ↑    │
                                [Prompt S1]  ↓  [Prompt S2] ↓  [Prompt S5] ↓
                                      [Approval] [Approval]    [Approval]
                                       (video)    (video)       (video)
```

**Key**: One image Approval output connects to multiple Veo3 `start frame` inputs. Each Veo3 output connects to its own video Approval node.

## Two-Pass Image Generation

When `generation_mode: "two-pass"`:

```
── PASS 1: SETTING ──
[Prompt: setting] + [ReferenceImage: product] → [NanobananaAPI] → [Approval: setting]
                                                                        │
── PASS 2: CHARACTER ──                                                 ↓ (as reference)
[Prompt: character] + [ReferenceImage: avatar] → [NanobananaAPI] → [Approval: final]
                    + Approval setting output →       ↑                  │
                    + [ReferenceImage: product] →      ↑                  ↓
                                                              ┌── fans out ──┐
                                                              ↓              ↓
                                                        [Veo3 S1]     [Veo3 S2] ...
```

The Pass 2 NanobananaAPI receives the setting Approval output as an additional image reference input. The final Approval output fans out to Veo3 nodes as usual.

## Hooks

Hooks share the same image generation group as scenes — the Founder Approval fans out to both scene and hook Veo3 nodes. Hooks are positioned below scenes in the same Mainbody tab. No separate hook image gen group.

**Veo3 speaking scenes and hooks** use `mode: "frames-to-video"` with only the `start frame` slot connected. The `end frame` slot is `null`.

## Reference Images

- One image gen group for all speaking content (scenes + hooks)
- NanobananaAPI typically gets 2 reference images (avatar + product)
- The single Founder Approval fans out to all Veo3 nodes
- One ReferenceImage node per connection — if the same product image feeds both start and end frame NanobananaAPIs, use separate ReferenceImage nodes for each (or a single one with multiple output links)
- **All ReferenceImage nodes must have descriptive labels** — title and variableName specify what image the user needs to upload

## Input Required

- `imageGroups[]` — Array of image generation groups, each with:
  - `prompt` — Full image prompt JSON (stringified)
  - `requires` — Reference images needed (e.g., `["avatar image", "product image"]`)
  - `sceneNumbers` — Which scenes/hooks use this reference (e.g., `[1, 2, 5]` or `["hook1", "hook2"]`)
- `scenes[]` — Array of speaking scenes, each with:
  - `number` — Scene number
  - `prompt` — Full Veo video prompt JSON (stringified)
  - `duration` — Always `"8"` (only supported duration for frames-to-video)
  - `imageGroup` — Which image group this scene references (index into imageGroups)
- `hooks[]` — (optional) Array of hook variations, each with:
  - `number` — Hook number
  - `prompt` — Full Veo video prompt JSON (stringified)
  - `imageGroup` — Which image group this hook references

## Construction

**Step 1: Image generation groups**

For each image group, create:
- 1 Prompt node (image prompt text)
- N ReferenceImage nodes (one per required asset)
- 1 NanobananaAPI node (imageCount = number of reference images)
- 1 Approval node (image review)

Wire: Prompt → NanobananaAPI slot 0, ReferenceImages → NanobananaAPI slots 1+, NanobananaAPI → Approval

**Step 2: Scene video generation**

For each scene, create:
- 1 Prompt node (video prompt text)
- 1 Veo3 node (mode: "frames-to-video", durationSeconds per scene)
- 1 Approval node (video review)

Wire: Prompt → Veo3 slot 0, correct image Approval output → Veo3 slot 1 (start frame), Veo3 → video Approval

**Step 2b: Hook video generation** (if hooks exist)

Same pattern as scenes, using the **same image generation group** as scenes (same Approval fan-out). Hooks are positioned below scenes in the same Mainbody tab.

**Step 3: Fan-out connections**

Each Approval node's output `links` array accumulates link IDs — one per Veo3 node that uses this image group as its start frame reference.

## Layout

Image generation groups are positioned left, scene videos to the right.

```
X positions (approximate):
  ReferenceImages:  -2200 to -1800
  Prompts (image):  -2000 to -1860
  NanobananaAPI:    -1360 to -1230
  Approval:          -900 to -810

  Prompts (video):   -265 to -165
  Veo3:               200 to 700

Y spacing: ~400-500px between scene rows
```

Image gen groups stack vertically. Scene Veo3 nodes stack vertically on the right side, with their corresponding Prompt nodes to their left.
