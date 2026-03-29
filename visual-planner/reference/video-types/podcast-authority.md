# Podcast Authority

<!-- analysis-date: 2026-03-26 -->
> **Reference data**: Analyzed 2026-03-26. Source accounts: @dailyhealthtalk. Upload date unknown — likely 2025.

Two-segment format: silent before/after transformation prehook, then hard cut to a static podcast desk setup. Speaker sits at a desk with a large podcast microphone, bookshelf backdrop, and authority props. The frame locks for the entire main body with no camera switches or B-roll cutaways.

## When to Use

- Authority/expert positioning with medical credibility (doctor, specialist)
- Supplement education where "doctor explains" framing builds trust
- When the speaker should feel like an expert rather than a peer
- Scripts with a single sustained monologue (no scene variety needed)
- Products that benefit from clinical/professional association without explicit claims

## Visual Structure

```
[FULL SCREEN: Before/after transformation B-roll — home setting, no audio, no text]
    ↓ hard cut at ~15s
[FULL SCREEN: Speaker at podcast desk with mic, bookshelf behind]
[TEXT: Persistent kinetic captions — white bold caps, 1 green keyword per line]
    ↓ static for ~60s
[FULL SCREEN: Same setup + product in hand + red CTA arrow]
```

- Prehook is purely visual: posture/props change (cane present to cane gone), no text overlays, no audio
- Main body is a single locked frame for the entire speaking portion
- No B-roll cutaways during speaking. The static podcast frame IS the visual
- Kinetic captions with one highlighted keyword per subtitle line (lime green on key benefit/symptom word)
- Product withheld until CTA. Speaker holds product only in the final frame
- Red downward arrow graphic at CTA mimics native TikTok UI, pointing toward the shop button

## Scene Layout

| Element | Frame Position | Size |
|---------|---------------|------|
| Speaker at desk | Full screen, seated, centered | 100% |
| Podcast microphone | Right side of frame, partially visible | Prop |
| Bookshelf/supplements backdrop | Behind speaker | Background |
| Kinetic captions | Lower third, centered | Overlay, added in post |
| Green keyword highlight | Within caption line, one word per line | Overlay, added in post |
| Product (CTA only) | Held in speaker's hand | Foreground, final scene only |
| Red CTA arrow | Pointing down toward shop button | Overlay, added in post |

## Camera

- Static, seated at desk, eye-level
- 9:16 vertical
- Podcast mic visible on right side of frame
- Bookshelf and supplement bottles as backdrop (authority set dressing, never referenced in dialogue)
- Locked angle for entire main body. No camera switches, no B-roll cuts
- Semi-professional aesthetic (cleaner than raw UGC, but not studio-polished)

## Reference Image Groups

- **Prehook "before" image** (full prompt): Subject in home setting, struggling posture, prop indicating ailment (cane, brace, etc.)
- **Prehook "after" image** (full prompt): Same subject and setting, upright posture, prop removed, companion reacting positively
- **Base speaking image** (full prompt): Speaker at podcast desk with mic, bookshelf behind, no product in hand
- **Product hold image** (modification mode): Same podcast setup, speaker holds product bottle. Used for CTA scene only

## Scene Segmentation

- All scenes 8 seconds (Veo 3.1 constraint)
- 22-30 words per scene
- **No angle changes** across main body. Single locked podcast frame for all speaking scenes
- No B-roll density selection. This format uses zero B-roll during speaking
- Prehook clips are separate (before/after transformation, no speaking)

## Beat Structure

This format has minimal visual transitions — the podcast frame locks for the entire main body.

```
PREHOOK (0:00-0:15):
  Silent before/after transformation footage. Home setting, no text, no audio.
  Visual: Wide shot of subject struggling (cane, brace), then same subject upright and healthy.

HARD CUT TO PODCAST (0:15):
  "Just listen." Single word bridge into the static podcast frame.
  Visual: Speaker at desk with mic, bookshelf behind. Text overlays begin. Frame locks here.

PODCAST BODY (0:15-1:05):
  Symptom cascade → mechanism → solution → benefits → dosage. All on one locked frame.
  Visual: Static podcast desk shot. Kinetic captions with one green keyword per line.

CTA (1:05-1:17):
  Brand name, offer, shop button reference.
  Visual: Same desk setup. Speaker now holds product. Red arrow appears pointing down.
```

Key takeaway: TWO visual changes in the entire video — the hard cut from prehook to podcast, and the product appearing at CTA. Everything between is the same static frame with text overlays doing all the work.

## Pipeline Mapping

| Component | Agent | Notes |
|-----------|-------|-------|
| Prehook clips | Veo/Seedance Prompter | Before/after transformation, no speaking, home setting |
| Prehook images | Image Prompter | 2 images: struggling pose (before), healthy pose (after) |
| Speaking scenes | Veo Prompter | Universal talking head template, swap dialogue only. Single locked angle |
| Speaking image (base) | Image Prompter | Speaker at podcast desk with mic, bookshelf, supplements backdrop |
| CTA image (product hold) | Image Prompter | Modification mode: same setup, product in hand |
| Text overlays | Post-production | Kinetic captions with one green keyword per line |
| Red CTA arrow | Post-production | Downward arrow mimicking TikTok UI |
| PatchWork | PatchWork Importer | Mainbody tab: single image gen group to all Veo3 speaking nodes. Prehook clips separate |

## Key Differences from Talking Head

| Aspect | Talking Head | Podcast Authority |
|--------|-------------|-------------------|
| Camera angles | 1-3 angles, shifts at emotional beats | Single locked angle, no switches |
| B-roll | Cutaways during speaking (density modes) | Zero B-roll during speaking |
| Setting | Casual (bathroom, kitchen, bedroom) | Professional (desk, mic, bookshelf) |
| Speaker posture | Standing or casual seated | Seated at desk, formal |
| Props | Product only | Podcast mic, bookshelf, supplement bottles, product at CTA |
| Trust signal | Peer relatability | Expert authority |
| Prehook style | Text hooks, symptom montage | Silent before/after transformation (no text, no audio) |
| Image gen groups | Multiple (angle changes) | One for all speaking scenes |

## Example

Salvora cortisol video: 16s silent prehook (older woman with cane to standing upright), hard cut to Black male doctor at podcast desk with mic and medical bookshelf. 8 speaking scenes on single locked frame. Kinetic captions with lime green keyword highlights. Product reveal only at CTA with red arrow pointing to shop button. ~80s total runtime.
