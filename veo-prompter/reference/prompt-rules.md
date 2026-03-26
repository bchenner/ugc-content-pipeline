# Veo 3.1 Prompt Rules
<!-- Extracted from Google AI for Developers documentation (ai.google.dev) -->
<!-- Replaces the 9.1MB PDF that was unreadable by tooling -->

---

## Model Specs

- **Frame rate**: 24fps
- **Duration**: 4s, 6s, or 8s. Must be 8s for 1080p, 4k, video extension, or reference images.
- **Aspect ratio**: 16:9 (landscape, default) or 9:16 (portrait)
- **Resolution**: 720p (default), 1080p, 4k. Higher resolution = higher latency.
- **Output**: 1 video per request
- **Audio**: Natively generated with the video (dialogue, SFX, ambient)
- **Watermark**: SynthID watermark embedded in all output
- **Latency**: 11 seconds min, up to 6 minutes at peak
- **Retention**: Generated videos stored 2 days, then deleted. Download locally.

---

## Input Modes

### Text-to-Video
Prompt only. No images needed.

### Image-to-Video
Single image as starting frame + text prompt. The image becomes the first frame and Veo animates from there.

### Reference Images (Veo 3.1 only)
Up to 3 images as "asset" guidance. Veo preserves subject appearance in the output. Good for character/product consistency across scenes.

### Frame Interpolation (First-to-Last Frame)
Supply a first image and a `lastFrame` image. Veo generates the transition between them. Gives precise control over shot composition at start and end.

### Video Extension
Extend a previous Veo-generated video by up to 7 seconds. Up to 20 extensions total. Extension finalizes the last second (24 frames) and continues the action. Requirements:
- Input must be from Veo generation (not arbitrary video)
- Max input length: 141 seconds
- Resolution: 720p only
- Aspect ratio: 9:16 or 16:9

---

## Prompt Structure

A good prompt covers these elements:

| Element | What It Controls | Examples |
|---------|-----------------|----------|
| **Subject** | The main focus of the video | Person, animal, object, cityscape |
| **Action** | What the subject does | Walking, turning head, running, picking up |
| **Style** | Creative/visual direction | Sci-fi, film noir, hyperrealistic, cartoon |
| **Camera** | Position and movement | Aerial view, eye-level, dolly shot, POV, tracking |
| **Composition** | Framing and shot type | Wide shot, close-up, single-shot, two-shot |
| **Focus/Lens** | Depth and lens effects | Shallow focus, deep focus, macro lens, wide-angle |
| **Ambiance** | Color and lighting mood | Blue tones, warm sunlight, golden hour, night |

---

## Audio and Dialogue

Veo 3.1 generates synchronized audio natively.

**Dialogue**: Use quotation marks for speech.
```
"This must be the key," he murmured.
```

**Sound effects**: Describe explicitly.
```
Tires screeching loudly, engine roaring.
```

**Ambient noise**: Describe the environment's soundscape.
```
Birds chirping, wind rustling through leaves, distant traffic.
```

**Voice extension caveat**: Voice cannot be effectively extended if it's not present in the last 1 second of the video.

---

## Negative Prompts

Do NOT use instructive language ("no," "don't," "avoid").

Instead, describe what you do not want as positive exclusions:
- Good: `"urban background, man-made structures"` (describes the unwanted thing)
- Bad: `"no buildings"` (instructive, less effective)

---

## Camera Movement Keywords

These terms trigger specific camera behaviors:

| Keyword | Effect |
|---------|--------|
| `aerial view` / `drone shot` | High overhead perspective |
| `eye-level` | Camera at subject's eye height |
| `top-down shot` | Directly overhead, looking down |
| `dolly shot` | Camera moves toward or away from subject |
| `tracking shot` | Camera follows the subject laterally |
| `POV` / `point-of-view` | Camera is the subject's eyes |
| `worms eye` | Very low angle, looking up |
| `close-up` | Tight framing on face/detail |
| `wide shot` | Full environment visible |
| `(thats where the camera is)` | Veo syntax for camera-aware processing |

---

## Ambiance and Lighting

Color and lighting language strongly affects mood:

| Term | Effect |
|------|--------|
| `warm tones` / `golden hour` | Warm, inviting feel |
| `cool blue tones` | Cold, clinical, or dramatic |
| `muted orange` | Nostalgic, retro warmth |
| `natural light` | Realistic, casual |
| `night` / `low light` | Dark, moody |
| `sunrise` / `sunset` | Directional warm glow |
| `overcast` | Soft, diffused, flat lighting |

---

## Descriptive Language Tips

- Use adjectives and adverbs to create vivid imagery
- Film terminology gives stylistic control (dolly, rack focus, anamorphic)
- Specify color palettes explicitly for mood
- Mention lighting conditions and direction
- Use directional terms for camera movement
- Combine multiple elements for cinematic results

---

## Person Generation

| Parameter | Value | Notes |
|-----------|-------|-------|
| `personGeneration` | `allow_all` | For text-to-video and video extension |
| `personGeneration` | `allow_adult` | For image-to-video, interpolation, reference images |

**Regional restrictions**: EU, UK, CH, and MENA locations are limited to `allow_adult` (Veo 3) or `dont_allow` / `allow_adult` (Veo 2).

---

## What Works Well

- Descriptive, specific prompts with cinematic language
- Combining multiple input types (text + images)
- Clear action descriptions with environmental context
- Specific color and lighting direction
- Audio cues with quotation marks for dialogue
- Camera movement terminology for composition control
- Enhancing facial details as a focus area

## Common Pitfalls

- Vague or generic descriptions produce generic results
- Instructional negatives ("no," "don't") are less effective than descriptive exclusions
- Conflicting style directions without clear prioritization
- Insufficient detail about desired motion and action
- Ignoring regional person-generation restrictions
- Attempting 1080p or 4k with durations under 8 seconds (not supported)

---

## Safety and Compliance

- All videos pass through safety filters and memorization checking
- Audio may trigger separate safety blocks (no charge if blocked)
- SynthID watermark is always applied
- Generated content must comply with Google's usage policies

---

## Example Prompt (from Google docs)

```
Create a short 3D animated scene in a joyful cartoon style. A cute creature
with snow leopard-like fur, large expressive eyes, and a friendly, rounded
form happily prances through a whimsical winter forest. The scene should
feature rounded, snow-covered trees, gentle falling snowflakes, and warm
sunlight filtering through the branches.
```

This works because it specifies: style (3D animated, joyful cartoon), subject (creature with specific features), action (prances), environment (winter forest with specific details), and ambiance (warm sunlight, snowflakes).
