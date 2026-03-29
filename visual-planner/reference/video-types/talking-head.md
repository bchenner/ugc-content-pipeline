# Talking Head

<!-- analysis-date: 2026-03-26 -->
> **Reference data**: Analyzed 2026-03-26. Source accounts: General format. Standard format, not tied to a specific dated video.

The standard UGC format. Avatar speaks directly to camera, full-screen. B-roll clips cut in as brief cutaways during speaking scenes.

## When to Use

- Default for all salesy content (product pitch, CTA-driven)
- Authority/expert positioning (doctor, wellness creator)
- Emotional storytelling (symptom cascade, confession, transformation)
- Any script where the speaker's face and delivery are the primary trust signal

## Visual Structure

```
[FULL SCREEN: Avatar speaking to camera]
    ↓ cutaway
[FULL SCREEN: B-roll clip (2-4s)]
    ↓ back to
[FULL SCREEN: Avatar speaking]
    ...
```

- Avatar occupies 100% of the frame during speaking scenes
- B-roll clips are full-screen cutaways that replace the avatar briefly
- Text hooks appear as overlays on prehook clips (separate from main body)
- Single-word captions (subtitles) are added in post

## Scene Layout

| Element | Frame Position | Size |
|---------|---------------|------|
| Avatar | Full screen | 100% |
| B-roll cutaway | Full screen (replaces avatar) | 100% |
| Text hook (prehooks only) | Centered, lower third | Overlay |
| Subtitles | Bottom center | Overlay, added in post |

## Camera

- Selfie, tripod, or propped-on-surface
- Eye-level or slight high-angle
- 9:16 vertical
- Smartphone aesthetic (deep DOF, slightly off-center)

## Reference Image Groups

- **Base speaking image** (full prompt): Avatar in setting, no product
- **Product hold image** (modification mode): Same scene, avatar holds product
- **End frame** (modification mode, optional): Posture/expression shift
- **B-roll images**: One reference image per B-roll clip (single image, not start+end)

## Scene Segmentation

- All scenes 8 seconds (Veo 3.1 constraint)
- 22-30 words per scene
- Angle changes at emotional/narrative shifts (1-3 angles total)
- B-roll density (High/Medium/Low) determines how many cutaways

## Pipeline Mapping

| Component | Agent | Notes |
|-----------|-------|-------|
| Speaking scenes | Veo Prompter | Universal talking head template, swap dialogue only |
| B-roll clips | Veo Prompter | Start image reference, natural language, no dialogue |
| Speaking images | Image Prompter | Full prompt (base) or modification mode (product hold) |
| B-roll images | Image Prompter | One image per clip |
| PatchWork | PatchWork Importer | Mainbody tab: image groups to Veo3 nodes. B-roll is separate |

## Example

Standard Salvora video: 8-12 speaking scenes, 2-6 B-roll cutaways, 1-2 camera angles, single setting (bathroom/kitchen/bedroom). Avatar speaks about the problem, reveals the product, explains the mechanism, delivers CTA.
