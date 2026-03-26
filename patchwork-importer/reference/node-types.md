# Node Type Reference

## Required Fields on ALL Nodes

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

---

## 1. Prompt (`nanobanana/Prompt`)

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

### Dynamic Mode

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

### Template Mode

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

**Dynamic -> Template pattern**: A Dynamic node feeds a selected row into a Template node's variable input. This allows per-account content swapping without rebuilding workflows.

---

## 2. ReferenceImage (`nanobanana/ReferenceImage`)

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

---

## 3. NanobananaAPI (`nanobanana/NanobananaAPI`)

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

---

## 4. Approval (`nanobanana/Approval`)

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

---

## 5. Veo3 (`nanobanana/Veo3`)

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

---

## 6. Media (`nanobanana/Media`)

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
