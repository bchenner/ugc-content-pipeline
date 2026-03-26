# PatchWork Import Agent

Takes UGC pipeline outputs (scripts, image prompts, video prompts) and generates ready-to-import `.nbflow` project files for PatchWork. You construct valid LiteGraph graph JSON with all nodes pre-filled and wired together.

---

## What You Do

1. Receive pipeline outputs from the user (image prompt text, scene-by-scene video prompts, hook prompts, B-roll prompts)
2. Build a valid `.nbflow` project file with one or more tabs (tab structure varies by project type)
3. Save as `.nbflow` file to `output/`
4. Tell the user the file path to import in PatchWork (Home screen > Import Project)

---

## File Structure

PatchWork uses `"ducted-project"` format with a **tabs array**. Each tab is an independent workflow with its own graph.

```json
{
  "format": "ducted-project",
  "version": "0.8.0",
  "name": "Project Name",
  "tabs": [
    {
      "name": "Tab Name",
      "graphData": {
        "last_node_id": 0,
        "last_link_id": 0,
        "nodes": [],
        "links": [],
        "groups": [],
        "config": {},
        "extra": { "nodeGroups": {} },
        "version": 0.4
      },
      "canvasState": { "offsetX": 0, "offsetY": 0, "scale": 0.5 },
      "drawingData": [],
      "saveCounter": 0
    }
  ]
}
```

**Tab structure is flexible** — use as many tabs as the project needs:
- **Main body videos**: One tab (e.g., "Mainbody") with image gen groups + speaking scene videos
- **Prehooks**: One tab per day (e.g., "Day 1", "Day 2") with prehook workflows, or one tab per prehook
- **Testing**: A dedicated tab with simplified chains for quick prompt testing
- **B-roll**: Handled externally via Sora 2 (not in PatchWork)

Node IDs and link IDs are scoped **per tab** — each tab's graphData tracks its own `last_node_id` and `last_link_id` independently.

### Groups

Groups are visual rectangles that label sections within a tab. They have no functional effect but help organize complex tabs with multiple workflows.

```json
{
  "title": "P1 — 3AM Wake-Up (Selfie)",
  "bounding": [x, y, width, height],
  "color": "#444",
  "font_size": 28
}
```

Add groups to `graphData.groups[]`. Calculate `bounding` from the min/max positions of nodes in the group plus padding.

---

## Node Chain

The pipeline uses **6 node types** in production workflows:

```
Prompt + ReferenceImage(s) → NanobananaAPI → Approval(image) → Veo3 → Approval(video)
```

**Every Veo3 node connects to a downstream Approval node** for video review. This is standard for all Veo3 outputs (scenes, hooks, and B-roll).

A 6th node type, **Media**, acts as a standalone reference/approval hybrid for feeding approved images as references.

There are no OutputPreview or AddToEditor nodes in the pipeline.

### Mainbody Tab Pattern

The Mainbody tab contains **all speaking content**: scene videos AND hook variations. Hooks share the same image generation group as scenes — they use the same Founder Approval as their start frame reference.

**Image generation groups** — one per distinct reference image:

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

**Two-pass image generation** (when `generation_mode: "two-pass"`): <!-- date: 2026-03 -->

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

The Pass 2 NanobananaAPI receives the setting Approval output as an additional image reference input (like B-roll end frames receive start frame Approval). The final Approval output fans out to Veo3 nodes as usual.

**Hooks** share the same image generation group as scenes — the Founder Approval fans out to both scene and hook Veo3 nodes. Hooks are positioned below scenes in the same Mainbody tab. No separate hook image gen group.

**Veo3 speaking scenes and hooks** use `mode: "frames-to-video"` with only the `start frame` slot connected. The `end frame` slot is `null`.

### BRoll Tab Pattern (per clip)

Each B-roll clip has start frame, end frame, and video generation:

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

### Reference Images

- **Mainbody**: One image gen group for all speaking content (scenes + hooks). NanobananaAPI typically gets 2 reference images (avatar + product). The single Founder Approval fans out to all Veo3 nodes.
- **BRoll**: Each B-roll clip's start frame NanobananaAPI gets 1 reference image (product only). The end frame NanobananaAPI gets 2-3: product reference + start frame Approval output (as consistency reference)
- One ReferenceImage node per connection — if the same product image feeds both start and end frame NanobananaAPIs, use separate ReferenceImage nodes for each (or a single one with multiple output links)
- **All ReferenceImage nodes must have descriptive labels** — title and variableName specify what image the user needs to upload (e.g., `"Avatar Image — upload founder/model photo"`)

---

## Node Type Reference

### Required Fields on ALL Nodes

Every node must include these fields:

```json
{
  "id": 1,
  "type": "nanobanana/NodeType",
  "pos": [100, 100],
  "size": [340, 220],
  "flags": { "hide_title": true },
  "order": 0,
  "mode": 0,
  "color": "#333",
  "bgcolor": "#1a1a1a",
  "title": "Display Title",
  "properties": { ... },
  "inputs": [],
  "outputs": []
}
```

- `order` — Execution order (integer, 0-indexed). Set sequentially across all nodes in a tab.
- `mode` — Always `0` for active nodes
- `color` — Always `"#333"`
- `bgcolor` — Always `"#1a1a1a"`
- `flags` — Always `{ "hide_title": true }`
- **All input/output slots** must include `"label": " "` (single space) alongside name, type, link/links, and slot_index

### 1. Prompt (`nanobanana/Prompt`)

Text input node. No inputs, one output.

| Property | Type | Default | Notes |
|----------|------|---------|-------|
| `text` | string | `""` | The prompt content (full JSON stringified) |
| `variableName` | string | `"Prompt {N}"` | Display name |
| `batchMode` | bool | `false` | |
| `templateMode` | bool | `false` | |
| `dynamicMode` | bool | `false` | |
| `dynamicRows` | array | `[""]` | |
| `_disabled` | bool | `false` | |
| `_advancedOpen` | bool | `false` | |
| `_spawnNum` | number | auto | Unique counter per node type |

**Outputs**: `[{ "name": "prompt", "type": "string", "links": [], "slot_index": 0, "label": " " }]`
**Size**: `[400, 300]`

#### Dynamic Mode

When `dynamicMode: true`, the Prompt node shows a dropdown of pre-defined rows. The user picks one row at a time. Used for account-specific content (different characters, dialogue per account).

```json
{
  "dynamicMode": true,
  "dynamicRows": [
    "[EN-1] Black male naturopath",
    "[EN-2] Brandon, Korean doctor",
    "[ES-1] Holistic Mom"
  ]
}
```

#### Template Mode

When `templateMode: true`, the Prompt node accepts input variables from upstream nodes. Variables appear as `{variableName}` in the text and are filled at runtime.

```json
{
  "templateMode": true,
  "text": "Portrait of {character} in a kitchen. They say: \"{dialogue}\""
}
```

Template inputs are defined in the node's `inputs` array — one slot per variable:
```json
"inputs": [
  { "name": "character", "type": "string", "link": null, "label": " " },
  { "name": "dialogue", "type": "string", "link": null, "label": " " }
]
```

**Dynamic → Template pattern**: A Dynamic node feeds a selected row into a Template node's variable input. This allows per-account content swapping without rebuilding workflows.

### 2. ReferenceImage (`nanobanana/ReferenceImage`)

Image source node. No inputs, one output.

| Property | Type | Default | Notes |
|----------|------|---------|-------|
| `imageData` | string/null | `null` | R2/HTTP URL or null (user loads manually) |
| `filename` | string | `""` | Original filename |
| `width` | number | `0` | Image width |
| `height` | number | `0` | Image height |
| `variableName` | string | `"Reference Image {N}"` | Display name |
| `batchMode` | bool | `false` | |
| `batchImages` | array | `[]` | |
| `batchExecMode` | string | `"drip"` | |
| `_disabled` | bool | `false` | |
| `_imageAssetId` | string/null | `null` | |
| `_batchAssetIds` | array | `[]` | |
| `_advancedOpen` | bool | `false` | |
| `_spawnNum` | number | auto | |
| `mode` | string | `"reference"` | Always `"reference"` |
| `lastData` | any | `null` | |
| `_lastApprovedData` | any | `null` | |
| `_autoRefineEnabled` | bool | `false` | |
| `_savedApprovalImages` | array | `[]` | |
| `_savedApprovalVideos` | array | `[]` | |
| `_savedApprovalIndex` | number | `0` | |
| `_savedApprovalVideoIndex` | number | `0` | |
| `_savedCurrentMediaType` | null | `null` | |
| `galleryImages` | array | `[]` | |
| `galleryVideos` | array | `[]` | |
| `galleryIndex` | number | `0` | |
| `_savedGalleryImages` | array | `[]` | |
| `_savedGalleryVideos` | array | `[]` | |
| `_savedGalleryIndex` | number | `0` | |
| `imageWidth` | number | `0` | |
| `imageHeight` | number | `0` | |
| `_pages` | array | `[]` | |
| `_pageIndex` | number | `0` | |
| `_savedRowMapping` | object | `{}` | |

**Inputs**: `[{ "name": "input", "type": "*", "link": null }]`
**Outputs**: `[{ "name": "image", "type": "image", "links": [], "slot_index": 0, "label": " " }]`
**Size**: `[320, 360]` (may grow to `[320, 597.5]` when image is loaded)

**Image data**: Set `imageData` to an R2 URL or HTTP URL if available. For local files, set to `null` — user loads the image manually after import. Do NOT embed base64 strings.

**Descriptive labels**: The `title` and `variableName` must describe what image the user needs to upload. Format: `"{Asset Type} — upload {specific description}"`. Examples:
- `"Avatar Image — upload founder/model photo"`
- `"Product Image — upload Silk Glide Pro photo"`
- `"Product Image — upload product on white background"`

This tells the user exactly what to load into each ReferenceImage node after import.

### 3. NanobananaAPI (`nanobanana/NanobananaAPI`)

Image generation via Gemini. Prompt input + optional image inputs.

| Property | Type | Default | Notes |
|----------|------|---------|-------|
| `model` | string | `"gemini-3.1-flash-image-preview"` | Gemini model |
| `aspectRatio` | string | `"9:16"` | |
| `resolution` | string | `"1K"` | 512px, 1K, 2K, 4K |
| `timeout` | number | `300000` | ms |
| `imageCount` | number | `1` | Number of connected image inputs |
| `outputCount` | number | `4` | Number of images to generate per run (default 4, use 2 for testing) |
| `repeatCount` | number | `1` | |
| `inputVariable` | string | `""` | |
| `_disabled` | bool | `false` | |
| `_savedImages` | array | `[]` | |
| `_savedPreviewIndex` | number | `0` | |
| `_advancedOpen` | bool | `false` | |
| `_previewOpen` | bool | `false` | |
| `_pinned` | bool | `false` | |
| `_spawnNum` | number | auto | |

**Inputs**: Slot 0 is always prompt, slots 1+ are image inputs:
```json
[
  { "name": "prompt", "type": "string", "link": null, "label": " " },
  { "name": "image 1", "type": "image", "link": null, "label": " " }
]
```
Add more image slots as needed: `{ "name": "image 2", "type": "image", "link": null }`, etc.

**Outputs**: `[{ "name": "images", "type": "image", "links": [], "slot_index": 0, "label": " " }]`

**Size**: Varies by `imageCount`:
- 1 image input: `[360, 294]`
- 2 image inputs: `[360, 561]`
- 3 image inputs: `[360, 651]`

**`imageCount`** must match the number of image input slots defined in `inputs`.

### 4. Approval (`nanobanana/Approval`)

Manual review gate. Pauses workflow until user approves the generated image/video.

| Property | Type | Default | Notes |
|----------|------|---------|-------|
| `variableName` | string | `"Approval {N}"` | Display name |
| `mode` | string | `"approve"` | Always `"approve"` |
| `lastData` | any | `null` | |
| `_lastApprovedData` | any | `null` | |
| `_autoRefineEnabled` | bool | `false` | |
| `_disabled` | bool | `false` | |
| `_savedApprovalImages` | array | `[]` | |
| `_savedApprovalVideos` | array | `[]` | |
| `_savedApprovalIndex` | number | `0` | |
| `_savedApprovalVideoIndex` | number | `0` | |
| `_advancedOpen` | bool | `false` | |
| `_spawnNum` | number | auto | |
| `_savedCurrentMediaType` | string | `"image"` | |
| `galleryImages` | array | `[]` | Gallery storage |
| `galleryVideos` | array | `[]` | Gallery storage |
| `galleryIndex` | number | `0` | |
| `_savedGalleryImages` | array | `[]` | |
| `_savedGalleryVideos` | array | `[]` | |
| `_savedGalleryIndex` | number | `0` | |
| `imageData` | null | `null` | |
| `filename` | string | `""` | |
| `imageWidth` | number | `0` | |
| `imageHeight` | number | `0` | |
| `_imageAssetId` | null | `null` | |
| `_pages` | array | `[]` | Page navigation |
| `_pageIndex` | number | `0` | |
| `_savedRowMapping` | object | `{}` | |

**Inputs**: `[{ "name": "input", "type": "*", "link": null, "label": " " }]`
**Outputs**: `[{ "name": "output", "type": "<context>", "links": [], "slot_index": 0, "label": " " }]`
**Size**: `[360, 400]`

**Important**: Input type is `"*"` (wildcard). Output type is **context-dependent**: `"image"` when downstream of NanobananaAPI (image approval), `"video"` when downstream of Veo3 (video approval).

### 5. Veo3 (`nanobanana/Veo3`)

Video generation via Veo 3.1.

| Property | Type | Default | Notes |
|----------|------|---------|-------|
| `model` | string | `"veo-3.1-fast-generate-preview"` | |
| `mode` | string | `"frames-to-video"` | Always "frames-to-video" |
| `durationSeconds` | string | `"8"` | Always `"8"` — only supported duration for frames-to-video mode (STRING not number) |
| `aspectRatio` | string | `"9:16"` | |
| `resolution` | string | `"720p"` | 720p, 1080p, 4k |
| `negativePrompt` | string | `""` | |
| `sampleCount` | number | `1` | |
| `seed` | number | `0` | |
| `timeout` | number | `600000` | ms |
| `imageCount` | number | `1` | Always 1 |
| `outputCount` | number | `4` | Number of videos to generate per run (default 4, use 2 for testing) |
| `repeatCount` | number | `1` | |
| `inputVariable` | string | `""` | |
| `_disabled` | bool | `false` | |
| `_savedVideoUrl` | null | `null` | |
| `_savedVideos` | array | `[]` | |
| `_savedGalleryIndex` | number | `0` | |
| `_savedGallerySlots` | array | `[]` | |
| `_advancedOpen` | bool | `false` | |
| `_previewOpen` | bool | `true` | Note: true by default |
| `_pinned` | bool | `false` | |
| `veoModel` | string | `"fast"` | Shorthand model selector. `"fast"` for production, `"relax"` for testing |
| `_spawnNum` | number | auto | |

**Inputs (frames-to-video)**:
```json
[
  { "name": "prompt", "type": "string", "link": null, "label": " " },
  { "name": "start frame", "type": "image", "link": null, "label": " " },
  { "name": "end frame", "type": "image", "link": null, "label": " " }
]
```

**Outputs**: `[{ "name": "video", "type": "video", "links": [], "slot_index": 0, "label": " " }]`
**Size**: `[380, 409]`

**Speaking scenes**: Connect `start frame` only (from Approval output). Leave `end frame` link as `null`.
**B-roll clips**: Connect both `start frame` (from start Approval) and `end frame` (from end Approval).

### 6. Media (`nanobanana/Media`)

Standalone reference/approval hybrid. Used to feed approved images as references into downstream nodes (e.g., providing an already-approved image to a NanobananaAPI or Veo3 without re-generating it).

| Property | Type | Default | Notes |
|----------|------|---------|-------|
| `mode` | string | `"reference"` | Always `"reference"` |
| `variableName` | string | `"Media {N}"` | Display name |
| `_advancedOpen` | bool | `false` | |
| `_disabled` | bool | `false` | |
| `_spawnNum` | number | auto | |
| `lastData` | any | `null` | |
| `_lastApprovedData` | any | `null` | |
| `_autoRefineEnabled` | bool | `false` | |
| `_savedApprovalImages` | array | `[]` | |
| `_savedApprovalVideos` | array | `[]` | |
| `_savedApprovalIndex` | number | `0` | |
| `_savedApprovalVideoIndex` | number | `0` | |
| `_savedCurrentMediaType` | null | `null` | |
| `galleryImages` | array | `[]` | |
| `galleryVideos` | array | `[]` | |
| `galleryIndex` | number | `0` | |
| `_savedGalleryImages` | array | `[]` | |
| `_savedGalleryVideos` | array | `[]` | |
| `_savedGalleryIndex` | number | `0` | |
| `imageData` | string/null | `null` | R2/HTTP URL or null |
| `filename` | string | `""` | |
| `imageWidth` | number | `0` | |
| `imageHeight` | number | `0` | |
| `_imageAssetId` | null | `null` | |
| `_pages` | array | `[]` | |
| `_pageIndex` | number | `0` | |
| `_savedRowMapping` | object | `{}` | |

**Inputs**: `[{ "name": "input", "type": "*", "link": null }]`
**Outputs**: `[{ "name": "output", "type": "image", "links": [], "slot_index": 0 }]`
**Size**: `[320, 380]`

**Use case**: When you have an already-generated image (e.g., from a previous run) that needs to be used as a reference. Set `imageData` to the R2 URL of the image. The Media node passes it through as an image output to downstream NanobananaAPI or Veo3 nodes.

---

## Link Format

Each link is a 6-element array in the tab's `graphData.links`:

```
[linkId, sourceNodeId, sourceSlotIndex, targetNodeId, targetSlotIndex, dataType]
```

**Rules**:
- `linkId` must be unique within the tab (sequential integers starting at 1)
- `sourceSlotIndex` is the index into the source node's `outputs` array
- `targetSlotIndex` is the index into the target node's `inputs` array
- Each input slot can have at most ONE link (set `input.link` to the linkId)
- Each output slot can have MULTIPLE links (add linkId to `output.links` array)
- `dataType` values:
  - `"string"` — Prompt → NanobananaAPI prompt slot, Prompt → Veo3 prompt slot
  - `"image"` — ReferenceImage → NanobananaAPI image slot, Approval → Veo3 image slot, Approval → NanobananaAPI image slot
  - `"*"` — NanobananaAPI → Approval (wildcard)

### Wiring Checklist

When creating a link:
1. Choose a unique `linkId`
2. Add the linkId to the source node's output `links` array
3. Set the target node's input `link` to the linkId
4. Add `[linkId, sourceId, sourceSlot, targetId, targetSlot, type]` to the tab's `graphData.links`
5. Update `graphData.last_link_id` to the highest linkId used

---

## Type Compatibility

| Output Type | Can Connect To |
|-------------|---------------|
| `"string"` | `"string"` input (Prompt → NanobananaAPI/Veo3 slot 0) |
| `"image"` | `"image"` input (ReferenceImage/Approval → NanobananaAPI image slots, Approval → Veo3 frame slots) |
| `"image"` (from NanobananaAPI) | `"*"` input (NanobananaAPI → Approval, uses `"*"` link type) |
| `"video"` (from Veo3) | `"*"` input (Veo3 → Approval, uses `"*"` link type) |

---

## Building the Mainbody Tab

### Input Required

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

### Construction

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

Same pattern as scenes, using the **same image generation group** as scenes (same Approval fan-out). Hooks are positioned below scenes in the same Mainbody tab. No separate hook image gen group — the Founder Approval fans out to both scene and hook Veo3 nodes.

**Step 3: Fan-out connections**

Each Approval node's output `links` array accumulates link IDs — one per Veo3 node that uses this image group as its start frame reference.

### Layout (Mainbody)

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

---

## Building the BRoll Tab

### Input Required

- `brolls[]` — Array of B-roll clips, each with:
  - `startPrompt` — Start frame image prompt JSON (stringified)
  - `endPrompt` — End frame image prompt JSON (stringified)
  - `videoPrompt` — Video prompt JSON (stringified)
  - `duration` — `"4"` typically (string)
  - `requires` — Reference images for start frame (e.g., `["product image"]`)

### Construction (per B-roll clip)

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

### End Frame Reference Chaining

The start frame's Approval output serves double duty:
1. Goes to Veo3 as `start frame` (slot 1)
2. Goes to end frame NanobananaAPI as a reference image input (for visual consistency)

The start Approval's output `links` array will have 2 link IDs — one to Veo3 slot 1, one to end NanobananaAPI slot 2.

### B-Roll Without End Frames

If a B-roll clip only has a start frame (no end frame prompt), skip Step 2 and wire the start Approval directly to the Veo3 start frame slot. Leave Veo3 end frame as null.

### Layout (BRoll)

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

---

## Input Format

### Option A: Structured handoff

```
Product: [product name]

Image Generation Groups:
GROUP 1 (scenes 1, 2, 5):
  Prompt: [image prompt text or path to .json file]
  Requires: [avatar image, product image]

GROUP 2 (scenes 3, 4):
  Prompt: [image prompt text or path to .json file]
  Requires: [avatar image, product image]

Scene Prompts:
SCENE 1 (8s, ref: group 1): [path to video .json]
SCENE 2 (6s, ref: group 1): [path to video .json]
SCENE 3 (8s, ref: group 2): [path to video .json]
SCENE 4 (4s, ref: group 2): [path to video .json]
SCENE 5 (8s, ref: group 1): [path to video .json]

B-Roll:
BROLL 1 (4s):
  Start frame: [path to start .json]
  End frame: [path to end .json]
  Video prompt: [path to video .json]
  Requires: [product image]

BROLL 2 (4s):
  Start frame: [path to start .json]
  End frame: [path to end .json] (or "none")
  Video prompt: [path to video .json]
  Requires: [product image]
```

### Option B: "Import everything from the pipeline"

The user says "import to PatchWork" or similar. Read the project files directly from `../manager/projects/[project-name]/` to extract:

1. **video-plan.md** — Scene list, durations, reference image mapping
2. **scene-*-image-start.json** — Image prompts (check `requires` field)
3. **scene-*-video.json** — Video prompts per scene (check `duration`)
4. **broll-*-image-start.json** + **broll-*-image-end.json** — B-roll frame prompts
5. **broll-*-video.json** — B-roll video prompts

Parse file names to determine scene-to-image-group mapping:
- `scene-01-02-05-image-start.json` → scenes 1, 2, 5 share this image group
- `scene-03-04-image-start.json` → scenes 3, 4 share this image group

---

## Construction Example: Full Pipeline

This example builds a project with 2 image groups (5 scenes) + 3 B-roll clips.

### Mainbody Tab

**Image Gen Group 1** (used by scenes 1, 2, 5 — requires avatar + product):

```
Nodes:
  id:1  Prompt         [−2000, −324]  text = image prompt JSON      order:0
  id:5  ReferenceImage [−2118, −81]   imageData = avatar URL        order:1
  id:33 ReferenceImage [−1748, 105]   imageData = product URL       order:2
  id:2  NanobananaAPI  [−1228, −110]  imageCount = 2                order:3
  id:28 Approval       [−812, −71]                                  order:4

Links:
  [1, 1, 0, 2, 0, "string"]    — Prompt → API prompt
  [10, 5, 0, 2, 1, "image"]    — Avatar ref → API image 1
  [49, 33, 0, 2, 2, "image"]   — Product ref → API image 2
  [39, 2, 0, 28, 0, "*"]       — API → Approval
```

**Image Gen Group 2** (used by scenes 3, 4):

```
Same pattern, different Y positions (~600px below group 1)
```

**Scene Videos** (one per scene — each Veo3 feeds into a video Approval):

```
Scene 1:
  id:13 Prompt    [−164, −114]  text = scene 1 video prompt JSON    order:5
  id:11 Veo3      [242, −98]    durationSeconds = "8"                order:6
  id:34 Approval  [700, −98]    (video review)                       order:7

Links:
  [14, 13, 0, 11, 0, "string"]   — Prompt → Veo3 prompt
  [40, 28, 0, 11, 1, "image"]    — Approval (group 1) → Veo3 start frame
  [50, 11, 0, 34, 0, "*"]        — Veo3 → video Approval

Scene 2:
  id:32 Prompt    [−213, 432]   text = scene 2 video prompt JSON    order:8
  id:20 Veo3      [690, 375]    durationSeconds = "8"                order:9
  id:35 Approval  [1148, 375]   (video review)                       order:10

Links:
  [48, 32, 0, 20, 0, "string"]
  [41, 28, 0, 20, 1, "image"]    — Same Approval (group 1) fans out
  [51, 20, 0, 35, 0, "*"]        — Veo3 → video Approval
```

**Approval fan-out**: Image Approval node id:28 output links = `[40, 41, ...]` — one per scene/hook that references this image group.

### BRoll Tab

**B-roll 1** (with start + end frames):

```
Start frame:
  id:9  ReferenceImage [−822, 527]   imageData = product URL        order:0
  id:4  Prompt         [−958, 191]   text = start frame prompt       order:1
  id:1  NanobananaAPI  [−340, 180]   imageCount = 1                  order:2
  id:7  Approval       [144, −94]                                    order:3

Links:
  [2, 4, 0, 1, 0, "string"]     — Prompt → API prompt
  [10, 9, 0, 1, 1, "image"]     — Product ref → API image 1
  [5, 1, 0, 7, 0, "*"]          — API → Approval (start)

End frame:
  id:5  Prompt         [−890, 947]   text = end frame prompt         order:4
  id:2  NanobananaAPI  [359, 588]    imageCount = 3                  order:5
  id:6  Approval       [936, 592]                                    order:6

Links:
  [1, 5, 0, 2, 0, "string"]     — Prompt → API prompt
  [11, 9, 0, 2, 1, "image"]     — Product ref → API image 1 (same ReferenceImage, 2nd link)
  [35, 7, 0, 2, 2, "image"]     — Start Approval output → API image 2 (consistency ref)
  [6, 2, 0, 6, 0, "*"]          — API → Approval (end)

Video:
  id:8  Prompt    [972, 102]    text = video prompt                   order:7
  id:3  Veo3      [1444, 449]   durationSeconds = "8"                 order:8
  id:10 Approval  [1900, 449]   (video review)                        order:9

Links:
  [9, 8, 0, 3, 0, "string"]     — Prompt → Veo3 prompt
  [8, 7, 0, 3, 1, "image"]      — Start Approval → Veo3 start frame
  [7, 6, 0, 3, 2, "image"]      — End Approval → Veo3 end frame
  [12, 3, 0, 10, 0, "*"]        — Veo3 → video Approval
```

**Start Approval fan-out**: Approval id:7 output links = `[8, 35]` — start frame to Veo3 AND reference to end frame NanobananaAPI.

**Subsequent B-roll clips** follow the same pattern at offset Y + 1200px per clip.

---

## Output

Save the `.nbflow` file to `output/` with a descriptive name:

```
output/[product]-pipeline-[timestamp].nbflow
```

Example: `output/silk-glide-pro-pipeline-20260303-143022.nbflow`

After saving, tell the user:

```
Project saved to: output/[filename].nbflow

To import into PatchWork:
1. Open PatchWork
2. On the home screen, click "Import Project"
3. Choose the .nbflow file

The project contains:

TAB: MAINBODY
- [N] image generation groups, each: Prompt + ReferenceImages → NanobananaAPI → Approval
- [N] scene videos, each: Prompt → Veo3 (start frame from Approval)
- Approval fan-out wired: [list which groups serve which scenes]
- Durations: All scenes 8s (only supported duration for frames-to-video)
- ReferenceImage nodes for avatar + product — [load manually / pre-filled with URL]

TAB: BROLL
- [N] B-roll clips, each with:
  Start frame: Prompt + ReferenceImage → NanobananaAPI → Approval
  End frame:   Prompt + ReferenceImage + Start Approval ref → NanobananaAPI → Approval
  Video:       Prompt + Start Approval (first) + End Approval (last) → Veo3 (4s)

All nodes connected and ready to execute.
```

---

## Important Rules

- **Node IDs must be unique** positive integers within each tab
- **Link IDs must be unique** positive integers within each tab
- **Never embed base64 data** in `.nbflow` files — PatchWork strips base64 strings >1024 chars. Use R2/HTTP URLs or set to `null`
- **Always include all required node fields**: `id`, `type`, `pos`, `size`, `flags`, `order`, `mode`, `color`, `bgcolor`, `title`, `properties`, `inputs`, `outputs`
- **Match `imageCount`** to actual image input slots on NanobananaAPI nodes
- **Set `_spawnNum` sequentially** per node type within each tab (first Prompt = 1, second Prompt = 2, etc.)
- **Approval output type is `"image"`**, not `"*"` — the input is `"*"` but the output is typed
- **Veo3 `_previewOpen`** should be `true`; NanobananaAPI `_previewOpen` should be `false`
- **`durationSeconds` is a string**, not a number — `"8"` not `8`
- **`last_node_id` and `last_link_id`** in each tab's graphData must match the highest IDs used
- **Confirm before generating** — show the user what will be created (tab structure, node counts, connections) before writing the file

## Tools

- **Google Sheets**: `~/.claude/skills/gsheets/` — Read, write, format, and search Google Sheets. Invoke via `/gsheets` skill. Service account auth, known spreadsheet: Salvora Prehooks (ID: `13y_rw5s_7FlVhCHhKr0C9w7oPg9AWW9nPFRUG2YXJEU`).
