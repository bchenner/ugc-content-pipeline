# Hybrid Two-Part

Two distinct visual formats joined by a hard cut within a single video. The first half uses one format (typically visually rich: mixed-media PiP, reaction overlay, or B-roll montage) to hook and establish the problem. The second half switches to a different format (typically static: talking head, storytelling confession) to deliver the sell and CTA.

The hard cut between halves IS the structural hook. The visual register shift signals "now I'm going to tell you the real answer."

References:
- amazon_cracked_heels (119s) — Mixed-media PiP (cracked skin renders, foam treatment imagery) → hard cut at 0:38 → full-frame talking head in cozy American room for Rhodiola/Salvora pitch
- burner_004 (106s) — Reaction PiP over medical examination footage → hard cut → car talking head/storytelling confession

## When to Use

- When the problem is visually compelling (gross symptoms, dramatic B-roll) but the sell needs personal delivery (talking head trust)
- Amazon content where the hook needs scroll-stopping imagery but the CTA needs a face saying "comment [keyword]"
- When two existing formats each serve half the video better than either could serve the whole
- Symptom-heavy topics where the first half educates visually and the second half pivots to product recommendation
- When you want maximum visual variety without committing to mixed-media for the entire duration

## Visual Structure

```
PART 1 — VISUAL HOOK (30-50% of video):
  Format A: Mixed-media PiP, reaction overlay, B-roll montage, or any visually rich format
  Purpose: Scroll-stop, establish the problem, show symptoms/evidence
  Speaker: Small PiP overlay or reaction insert (NOT full-frame)
    ↓ HARD CUT (no transition, no fade — abrupt visual shift)
PART 2 — TALKING SELL (50-70% of video):
  Format B: Full-frame talking head, storytelling confession, or podcast authority
  Purpose: Mechanism explanation, product pitch, CTA delivery
  Speaker: Full-frame, direct address, personal authority
```

The hard cut is NOT a smooth transition. The setting, framing, lighting, and visual register all change simultaneously. This signals "the entertaining part is over, now listen to me."

## Common Format Combinations

| Part 1 (Hook) | Part 2 (Sell) | Best For |
|---------------|---------------|----------|
| Mixed-media PiP (medical renders + symptom close-ups) | Talking head (home/office setting) | Amazon symptom→supplement videos |
| Reaction PiP (reacting to someone else's footage) | Car confession / storytelling | "I saw this and here's what you need to know" |
| B-roll montage (before/after transformation clips) | Podcast authority (desk, mic, supplements) | Transformation testimonial → expert recommendation |
| Split-screen storytelling (evidence cycling in top half) | Full-frame talking head | Third-party proof → personal endorsement |

## Beat Structure

```
PART 1 — VISUAL HOOK (typically 15-40s):
  Uses the rules of whichever Format A is chosen:
    - If mixed-media PiP: rendered backgrounds cycle, speaker is small PiP
    - If reaction PiP: speaker reacts to external footage
    - If B-roll montage: symptom/transformation clips with text overlay
  Audio: Voiceover or speaking establishes the problem
  Text: Symptom captions, hook lines
  Purpose: Retain attention, educate on the problem, build "I need to hear this"

HARD CUT:
  Visual: Instant switch to completely different setting/framing
  No transition effect. The abruptness IS the design choice
  Often coincides with a narrative pivot word: "But here's the thing..." / "Now listen..."

PART 2 — TALKING SELL (typically 40-80s):
  Uses the rules of whichever Format B is chosen:
    - If talking head: full-frame, static background, direct address
    - If car confession: single shot, persistent text banner, emotional delivery
    - If podcast authority: desk setup, mic, supplements visible
  Audio: Speaker delivers mechanism, product recommendation, CTA
  Text: Keyword captions, "comment [keyword]" CTA
  Purpose: Build trust through personal delivery, convert to action
```

## Pipeline Mapping

| Component | Agent | Notes |
|-----------|-------|-------|
| Part 1 backgrounds | Image Prompter | Rendered medical/symptom imagery, or B-roll reference images |
| Part 1 speaker PiP | Image Prompter | Small avatar overlay (if mixed-media PiP variant) |
| Part 2 speaker | Image Prompter + Veo Prompter | Full-frame talking head or confession scene |
| Hard cut | Post-production | Simple splice in editing. No special assets needed |
| Text overlays | Post-production | Different text styles may apply per part |
| Voiceover | Continuous | Same voice across both parts. The audio bridges the visual cut |

## Key Differences from Other Formats

**vs. Mixed-Media Animation**: Mixed-media cycles visual modes throughout the ENTIRE video. Hybrid uses a rich visual format for only the first portion, then switches to a completely different format (usually simpler, face-driven) for the sell. The switch itself is a structural element.

**vs. Talking Head with B-roll**: Talking head with B-roll is one format throughout (speaker + cutaways). Hybrid is two distinct formats with a hard cut between them. The speaker's framing, setting, and visual role change completely at the cut.

**vs. Any single format**: The hybrid is explicitly not one format. It's a composition strategy. The Visual Planner needs to plan two distinct visual sections and specify where the hard cut falls in the script.

## Storyboard Adjustments

When planning this video type:
- Identify the hard cut point in the script. Typically after the problem/symptom section, before the mechanism/solution
- Plan Part 1 and Part 2 as separate visual plans with different settings, framing, and reference image groups
- Part 1 speaker image (if PiP) and Part 2 speaker image (full-frame) may use the same avatar but in different settings/outfits, or can be the same for consistency
- Flag the format used in each part so the correct pipeline agents handle each section
- The hard cut is a scene boundary. Mark it explicitly in the storyboard
- Audio is continuous across the cut (same voice, same pace). Only visuals change
- Part 2 is usually longer than Part 1. The hook is shorter, the sell needs time
