# Faceless Hands-Only Demo

No face visible. Only hands, product, and surface. Text overlays carry the message alongside a continuous product demonstration. Common in skincare application, unboxing, product comparison, and "watch this" demos.

Fully AI-feasible since no face consistency is needed. The hands and product are the entire visual.

## When to Use

- Product texture or application is the selling point
- ASMR-adjacent content ("satisfying" genre, smooth textures, crisp sounds)
- Skincare routines, serum application, cream blending
- Unboxing and first impressions
- Product comparison (side-by-side)
- Ingredient mixing or DIY recipes (simpler than Recipe Demo PiP since no speaker overlay)
- "Watch this" or "you need to see this" hook formats

## Visual Structure

```
[FULL SCREEN: Top-down or angled shot — hands + product + clean surface]
[TEXT OVERLAY: Hook text or product name]
    | continuous demo action
[FULL SCREEN: Hands open, pour, apply, or demonstrate product]
[TEXT OVERLAY: Benefit or instruction text]
    | angle change or close-up
[FULL SCREEN: Macro texture shot — cream, serum, powder on skin]
[TEXT OVERLAY: Result or reaction text]
    |
[FULL SCREEN: Product packaging or final result]
[TEXT OVERLAY: CTA]
```

- Hands and product occupy the frame at all times
- Camera stays tight on the action, never pulls wide
- Text overlays provide context, benefits, or instructions
- Background music or ASMR audio (product clicks, squishes, pours)

## Scene Layout

| Element | Frame Position | Size |
|---------|---------------|------|
| Hands + product demo | Full screen, top-down or slight angle | 100% |
| Surface/backdrop | Fills frame behind hands | 100% |
| Text overlay | Top third or bottom third, avoiding hand action area | Medium, 1-2 lines |
| Product label close-up | Full screen (cut-in shot) | 100% |

## Beat Structure

```
PRODUCT REVEAL (3-5s):
  Hands bring product into frame, or product sits on surface and hands enter
  Visual: Clean surface, product centered, hands reach in
  Text: Hook line ("this changed my skin in 2 weeks") or product name
  Audio: Satisfying click, cap pop, or ambient

APPLICATION / DEMO (15-25s):
  Hands interact with product — open, pour, squeeze, apply, blend
  Visual: Multiple angles or continuous top-down action
  Text: Benefits, instructions, or ingredient callouts (1 line at a time)
  Audio: ASMR textures (squish, pour, tap) or background music
  Can include 2-3 sub-steps:
    1. Open/dispense (3-5s)
    2. Apply to skin or surface (5-10s)
    3. Blend/massage/work in (5-10s)

RESULT / TEXTURE CLOSE-UP (5-10s):
  Macro shot of the result — skin glow, absorbed serum, smooth texture
  Visual: Extreme close-up, slow movement, shallow DOF
  Text: Result claim ("instant glow", "absorbed in seconds")
  Audio: Music swell or ambient

CTA TEXT (3-5s):
  Product packaging or hands holding product up
  Visual: Product label visible, clean framing
  Text: CTA line ("comment GLOW for the link", "link in bio")
```

## Camera

- **Primary angle**: Top-down bird's eye (most common). Static or very slow push-in
- **Secondary angle**: 45-degree slight angle for depth. Shows product label and hand interaction
- **Macro inserts**: Extreme close-up for texture, absorption, skin surface
- All 9:16 vertical
- Clean, well-lit, minimal shadow
- Smooth movement only (slow zoom, gentle slide). No handheld shake
- Shallow DOF on macro shots, deep DOF on top-down overview

## Props & Staging

- **Surface**: Clean white marble, light wood, or matte white. One material per video
- **Product**: Centered, label facing camera when visible
- **Hands**: Clean, well-groomed nails, minimal jewelry (one ring max)
- **Complementary items**: Small towel, dropper, cotton pad. Only what the demo needs
- **Background elements**: Minimal. A plant leaf, a candle, or nothing. The surface should feel intentionally styled but not cluttered
- No clutter. Clean and product-focused. The aesthetic is closer to product photography than UGC

## Text Overlay Style

- Clean sans-serif font, medium weight
- White or off-white text with subtle shadow
- Positioned in the top or bottom third to avoid covering the hand action
- 1-2 lines at a time, swapped every 3-5 seconds
- Can use colored highlight on key words (ingredient names, benefit claims)
- Never covers the product label or the main hand interaction

## Pipeline Mapping

| Component | Agent | Notes |
|-----------|-------|-------|
| Demo clips (hands + product) | Veo Prompter or Seedance | Start image reference per step (hands + product + surface). 4-8s per clip |
| Macro/texture inserts | Veo Prompter or Seedance | Close-up reference image, slow zoom motion |
| Reference images (demo steps) | Image Prompter | Top-down still: hands, product, surface at each step |
| Reference images (macro) | Image Prompter | Extreme close-up: texture on skin, serum drop, cream swirl |
| Text overlays | Post-production | Added in editing, synced to demo beats |
| Audio (ASMR/music) | Post-production | ASMR foley or background music track |
| Speaking scenes | N/A | None. No Veo needed |
| Avatar images | N/A | None. No avatar needed |
| PatchWork | N/A | No PatchWork file. All clips are Veo/Seedance (manual) |

## Key Difference from Talking Head

In talking head, the speaker's face is the trust signal and B-roll cuts away briefly. In faceless hands-only, the product interaction IS the content. There is no speaker, no face, no voice on camera. The demo proves the product through visual evidence rather than verbal persuasion.

## Key Difference from Recipe Demo PiP

Recipe demo PiP has a speaker visible in a PiP circle providing narration and authority. Faceless hands-only has no speaker at all. Recipe demo PiP follows an ingredient-by-ingredient loop structure. Faceless hands-only follows a linear application/demo flow. Recipe demo PiP needs two subjects (expert + demo person). Faceless hands-only needs zero identifiable people.

## Key Difference from Text-Wall Over B-Roll

Text-wall over B-roll uses atmospheric, non-sequential footage (product glamour shots, lifestyle clips). Faceless hands-only shows a continuous, sequential process (step 1, step 2, step 3). The hands are performing an action with a clear beginning, middle, and end.

## Storyboard Adjustments

When planning this video type:
- Scene count is driven by **demo steps**, not dialogue pacing
- Each step (open, pour, apply, blend, result) gets its own scene
- Reference image groups are per-step (different hand position and product state at each stage)
- No speaker image groups needed
- B-roll density concept does not apply since the demo footage IS the main visual
- Plan 3-5 unique demo clips plus 1-2 macro inserts
- Total duration typically 30-50s
- Hand appearance must stay consistent across all reference images (same skin tone, same nails, same ring if any)
