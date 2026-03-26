# Green Screen Commentary

Speaker at bottom-center of the frame (waist-up, ~30-40% of screen), with a green screen background replaced by evidence: screenshots, articles, ingredient lists, competitor labels, studies, or diagrams. The visual evidence is the main content. The speaker provides narration and reactions.

Highest-converting format for supplement micro-practitioners (10k-50k followers). Builds authority through visible proof rather than verbal claims alone.

## When to Use

- Ingredient breakdowns (showing the actual supplement facts panel)
- Competitor debunking (side-by-side label comparisons)
- Study citations ("a 2024 study found..." with the study on screen)
- "Let me show you why" educational content
- Reacting to news articles, social media posts, or competitor claims
- Doctor/expert content where credentials + evidence = trust
- Myth-busting or "what they don't tell you" formats

## Visual Structure

```
[BACKGROUND: Screenshot, article, study, or ingredient list — full screen]
[SPEAKER: Waist-up at bottom-center, ~30-40% of frame height]
[TEXT OVERLAY: Circles, arrows, highlights on the background content]
    | background swaps every 5-10s
[BACKGROUND: Next piece of evidence — different screenshot or diagram]
[SPEAKER: Same framing, continuous talking]
[TEXT OVERLAY: New highlights on new background]
    | repeats 3-5x
[BACKGROUND: Product image or solution reveal]
[SPEAKER: Same framing, delivers CTA]
```

- Speaker stays in the same position and framing throughout
- Only the background changes, creating a "slideshow with narrator" effect
- Text annotations (circles, arrows, underlines) draw attention to specific parts of the background
- Speaker is always visible and always talking

## Scene Layout

| Element | Frame Position | Size |
|---------|---------------|------|
| Background evidence | Full screen, behind speaker | 100% of frame |
| Speaker | Bottom-center, waist-up | ~30-40% of frame height, ~50-60% width |
| Highlight annotations | On background content, around key areas | Circles, arrows, underlines |
| Text callouts (optional) | Near highlighted area, above speaker | Small, 1 line |

## Beat Structure

```
HOOK (3-5s):
  Speaker makes a bold claim or asks a provocative question
  Visual: First background appears — the most shocking piece of evidence
  Text: Optional hook text overlay at top of frame
  Speaker energy: High, leaning in, direct eye contact

EVIDENCE WALKTHROUGH (20-40s):
  Speaker narrates through 3-5 pieces of evidence, one background per point
  Visual: Background swaps every 5-10 seconds
  Each background gets:
    1. Speaker introduces the evidence (2-3s)
    2. Annotations appear highlighting the key area (circles, arrows)
    3. Speaker explains what it means (3-7s)
  Backgrounds can include:
    - Supplement facts panels (circling dosages)
    - Study abstracts (highlighting key findings)
    - Competitor product labels (underlining bad ingredients)
    - Before/after photos (with date stamps)
    - News article headlines
    - Ingredient comparison charts

PRODUCT REVEAL (5-10s):
  Background switches to the product or solution
  Visual: Product image, brand website, or clean product shot as background
  Speaker: Transitions from problem to solution, explains why this product is different
  Annotations: Highlight the good ingredients, the right dosages

CTA (5s):
  Speaker delivers the call to action
  Visual: Background stays on product or switches to a purchase/link screen
  Speaker: Direct, confident close
```

## Camera

- **Speaker framing**: Static, waist-up, eye-level, centered at bottom of frame
- **No camera movement**: Speaker framing never changes. Only backgrounds swap
- **Lighting**: Ring light or front-facing window light on the speaker. Even, flat, no dramatic shadows
- 9:16 vertical
- Speaker is recorded against actual green screen (or solid color for keying)
- Smartphone selfie quality is fine. The evidence is the visual star, not the speaker's production value

## Background Content Types

| Background Type | Source | Notes |
|----------------|--------|-------|
| Supplement facts panel | Real product photo or screenshot | Circle specific dosages or ingredients |
| Study abstract | PubMed screenshot or formatted excerpt | Highlight the key finding sentence |
| Competitor label | Real competitor product photo | Underline problematic ingredients |
| Ingredient comparison chart | AI-generated or designed in Canva | Side-by-side columns |
| News article headline | Screenshot from real article | Highlight the headline and source |
| Before/after photos | User-submitted or stock | Date stamps add credibility |
| Social media post | Screenshot of a relevant post or comment | Blur username if needed |

## Annotations & Highlights

- Red circles around key numbers (dosages, percentages)
- Arrows pointing to specific ingredients or claims
- Yellow highlight bars over key sentences in studies
- X marks or strikethroughs on bad ingredients
- Check marks next to good ingredients
- These are added in post-production, timed to the speaker's narration

## Pipeline Mapping

| Component | Agent | Notes |
|-----------|-------|-------|
| Speaker footage | Veo Prompter | Static framing, waist-up, eye-level. Simple talking head but cropped to bottom 40% in post. Universal template works |
| Speaker reference image | Image Prompter | Waist-up portrait against solid/neutral background (will be keyed out) |
| Background images | Mixed sources | Real screenshots (not AI), AI diagrams, or designed comparison charts. Mostly sourced or created outside the pipeline |
| Green screen compositing | Post-production | Key out speaker background, layer over evidence images |
| Annotations (circles, arrows) | Post-production | Added in editing, timed to voiceover |
| Text overlays | Post-production | Optional hook text or callout labels |
| B-roll clips | N/A | None. Background images are stills, not video |
| PatchWork | PatchWork Importer | Speaker scenes only (standard Veo pipeline). Background images are loaded separately in post |

## Key Difference from Talking Head

In talking head, the speaker IS the visual content and B-roll provides brief supplementary cutaways. In green screen commentary, the visual EVIDENCE is the main content and the speaker provides narration over it. The speaker occupies only 30-40% of the frame, and the audience's eyes are drawn to the background evidence, not the speaker's face. The speaker builds trust through what they show, not just what they say.

## Key Difference from Recipe Demo PiP

Recipe demo PiP has live demo footage (hands mixing, pouring, applying) as the main visual. Green screen commentary has static images (screenshots, studies, labels) as the background. Recipe demo PiP is about process. Green screen commentary is about proof.

## Storyboard Adjustments

When planning this video type:
- Scene count is driven by **number of evidence pieces**, not dialogue pacing
- Each background swap is a scene boundary (even if the speaker continues talking)
- Plan 3-5 background images per video (more than 6 feels rushed)
- Speaker reference image groups are simpler than talking head (1 angle, 1 framing, solid background)
- No B-roll clips needed. The backgrounds serve the visual variety role
- B-roll density setting does not apply to this format
- Background images must be sourced or created before production. Flag these in the reference material checklist
- Post-production is heavier than talking head (green screen keying, background timing, annotation placement)
- Speaker Veo scenes are simpler to generate (static framing, no angle changes, no product holds)
- Total duration typically 40-60s (longer than talking head due to evidence walkthrough)
