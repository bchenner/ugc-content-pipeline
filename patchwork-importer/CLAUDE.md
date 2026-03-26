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
- **Prehooks**: One tab per day or per prehook
- **Testing**: A dedicated tab with simplified chains for quick prompt testing
- **B-roll**: Handled externally via Sora 2 (not in PatchWork)

Node IDs and link IDs are scoped **per tab** — each tab's graphData tracks its own `last_node_id` and `last_link_id` independently.

### Groups

Visual rectangles that label sections within a tab. No functional effect, just organization.

```json
{
  "title": "P1 — 3AM Wake-Up (Selfie)",
  "bounding": [x, y, width, height],
  "color": "#444",
  "font_size": 28
}
```

Add groups to `graphData.groups[]`. Calculate `bounding` from min/max node positions plus padding.

---

## Node Chain

The pipeline uses **6 node types**. See [node-types.md](reference/node-types.md) for full node specifications (properties, inputs, outputs, sizes).

```
Prompt + ReferenceImage(s) → NanobananaAPI → Approval(image) → Veo3 → Approval(video)
```

**Every Veo3 node connects to a downstream Approval node** for video review. A 6th node type, **Media**, acts as a standalone reference/approval hybrid for feeding approved images as references.

### Tab Patterns

- **Mainbody Tab**: See [mainbody-tab-pattern.md](reference/mainbody-tab-pattern.md) for image gen groups, scene wiring, two-pass generation, hook integration, fan-out, and layout.
- **BRoll Tab**: See [broll-tab-pattern.md](reference/broll-tab-pattern.md) for start/end frame chains, reference chaining, and layout.
- **Construction Examples**: See [examples.md](reference/examples.md) for a complete 5-scene + 3-B-roll worked example with node IDs, positions, and links.

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
- `dataType` values: `"string"` (Prompt connections), `"image"` (ReferenceImage/Approval connections), `"*"` (NanobananaAPI/Veo3 → Approval)

### Wiring Checklist

When creating a link:
1. Choose a unique `linkId`
2. Add the linkId to the source node's output `links` array
3. Set the target node's input `link` to the linkId
4. Add `[linkId, sourceId, sourceSlot, targetId, targetSlot, type]` to the tab's `graphData.links`
5. Update `graphData.last_link_id` to the highest linkId used

---

## Input Format

### Option A: Structured handoff

```
Product: [product name]

Image Generation Groups:
GROUP 1 (scenes 1, 2, 5):
  Prompt: [image prompt text or path to .json file]
  Requires: [avatar image, product image]

Scene Prompts:
SCENE 1 (8s, ref: group 1): [path to video .json]
SCENE 2 (8s, ref: group 1): [path to video .json]

B-Roll:
BROLL 1 (4s):
  Start frame: [path to start .json]
  End frame: [path to end .json]
  Video prompt: [path to video .json]
  Requires: [product image]
```

### Option B: "Import everything from the pipeline"

The user says "import to PatchWork" or similar. Read the project files directly from `../manager/projects/[project-name]/` to extract:

1. **video-plan.md** — Scene list, durations, reference image mapping
2. **scene-*-image-start.json** — Image prompts (check `requires` field)
3. **scene-*-video.json** — Video prompts per scene
4. **broll-*-image-start.json** + **broll-*-image-end.json** — B-roll frame prompts
5. **broll-*-video.json** — B-roll video prompts

Parse file names to determine scene-to-image-group mapping (e.g., `scene-01-to-06-image-start.json` means scenes 1 through 6 share one image group).

---

## Output Format

### File naming

Save to `output/` with a descriptive name: `output/[product]-[descriptor].nbflow`

### Post-save message

After saving, tell the user:

```
Project saved to: output/[filename].nbflow

To import into PatchWork:
1. Open PatchWork
2. On the home screen, click "Import Project"
3. Choose the .nbflow file

The project contains:

TAB: [TAB NAME]
- [N] image generation groups, each: Prompt + ReferenceImages → NanobananaAPI → Approval
- [N] scene videos, each: Prompt → Veo3 (start frame from Approval) → Approval (video)
- Approval fan-out: [which groups serve which scenes]
- ReferenceImage nodes: [list what needs to be loaded manually]

All nodes connected and ready to execute.
```

---

## Node Naming Rules

Every node must have a descriptive `title` that tells the user what it does or what to upload.

| Node Type | Title Format | Example |
|-----------|-------------|---------|
| Media / ReferenceImage | `"{Asset} — upload {description}"` | `"Avatar Image — upload Black naturopath photo"` |
| NanobananaAPI | `"Generate: {what}"` | `"Generate: Naturopath at desk"`, `"Generate: BG Scene 4 hot flash render"` |
| Veo3 | `"Veo: {scene label}"` | `"Veo: Scene 01 — daughter walks in"`, `"Veo: Scene 09a — transformation results"` |
| Approval | `"Approve: {what}"` | `"Approve: Naturopath image"`, `"Approve: Scene 01 video"` |
| Prompt | `"Prompt: {what}"` | `"Prompt: Base speaking image"`, `"Prompt: Scene 03 dialogue"` |

---

## Dynamic + Template Pattern

When the same reference image is used across multiple Veo scenes (common in talking head, confession, practitioner demo), use the **Dynamic → Template** pattern instead of duplicating the full video prompt in every Prompt node.

### How it works:
1. **Template Prompt** — contains the full video prompt with `{dialogue}` (and optionally `{action}`) as variables
2. **Dynamic Prompt** — contains a dropdown of dialogue lines (one per scene). User selects which scene to generate
3. Dynamic feeds into Template's variable input. Template feeds into Veo3

### When to use:
- All scenes share the same reference image (same setting, same angle, same person)
- Only the dialogue line changes per scene (standard talking head, confession)
- If a scene has a unique physical action (recipe steps, product reveal), include `{action}` as a second variable in the template

### When NOT to use:
- Mixed-Media PiP backgrounds (each background is completely different — no template reuse)
- Scenes with radically different camera angles or settings

### Structure:
```
Dynamic Prompt (dialogue rows) ──→ Template Prompt ({dialogue} variable) ──→ Veo3 ──→ Approval
                                   ↑
                        Approval (start frame image) ──┘
```

If actions vary per scene, add a second Dynamic for actions:
```
Dynamic (dialogue) ──→ Template ({dialogue}, {action}) ──→ Veo3 ──→ Approval
Dynamic (action)   ──↗
```

---

## Testing Workflow

When building a testing project, apply these rules:

1. **`outputCount: 2`** on all NanobananaAPI and Veo3 nodes (instead of 4). Saves credits while testing.
2. **Only 2 Veo scenes per script** — pick the most representative scenes (e.g., scene 1 for the hook, and a mid-body scene). Don't generate all scenes during testing.
3. **Use Dynamic + Template** for Veo prompts — lets the user test different scenes from the same dropdown without rebuilding the workflow.
4. **Layout: horizontal = sequence, vertical = clips in that sequence.** Left-to-right is a new pipeline stage (image gen → approval → video gen → approval). Top-to-bottom are parallel clips within the same stage. Use horizontal space generously.
5. **Name everything** — every node gets a descriptive title (see Node Naming Rules above).

---

## Layout Rules

- **Horizontal axis (left → right)** = pipeline sequence. Each stage goes further right: Reference Images → Prompt → Image Gen → Approval → Veo Prompt → Veo3 → Video Approval
- **Vertical axis (top → bottom)** = parallel clips within the same stage. Multiple Veo scenes stack vertically.
- **Use horizontal space generously** — don't cram everything into a narrow column. Spread stages out with ~400-500px gaps between columns.
- **Group labels** should span the horizontal extent of the stage they describe.

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

## Reference

- **Node type specifications**: [reference/node-types.md](reference/node-types.md)
- **Mainbody tab pattern**: [reference/mainbody-tab-pattern.md](reference/mainbody-tab-pattern.md)
- **BRoll tab pattern**: [reference/broll-tab-pattern.md](reference/broll-tab-pattern.md)
- **Construction examples**: [reference/examples.md](reference/examples.md)
- **Real factory reference file**: [reference/sgp-factory-reference.nbflow](reference/sgp-factory-reference.nbflow) (5 scenes, 3 B-roll, 2 image gen groups)

## Tools

- **Google Sheets**: `~/.claude/skills/gsheets/` — Read, write, format, and search Google Sheets. Invoke via `/gsheets` skill. Service account auth, known spreadsheet: Salvora Prehooks (ID: `13y_rw5s_7FlVhCHhKr0C9w7oPg9AWW9nPFRUG2YXJEU`).
