# Split-Screen Storytelling

Third-party transformation narrative. Creator speaks in the bottom half while the top half cycles through visual evidence: before/during/after photos, ingredient B-roll, product shots. The split layout lets you show proof while the narrator explains.

## Reference Video

**Daughter Hero Journey** (68s) — https://www.tiktok.com/t/ZP8b94SdK/

Daughter helps her mom glow up after dad leaves for a younger woman. Creator narrates from the bottom half while the top half cycles through: cheater photo, mom's face (before/during/after), food B-roll, product shot. Final frame flips to full-screen creator holding product.

## When to Use

- Transformation stories told by a third party (daughter helping mom, friend helping friend)
- Visual EVIDENCE of the transformation is the selling point
- Before/after arcs where the proof needs to stay on screen alongside narration
- Multi-step routines or ingredient reveals where each step gets its own visual
- Stories where the creator is the guide, not the testimonial subject

## Visual Structure

```
[SPLIT: Top = reference photo (story context) | Bottom = creator talking head]
    ↓ top half cycles
[SPLIT: Top = subject "before" close-up | Bottom = creator talking head]
    ↓
[SPLIT: Top = food/ingredient B-roll | Bottom = creator talking head]
    ↓ repeats per ingredient/step
[SPLIT: Top = subject "during" / "after" | Bottom = creator talking head]
    ↓
[SPLIT: Top = product shot | Bottom = creator talking head]
    ↓ final flip
[FULL FRAME: Creator holding product, subject inset in corner]
```

- Creator occupies the bottom half during all split-screen scenes
- Top half is static images (not video), swapped at each narrative beat
- Text hooks appear as overlays on the split frame
- Final frame breaks the split: creator goes full-screen for the CTA, subject photo shrinks to corner inset
- Single-word captions (subtitles) added in post

## Scene Layout

| Element | Frame Position | Size |
|---------|---------------|------|
| Creator (speaking) | Bottom half | ~50% of frame |
| Evidence image (top) | Top half | ~50% of frame |
| Creator (final CTA) | Full screen | 100% |
| Subject inset (final CTA) | Bottom-right corner | ~15-20% |
| Text hook | Centered on split frame | Overlay |
| Subtitles | Bottom center (over creator) | Overlay, added in post |

## Camera

- Creator filmed selfie-style, close crop (head and shoulders only since they appear small in frame)
- Eye-level or slight high-angle
- 9:16 vertical
- Smartphone aesthetic
- Top half is static images composited in post, not live video

## Key Patterns

1. Creator is always small/bottom. Visual evidence dominates the top half.
2. Top half cycles through: reference photos, food/ingredient B-roll, product shots, before/during/after photos.
3. Before/during/after transformation arc shown through 3 separate subject face shots (sad/aging, improving, glowing).
4. Mid-video CTA embedded naturally ("comment salad") rather than only at the end.
5. Final frame flips the layout. Creator goes full-screen for the product CTA.
6. Two visual registers: personal (subject photos, food B-roll) and product (bottle, brand).
7. The "hero helper" narrative makes the creator a relatable intermediary, not the testimonial subject.

## Reference Image Groups

- **Creator speaking image** (full prompt): Creator in setting, close crop for bottom-half framing
- **Subject "before" photo** (full prompt): Subject looking sad, puffy, aging, no makeup
- **Subject "during" photo** (full prompt): Same subject, visibly improved but not final result
- **Subject "after" photo** (full prompt): Same subject, dramatic improvement, confident, glowing
- **Context photo** (full prompt): Story setup image (e.g., the cheater with younger partner)
- **Food/ingredient B-roll** (full prompt): Top-down food shots per ingredient (one image per step)
- **Product shot** (full prompt or real photo): Hand holding product, casual bathroom/vanity background
- **Final CTA frame** (full prompt): Creator full-screen holding product, subject photo composited as inset

## Scene Segmentation

- All scenes 8 seconds (Veo 3.1 constraint)
- 22-30 words per scene
- The creator's speaking footage is continuous (same angle, same crop). Scene breaks happen in the top-half image swaps, not camera changes.
- Top-half image changes align with narrative beats (new ingredient, new transformation stage, product reveal)
- Final scene breaks the split format entirely

## Beat Structure

The creator stays in the bottom half the entire video. Visual transitions happen in the TOP half only, swapping images at each narrative beat. Final scene breaks the split entirely.

```
HOOK (0:00-0:14):
  Story setup. Emotionally loaded premise that creates investment.
  Visual: Creator bottom + context photo top (the cheater, the villain, the inciting incident).

BEFORE STATE (0:14-0:20):
  Show the starting point. "This is how she looked when we started."
  Visual: Creator bottom + subject "before" face top (sad, puffy, aging, no makeup).

INGREDIENT LOOP (0:20-0:40):
  Each ingredient/step gets its own top-half image swap. One image per step.
  Visual: Creator bottom + food/ingredient B-roll top (top-down food photography). Repeats per ingredient.

AFTER STATE (0:40-0:54):
  Transformation proof. "By the end of month two, she looked 15 years younger."
  Visual: Creator bottom + subject "during/after" face top + product shot top (cycles between these).

CTA FLIP (1:00-1:08):
  Layout BREAKS. Creator goes FULL FRAME holding product. Subject photo shrinks to corner inset.
  Visual: Full-screen creator outdoors + mom "after" face as small bottom-right inset.
```

Key takeaway: The split layout is the format. Top half cycles through evidence images at narrative beats. Only the final CTA breaks the split for impact.

## Pipeline Mapping

| Component | Agent | Notes |
|-----------|-------|-------|
| Creator speaking scenes | Veo Prompter | Universal talking head template, swap dialogue only. Creator is cropped tight for bottom-half compositing |
| Subject before/during/after | Image Prompter | 3 variations of the same face: sad/aging, improving, glowing. Character reference for consistency across all 3 |
| Context photo | Image Prompter | Story setup image (e.g., man with younger woman). One-off, no character consistency needed |
| Food/ingredient B-roll | Image Prompter | Top-down food photography, one image per ingredient step |
| Product shot | Image Prompter or real photo | Hand holding product, casual setting |
| Final CTA frame | Image Prompter | Creator full-screen with product. Different framing from speaking scenes |
| Split-screen compositing | Post-production | Top/bottom split, image swaps timed to script beats |
| Layout flip (final scene) | Post-production | Full-frame creator + corner inset of subject |
| Text overlays | Post-production | Hook text, subtitles |
| PatchWork | PatchWork Importer | Creator speaking scenes in Mainbody tab. Top-half images generated separately. Compositing is manual |

## Example

Daughter Hero Journey video: 8 speaking scenes (all from creator's bottom-half perspective), 7 top-half image swaps (cheater photo, mom before, kiwi bowl, salad bowl, mom during, product shot, mom after as inset). Creator maintains one angle throughout. Top half carries the visual proof. Final frame breaks the format for CTA impact.
