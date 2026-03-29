# Text-Wall Over B-Roll

<!-- analysis-date: 2026-03-26 -->
> **Reference data**: Analyzed 2026-03-26. Source accounts: @carly_unfiltered (17.8M views). Upload date unknown.

No speaker visible. Looping B-roll clips fill the screen while large bold text overlay carries the entire message. The text IS the script. Background music or ambient audio only.

Example: @carly_unfiltered style (17.8M views). Easiest format to produce with AI since there is no face consistency to maintain.

## When to Use

- Testimonial-style content without showing a face
- Rapid-fire benefit lists, "things I wish I knew" format, listicles
- Product-focused content where the visuals sell (texture, ingredients, packaging)
- When no avatar is available or face consistency is a bottleneck
- Anonymous authority content ("a dermatologist told me...", "my doctor said...")
- High-volume content where speed matters more than personal connection

## Visual Structure

```
[FULL SCREEN: B-roll clip — product close-up, lifestyle, or ingredient shot]
[TEXT OVERLAY: 2-4 lines of bold text, centered or left-aligned]
    | swaps every 3-5s
[FULL SCREEN: Next B-roll clip — different angle or subject]
[TEXT OVERLAY: Next block of text]
    | repeats
[FULL SCREEN: Product hero shot or CTA visual]
[TEXT OVERLAY: CTA text — "comment GLOW for the link"]
```

- B-roll occupies 100% of the frame at all times
- Text overlay is the only narrative element (no voiceover, no speaker)
- Background music sets the mood and pacing
- B-roll clips loop or crossfade, one per text block

## Scene Layout

| Element | Frame Position | Size |
|---------|---------------|------|
| B-roll footage | Full screen | 100% |
| Text overlay | Centered or left-aligned, vertically centered | Large, 2-4 lines visible |
| CTA text | Bottom third or centered | Same style as body text |
| Subtitles | N/A (text IS the content) | N/A |

## Beat Structure

```
HOOK TEXT (3-5s):
  Bold provocative statement or question
  Visual: Eye-catching B-roll — product being poured, ingredient close-up, skin texture
  Text: 1-2 punchy lines, large font

PROBLEM / SYMPTOM TEXT (10-15s):
  Pain points, relatable frustrations, "things nobody tells you"
  Visual: Relevant B-roll — failed products, skin issues, lifestyle context
  Text: 2-4 lines per swap, new block every 3-5s

SOLUTION / BENEFIT TEXT (10-15s):
  Product reveal, ingredient breakdown, mechanism explanation
  Visual: Product B-roll — close-ups, pouring, texture, packaging
  Text: Benefits listed one block at a time, building the case

CTA TEXT (5s):
  Comment keyword, follow, or "link in bio"
  Visual: Product hero shot or lifestyle aspirational clip
  Text: Clear action line
```

## Camera

- **Product close-ups**: Macro lens feel, shallow DOF, clean surface
- **Lifestyle shots**: Slow pan, golden hour, cozy/aspirational setting
- **Ingredient glamour**: Top-down, studio-lit, isolated ingredients
- **Texture shots**: Extreme close-up of cream, serum, powder
- All 9:16 vertical
- Slow movement preferred (slow pan, gentle zoom, subtle rotation)
- No handheld shake. Smooth, cinematic, almost meditative

## Text Overlay Style

- Large bold sans-serif font (Montserrat, Inter, or similar)
- White text with dark shadow or semi-transparent background bar
- 2-4 lines visible at a time, never a full paragraph
- Each text block stays on screen 3-5 seconds before swapping
- Text swaps can be hard cuts or subtle fade transitions
- All caps or sentence case, never mixed within a video

## Pipeline Mapping

| Component | Agent | Notes |
|-----------|-------|-------|
| B-roll clips | Veo Prompter or Seedance | Start image reference per clip, ambient audio, no dialogue |
| B-roll reference images | Image Prompter | Product close-ups, ingredient shots, lifestyle stills |
| Text overlays | Post-production | Added in editing software, synced to music beats |
| Background music | Post-production | Trending audio or royalty-free ambient track |
| Speaking scenes | N/A | None. No Veo needed |
| Avatar images | N/A | None. No avatar needed |
| PatchWork | N/A | No PatchWork file. All clips are Veo/Seedance (manual) |

## Key Difference from Talking Head

In talking head, the speaker is the primary trust signal and B-roll is supplementary. In text-wall over B-roll, there is no speaker at all. The text carries the narrative while B-roll provides visual atmosphere and product proof. This removes the face consistency challenge entirely, making it the fastest format to produce with AI generation.

## Key Difference from Faceless Hands-Only

Faceless hands-only shows a live demo (hands interacting with product). Text-wall over B-roll is purely atmospheric. The B-roll loops or crossfades without showing a continuous process. There are no hands, no demo steps, no sequential action.

## Storyboard Adjustments

When planning this video type:
- Scene count is driven by **text blocks**, not dialogue pacing
- Each text swap gets its own B-roll clip (or clips loop across multiple text blocks)
- No reference image groups for speaker consistency needed
- B-roll density is effectively always "High" since B-roll IS the entire visual
- Plan 4-8 unique B-roll clips per video (some can loop)
- Music selection drives the pacing more than script rhythm
- Total duration typically 30-45s (shorter than talking head)
