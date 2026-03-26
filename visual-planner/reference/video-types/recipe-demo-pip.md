# Recipe Demo PiP

Demo footage dominates the frame. The speaker appears as a small picture-in-picture (PiP) circle in the corner. The visual focus is on ingredients, mixing, and application, not the speaker's face.

## When to Use

- DIY recipes (skincare scrubs, health drinks, food remedies)
- Ingredient-by-ingredient walkthroughs (Pattern U: Routine Walkthrough)
- Product demonstrations where the process matters more than the speaker
- Educational content where showing beats telling
- "Ancient remedy" or "kitchen hack" formats

## Visual Structure

```
[MAIN FRAME: Top-down demo footage — ingredients, mixing, pouring]
[PiP CIRCLE: Speaker/expert in bottom-left corner, small]
[TEXT OVERLAY: Single-word keyword synced to voiceover, centered]
    ↓ repeats per ingredient/step
[MAIN FRAME: Application footage — hands applying, face shot]
[PiP CIRCLE: Speaker still visible]
    ↓
[MAIN FRAME: CTA — may switch to full-screen speaker or stay PiP]
```

## Scene Layout

| Element | Frame Position | Size |
|---------|---------------|------|
| Demo footage (B-roll) | Full screen, top-down | 100% of frame |
| Speaker PiP | Bottom-left corner, circular crop | ~15-20% of frame |
| Single-word caption | Center of frame, bold white text with dark outline | Large, 1-2 words max |

## Beat Structure

This format follows a **repetitive ingredient loop**:

```
HOOK (3-7s):
  Bold claim + authority statement
  Visual: First ingredient being shown or speaker full-screen

INGREDIENT LOOP (repeated 3-6x):
  1. Show ingredient being added to bowl/surface (top-down B-roll)
  2. Name it with single-word text overlay ("COFFEE", "HONEY", "LEMON")
  3. Explain the benefit (voiceover, 5-10s per ingredient)
  Visual: Pouring, scooping, squeezing — continuous action

MIX/PREPARE (5-10s):
  Combine all ingredients
  Visual: Stirring, mixing into paste/liquid

APPLICATION (5-15s):
  Apply to skin/body, show the process
  Visual: Close-up hands applying, or different person demonstrating
  Can use a second subject (younger model) for application shots

CTA (5-10s):
  Identity + follow + keyword CTA
  Visual: Speaker PiP or switch to full-screen speaker
```

## Camera

- **Demo footage**: Top-down (bird's eye), static, clean white/marble surface
- **Application footage**: Close-up, handheld or propped, bathroom/vanity setting
- **Speaker PiP**: Waist-up, eye-level, separate recording (composited in post)
- All 9:16 vertical

## Props & Staging

- Clean white or marble surface (minimal, product-focused)
- Glass bowls, wooden spoons (natural/organic feel)
- Fresh ingredients visible (flowers, herbs as decoration)
- No clutter. The opposite of UGC narrative clutter. This format is clean and clinical

## Text Overlay Style

- Single word per beat, synced to voiceover
- Bold white text, dark outline or shadow for readability
- Centered in the frame
- Keywords highlight the ingredient name OR the benefit ("COFFEE", "PUFFINESS", "WATER")
- NOT full sentences. NOT text hooks. Just keyword anchors

## Two Subjects

This format often uses two different people:
1. **The expert** (PiP): Older, authoritative, voiceover narrator. Provides credibility
2. **The demo person** (application shots): Younger, matches target demographic. Provides aspiration

The expert never touches the product on camera. The demo person does the application. This separation reinforces the authority dynamic

## Reference Example

**Helen Xu — Coffee Scrub** (`helenxu_coffee_scrub.mp4`)
- Duration: ~82s
- Structure: Hook (7s) + 5 ingredients (50s) + mix/apply (15s) + CTA (10s)
- Speaker: Older Chinese woman (Helen Xu), traditional Chinese medicine authority
- Demo person: Younger woman applying scrub to face
- Surface: White/marble, glass bowl, wooden spoon, flowers as decoration
- Text overlays: "COFFEE", "PUFFINESS", "MOTIONS", "WATER" — single keywords
- CTA: "Comment HEALTH for my complete natural skin care protocol" (Pattern O: Keyword CTA)
- Script pattern: Pattern U (Routine Walkthrough) + Pattern E (Medical Authority)

## Pipeline Mapping

| Component | Agent | Notes |
|-----------|-------|-------|
| Demo footage (ingredient shots) | Veo Prompter or Seedance | Top-down B-roll, start image reference per ingredient step |
| Application footage | Veo Prompter or Seedance | Close-up hands/face, separate reference image |
| Speaker PiP | Veo Prompter | Standard talking head, but output is composited as PiP in post |
| Ingredient images | Image Prompter | Top-down still: bowl, spoon, ingredient, clean surface |
| Speaker image | Image Prompter | Standard waist-up portrait for PiP circle |
| Text overlays | Post-production | Single-word keywords added in editing |
| PiP compositing | Post-production | Speaker circle layered over demo footage in editing |

## Key Difference from Talking Head

In talking head, B-roll is the interruption. In recipe demo PiP, the **demo IS the main content** and the speaker is reduced to a small overlay. The pipeline needs to generate more B-roll clips (one per ingredient/step) and fewer speaking scene variations.

## Storyboard Adjustments

When planning this video type:
- Scene count is driven by the **number of ingredients/steps**, not by dialogue pacing
- Each ingredient gets its own scene (even if the voiceover continues across ingredients)
- Reference image groups are per-ingredient (different bowl contents at each stage)
- Speaker scenes can be fewer (1-2 angles, composited as PiP)
- B-roll density is effectively always "High" since demo footage IS the main visual
