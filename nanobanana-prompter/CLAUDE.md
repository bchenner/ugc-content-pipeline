# Image Prompt Architect

Generate image prompts for AI image generation (Gemini via Nanobanana API). Two modes: **plain text** for simplicity, **JSON** for detail and consistency.

## Reference Files

- `reference/prompt-examples.md` — Full prompt example library. **Consult before every prompt generation** to match structure and tone.
- `reference/prompt-examples.pdf` — Teaching document with 6 titled prompts and "Lessons Drawn" sections. The definitive guide to what works and why.
- `reference/prompting-guide.pdf` — Gemini API image generation docs. Pages 15-27 for photorealistic strategies.
- **Google Sheets**: `~/.claude/skills/gsheets/` — Read, write, format, and search Google Sheets. Invoke via `/gsheets` skill. Service account auth, known spreadsheet: Salvora Prehooks (ID: `13y_rw5s_7FlVhCHhKr0C9w7oPg9AWW9nPFRUG2YXJEU`).

---

## Core Principles

These rules override everything else. If a field reference or example contradicts these, follow these.

### Write Like a Person, Not a Spec Sheet

Prompts are creative briefs, not technical documentation. The model responds better to conversational language than camera specs.

**Do this:**
> "iPhone camera propped on a bathroom counter, good quality but not professional"

**Not this:**
> "iPhone 15 Pro rear camera, 26mm f/1.78 lens, 4K 30fps video frame, sensor noise in shadows, milky blacks"

### Describe Action, Not Appearance

Tell the model what the subject is *doing*, not how attractive they are. Give the model a character to play.

**Do this:**
> "playfully biting the straw of an iced green drink, nose scrunched"
> "half-sitting half-standing, flicking hair back with one hand"
> "mid-sentence, slight head tilt, explaining something"

**Not this:**
> "beautiful young woman posing with a calm yet playful smile"
> "standing gracefully with a serene expression"

### Tell the Model What It ISN'T

Negative boundaries are powerful for steering away from AI look:
- "NOT professional lighting"
- "not a studio, not luxury"
- "not over-processed, not airbrushed"

### Let Imperfections Happen

Don't describe perfect features. Describe clothing fit, fabric behavior, hair movement, body action — the model adds natural imperfections on its own. Over-describing skin texture ("clearly visible pores across nose, cheeks, and chin") often backfires into uncanny territory.

### Narrative Clutter = Realism

Small imperfect details signal "real" to the model:
- Hair tie on wrist, coffee ring stain on table, phone face-down on cushion
- Condensation on a bottle, scuffed shoes, a pen left on a notebook
- Masking tape on a skateboard, a crumpled receipt, a half-empty water glass

These are more powerful than any technical camera setting for making images look authentic.

### Anchor the Hands

Always give hands something to interact with — a surface, a prop, a body part:
- "hand resting on thigh", "fingers wrapped around coffee mug"
- "one hand on phone, other resting on counter"
- "head resting on hand, elbow propped on table"

Never let hands float freely. Never have hands clasped or interlocking (AI can't render this).

### Plain Fabrics Win

"No overt patterns" on clothing reduces AI rendering errors. Plain, solid-color fabrics render more convincingly than complex patterns, plaids, or prints. When in doubt, keep it simple.

### Lighting Must Be Pattern-Matchable

The model renders realistic lighting when it can pattern-match to real photos of that environment. Two approaches:

**Natural light** (always works): "soft natural daylight", "natural window light", "dim directional daylight entering from the left". The model has seen millions of real photos lit by windows and sunlight.

**Artificial light** (must be specific): Name the fixture placement + color temperature so the model can recall real photos with that lighting. "Overhead diffused light, neutral white" (retail store), "overhead diffused light, neutral white leaning slightly warm" (home studio). Never just "warm room light" — too vague, defaults to golden AI glow.

**Avoid**:
- Studio language: "key light", "fill light", "rim light", "bounce", "falloff" — even conversationally, these push toward professional setups
- Describing shadows or light ratios: "shadows on the right side of her face", "background darker than subject"
- Stacking "warm" across multiple fields (lighting + atmosphere + background) — if warmth is needed, put it in ONE place with restraint

---

## AI Look Anti-Patterns

These make images look generated. Avoid them in all prompts.

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Beauty descriptors ("beautiful", "stunning", "porcelain", "flawless") | Pushes model toward smooth, textureless AI skin |
| Generic pose words ("posing elegantly", "standing gracefully") | Produces stiff, symmetric, obviously-AI poses |
| Skin quality descriptions ("porcelain-white skin", "smooth complexion") | Model gives natural texture by default — describing it forces unnatural smoothness |
| Technical camera specs (f-stops, focal lengths, aperture values) | Model doesn't understand these — they add noise without improving output |
| Detailed lighting diagrams (key/fill/rim with angles and color temps) | Over-constrains the model. "Warm light from the left" works better than a 4-paragraph lighting setup |
| Hex color palettes (#E0C8B8, #3B2E2A) | Model doesn't reliably interpret hex codes. Use plain color words |
| Over-detailed micro_details on every object | Diminishing returns. Reserve micro_details for the 1-2 most important items |
| `negative_prompt` JSON blocks with 10+ forbidden elements | A few key `--no` items work. Long forbidden lists add noise |
| Subject not interacting with environment | Person feels pasted in. They should be *doing something* in the space |

---

## Three Prompt Modes

### 1. Plain Text

Single-line prompt. Use when simplicity is key or for quick iterations.

Structure:
```
[Medium & Style] + [Subject & Action] + [Environment] + [Lighting] + [Camera] + parameters
```

**Example:**
```
Raw unedited smartphone selfie, a young person with messy hair and a tired smile wearing an old grey oversized hoodie, holding phone in one hand, looking right into the lens, cluttered living room with unmade couch, mixed natural window light, wide-angle front camera distortion --no professional camera, bokeh, makeup, 3d render --ar 9:16
```

### 2. JSON

Structured prompt for detailed, consistent outputs. **Two formats — two different paradigms:**

**Compact JSON** — a creative recipe. For single-subject scenes, selfies, outfits, portraits, UGC content:
```json
{
  "subject": {},
  "face": {},
  "hair": {},
  "clothing": {},
  "accessories": {},
  "photography": {},
  "background": {}
}
```

**Full Analytical JSON** — a scene graph. For complex multi-object scenes, product placement, brand text, eCommerce, reverse-engineered images:
```json
{
  "meta": {},
  "character_reference": {},
  "global_context": {},
  "composition": {},
  "subject": {},
  "objects": [],
  "text_ocr": {},
  "semantic_relationships": []
}
```

**Don't mix paradigms.** Compact is a recipe — conversational, minimal, vibes-driven. Full Analytical is a scene graph — precise, object-oriented, spatially explicit. Using scene graph verbosity in a compact prompt (or recipe casualness in a scene graph) produces worse results than committing to one.

| Format | Use For |
|--------|---------|
| **Compact** | Single subject, simple environment, lifestyle/fashion/selfie, outfit checks, UGC |
| **Full Analytical** | Multiple objects needing spatial precision, product with brand text, complex multi-element compositions |

### 3. Modification Mode

Takes an existing base image as reference and applies a small change via plain text instruction. No JSON, no full prompt. The base image already defines the scene, subject, environment, lighting, and camera. You only describe what changed.

**When to use:**
- End frames (base = start image, instruction = what shifted)
- Product placement (base = speaking scene image + product photo, instruction = how the subject holds/interacts with the product)
- Angle variations (base = existing scene, instruction = new framing)
- Any image that is a small delta from an existing one

**Input:**
1. Base image uploaded as reference (the start frame or existing scene)
2. Optional: additional reference image (product photo, prop photo)
3. Plain text instruction describing ONLY what changed

**Examples:**
```
The speaker holds the product bottle in her right hand, resting on the desk surface.
```
```
She leans slightly forward, looking down at the open product box on the table.
```
```
Same scene but framed as a tighter close-up, chest and above.
```

**Rules:**
- Keep instructions short and specific (1-2 sentences)
- Don't re-describe the scene, subject, environment, or lighting. The base image handles all of that.
- Focus on the delta: what moved, what appeared, what changed position
- If a product photo is provided as a second reference, the model uses it for accurate product appearance
- Anchor hands to the product or a surface (same rule as always)

| Variation Type | Base Image | Additional Reference | Instruction Focus |
|---------------|------------|---------------------|-------------------|
| End frame | Start image | — | Posture shift, expression change, gesture |
| Product hold | Speaking scene image | Product photo | How subject holds/displays the product |
| Angle shift | Existing scene | — | New framing (tighter, wider, different angle) |

---

## Parameters

Parameters go at the end of plain-text prompts.

| Parameter | Values | Notes |
|-----------|--------|-------|
| `--ar` | `1:1` (default), `9:16` (vertical), `16:9` (cinematic) | Always 9:16 for TikTok/Reels |
| `--no` | comma-separated list | What to avoid: `--no professional lighting, makeup, 3d render` |
| `--s` / `--stylize` | 25-50 (strict) to 750 (artistic) | **Keep low for UGC.** High values = "art" not reality |

---

## Compact Format Guide

The compact format is conversational. Write it like you're describing the image to a friend, not filling out a database.

### `subject`
The scene description and what the person is doing. This is the most important field — get the action and energy right.

```json
{
  "description": "A young woman taking a mirror selfie, playfully biting the straw of an iced matcha latte, nose scrunched",
  "age": "young adult",
  "expression": "playful, nose scrunched, biting straw"
}
```

Optional: `"mirror_rules": "ignore mirror physics for text on clothing, display text forward and legible to viewer"` — use for mirror selfies where brand logos need to be readable.

### `face`
Keep it minimal. The reference image handles identity. Focus on makeup level and let natural texture happen on its own.

```json
{
  "preserve_original": true,
  "makeup": "natural sunkissed look, glowing skin, nude glossy lips"
}
```

**Don't** list pores, undereye circles, oily shine, blemishes — the model generates natural skin texture by default when you don't over-describe it.

### `hair`
Simple — color and style. Add movement if relevant.

```json
{
  "color": "brown",
  "style": "long straight hair falling over shoulders, a few flyaways"
}
```

### `clothing`
Plain fabrics, specific garment types. Avoid patterns.

```json
{
  "top": {
    "type": "oversized hoodie",
    "color": "light heather grey",
    "details": "soft fleece, relaxed fit, hood falling back"
  },
  "bottom": {
    "type": "denim jeans",
    "color": "light wash blue",
    "details": "relaxed fit, visible button fly"
  }
}
```

### `accessories`
Layer specific items. Trend stacking (multiple distinct accessories) makes content feel culturally current.

```json
{
  "headwear": { "type": "olive green baseball cap", "details": "white NY logo, headphones worn over the cap" },
  "jewelry": {
    "earrings": "large gold hoop earrings",
    "necklace": "thin gold chain with cross pendant",
    "wrist": "gold bangles and bracelets mixed"
  },
  "prop": { "type": "iced beverage", "details": "plastic cup with iced matcha latte and green straw" }
}
```

### `photography`
Keep it simple and conversational. 5-6 lines max. No f-stops, no focal lengths.

```json
{
  "camera_style": "smartphone mirror selfie aesthetic",
  "angle": "eye-level mirror reflection",
  "shot_type": "waist-up composition",
  "aspect_ratio": "9:16 vertical",
  "texture": "sharp focus, natural indoor lighting, social media realism, clean details"
}
```

**"Social media realism"** = bright, flattering, high-def, aspirational but attainable. It's reality with a filter.
**"Raw photorealism"** = gritty, noisy, imperfect. iPhone video frame quality.

Choose the right one for the content type. Don't default to raw for everything.

### `background`
Environment as a short list. Don't over-describe — the model fills in believably when given a setting + a few key elements.

```json
{
  "setting": "bright casual bedroom",
  "wall_color": "plain white",
  "elements": ["bed with white textured duvet", "leopard print throw pillow", "distressed white nightstand"],
  "atmosphere": "casual lifestyle, cozy, spontaneous",
  "lighting": "soft natural daylight"
}
```

---

## Full Analytical Format Guide

This is a scene graph — an object-oriented spatial description. Every element gets its own ID, attributes, and spatial position. Use this when objects need to not bleed into each other and spatial relationships are critical.

### Key Concepts

**Object ID De-entanglement**: Separate objects prevent texture/adjective bleed. "Worn" on a skateboard (obj_007) won't make the person (obj_001) look worn. This is the primary reason to use full analytical over compact.

**Semantic Relationships as Glue**: Listing objects isn't enough — define their interaction. "Subject is squatting directly over the skateboard" prevents the skateboard from floating or merging into the ground.

**Foreshortening Must Be Named**: AI struggles with extreme angles. Explicitly name perspective effects: "foreshortening", "top-down", "low-angle distortion." This guides the geometry engine.

### Fields

#### `meta`
```json
{
  "image_quality": "High",
  "image_type": "Photo",
  "aspect_ratio": "9:16"
}
```

#### `character_reference`
```json
{
  "instruction": "Use the attached reference sheet as the absolute ground truth for the subject's facial features, skin texture, and body proportions. The output must be a 1:1 match of the character provided."
}
```

#### `global_context`
Scene description + lighting. Keep lighting simple — a source, direction, and quality. No hex color temperatures.

```json
{
  "scene_description": "A candid selfie taken on an outdoor patio, subject holding a supplement bottle at shoulder height, residential house in background",
  "time_of_day": "Daytime",
  "lighting": {
    "source": "Natural sunlight",
    "direction": "Frontal, diffused",
    "quality": "Soft, even"
  }
}
```

#### `composition`
Camera angle and framing. Use plain descriptions, not lens specs.

```json
{
  "camera_angle": "Eye-level selfie",
  "framing": "Close-up, subject fills most of frame",
  "depth_of_field": "Deep — subject and immediate background in focus",
  "focal_point": "The product bottle and subject's face"
}
```

#### `subject`
Pose, clothing, and position. Same anti-patterns apply — action over appearance.

```json
{
  "pose": {
    "body_position": "Standing",
    "gesture": "Left hand holding bottle near shoulder height, right arm extended forward (selfie)",
    "head_angle": "Facing camera",
    "expression_mood": "Neutral, relaxed"
  },
  "clothing": {
    "outfit_description": "Plain white hoodie, casual loungewear",
    "colors": ["White"],
    "accessories": ["Tortoiseshell round glasses", "Multiple small gold hoop earrings"]
  },
  "position_in_frame": "Center",
  "prominence": "Foreground"
}
```

#### `objects[]`
Each object gets its own ID. Use `micro_details` only on the 1-2 most important objects (usually the product). Don't micro-detail everything.

```json
{
  "id": "obj_001",
  "label": "Supplement Bottle",
  "category": "Product",
  "location": "Mid-right, held by subject",
  "prominence": "Foreground",
  "visual_attributes": {
    "color": "Translucent cyan/blue with white cap",
    "texture": "Smooth plastic",
    "state": "New"
  },
  "micro_details": [
    "White screw-top lid with vertical ridges",
    "Label wraps around bottle",
    "Gummies visible inside through translucent plastic"
  ]
}
```

#### `text_ocr`
When brand text must appear on products. Use `mirror_rules` in compact format instead for mirror selfies.

```json
{
  "present": true,
  "content": [
    { "text": "ASHWAGANDHA", "location": "Bottle label center", "font_style": "Sans-serif uppercase bold", "legibility": "Clear" }
  ]
}
```

#### `semantic_relationships`
The spatial glue. Define how objects interact with each other and the subject. Critical for preventing floating objects and merging.

```json
[
  "Subject is holding Supplement Bottle in left hand",
  "Subject is positioned in front of Sliding Glass Door",
  "Glasses are worn on Subject's face"
]
```

---

## Character Consistency

For maintaining the same character across multiple images:

1. Add `character_reference` block to the JSON:
```json
"character_reference": {
  "instruction": "Use the attached reference sheet as the absolute ground truth for the subject's facial features, skin texture, and body proportions. The output must be a 1:1 match of the character provided."
}
```

2. Set `face.preserve_original: true` on the subject (Identity Lock Protocol)

3. The reference sheet image is attached alongside the prompt as a generation input

**Don't over-describe the face when using a reference** — the image handles identity. Focus on expression and action instead.

### Generating a Character Reference Sheet

Use this plain text template to generate a new character reference sheet from scratch. Fill in the bracketed fields based on the character description.

```
A character reference sheet of a [age range] [ethnicity/background] [gender], [specific skin tone], [hair color] hair [hair style], [distinctive eyebrow description], [eye color] eyes, [face shape and defining facial features — jawline, nose, cheekbones, etc.]. Three vertically stacked photos filling the entire frame edge to edge with no gaps, no borders, no dividing lines between them. Top third: front-facing headshot, relaxed neutral expression, looking directly at camera. Middle third: three-quarter view, head turned slightly to the right. Bottom third: full side profile facing right. All three shots are shoulders-up, wearing a plain [color] [simple top — e.g. black crewneck t-shirt]. [Signature accessories — glasses, earrings, necklace, etc.]. No makeup, natural bare skin. Shot on a smartphone against a plain light grey wall, natural window light from the left, social media realism. --ar 9:16 --no borders, frames, dividing lines, white space between photos, text, labels
```

**Key rules for reference sheets:**
- **Always plain text** — this is a utility image, not a creative scene
- **Describe the face in detail** — this is the one case where face topology is correct, because there's no reference image to rely on
- **Include signature accessories** (glasses, earrings, jewelry) — these are part of the character's identity
- **Keep clothing plain and neutral** — plain black or white t-shirt, nothing distracting
- **Natural window light + smartphone** — even utility images need a real light source and camera anchor to avoid AI skin
- **Never use "flat even lighting"** — that's what AI does by default and reinforces the artificial look

---

## Image-to-JSON (Reverse Engineering)

Two methods:

### Standard Image-to-JSON
Analyze the image and produce a full analytical JSON. This is the scene graph paradigm — capture every observable element with object IDs, spatial positions, and relationships.

### Character Consistency Extraction
Extract the character's distinguishing features for reuse: face structure, skin texture, body proportions, signature accessories. Output a character reference block for future prompts.

---

## Aesthetic Modes

Different content types need different aesthetic approaches:

| Content Type | Aesthetic | Photography Texture |
|-------------|-----------|-------------------|
| UGC / TikTok / raw feel | Raw photorealism | "iPhone video frame, soft focus, video noise in shadows, slightly desaturated" |
| Lifestyle / fashion / aspirational | Social media realism | "Sharp focus, natural indoor lighting, social media realism, clean details" |
| Retro / nostalgic | Named camera aesthetic | "Canon IXUS point-and-shoot, direct flash, warm skin, dark background falloff" |
| Clean girl / viral slideshow | Curated realism | "Bright daylight, crisp details, styled but spontaneous feel" |
| **Storytelling / emotional narrative** | Lo-fi intimate | "Handheld iPhone, natural light only, no filters, no color grading, raw and unpolished" |

**Social media realism ≠ raw photorealism.** They're different aesthetics. Social media realism is bright, flattering, aspirational. Raw photorealism is gritty and imperfect. Match the aesthetic to the content goal.

### Storytelling Visual Style <!-- date: 2026-03 -->

When generating images for Pattern Q (Long-Form Personal Storytelling) scripts, use these visual rules:

**Opening frames (first 3 seconds)**:
- Full-screen close-up — eyes, skin, expression fill the frame
- Show exhaustion, dark circles, raw emotion. No makeup, no filters
- Lo-fi iPhone aesthetic: handheld, natural light, slight motion blur acceptable

**Symptom visuals**:
- Tired faces with visible dark circles
- Sitting up in bed at 3AM — dim blue-ish light, disheveled
- Sitting alone in car at night — dashboard glow, isolation
- No stock footage look, no filters, no brand overlays

**Key rules**:
- NO beauty descriptors at all — not "natural beauty" or "effortless." This is raw.
- Narrative clutter is critical — crumpled tissues, half-empty water glass, phone face-down
- Lighting must feel accidental (overhead kitchen light, bedside lamp, car dome light)
- Expression should be mid-emotion, not posed — caught crying, staring blankly, looking away

---

## Quality Checklist

Before delivering any prompt:

- [ ] Aspect ratio specified (default 9:16 for social)
- [ ] Subject is doing something specific — not just "standing" or "smiling"
- [ ] Hands are anchored (holding something, resting on a surface, in a pocket)
- [ ] Clothing is plain/solid colors (no complex patterns unless intentional)
- [ ] No beauty descriptors ("beautiful", "stunning", "porcelain", "flawless")
- [ ] Photography block is 5-6 lines of plain language (no f-stops, no focal lengths)
- [ ] Environment is a short list of elements, not nested object arrays
- [ ] At least 1-2 narrative clutter items for realism
- [ ] Face block is minimal — `preserve_original: true` + makeup level only
- [ ] Lighting is 1-2 sentences, not a multi-section diagram

See `reference/prompt-examples.md` for the full example library.
