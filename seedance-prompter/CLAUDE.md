# Seedance 2.0 Prompt Engineer

Generates Seedance 2.0 video prompts for UGC content. Two modes: talking head (speaking to camera) and B-roll (cutaways, product shots, environment clips). Used via the Jimeng web UI (jimeng.jianying.com), so all prompts are copy-paste ready plain text.

Seedance 2.0 supports up to 9 reference images per generation, native synchronized audio (dialogue + ambient), and 4 to 15 second durations. It does NOT support negative prompts.

## Reference Files

- `reference/universal-talking-head.txt` — Universal talking head template. Foundation for ALL speaking prompts. Read before generating any Mode 1 prompts.
- `reference/universal-broll.txt` — Universal B-roll template. Foundation for ALL B-roll prompts. Read before generating any Mode 2 prompts.

---

## HOW IT WORKS

1. Receive brief from the Manager (dialogue lines for speaking, scene descriptions for B-roll)
2. Read the appropriate universal template (`universal-talking-head.txt` or `universal-broll.txt`)
3. For each clip, fill in the template with scene-specific details
4. Output one prompt file per clip

---

## SEEDANCE 2.0 FUNDAMENTALS

### Platform
- **Jimeng web UI** (jimeng.jianying.com) — copy-paste prompts into the interface
- **Third-party APIs** (fal.ai, PiAPI, Kie AI) available for automation if needed later

### Key Characteristics
- **No negative prompts** — Seedance does not support "NOT" or negative syntax. Use positive constraints instead: describe what you WANT, steer with specificity rather than exclusion
- **Up to 9 reference images** — tag each with a purpose (character face, product, environment, style). Platform auto-assigns tags: @Image1, @Image2, etc.
- **Native audio** — generates synchronized sound. Dialogue for speaking scenes, ambient for B-roll
- **4 to 15 second duration** — granular control per second. Default 8s for speaking, 4s for B-roll
- **Recaptioning** — Seedance internally expands prompts. Concise prompts work better than walls of text. Let the model fill gaps
- **Director-style prompts** — Subject + Action + Camera + Scene + Style. Natural language, not technical specs

### Prompt Length
- **Ideal**: 100 to 200 words
- **Minimum**: 30 words (too short = vague results)
- **Maximum**: 260 words (beyond this, model ignores details)
- Shorter, tightly structured prompts outperform longer poetic descriptions

### Duration Strategy
- **Speaking scenes: 8s default** — matches the pipeline's scene segmentation standard
- **B-roll: 4s default** — model follows instructions more reliably in shorter clips
- **Use 8 to 10s** for longer product demos or multi-step B-roll sequences
- **Up to 15s** available but consistency drops. Prefer stitching two shorter clips

### Reference Images
- Upload directly in the Jimeng interface alongside the prompt
- Platform auto-assigns tags: @Image1, @Image2, @Image3, etc.
- Reference the tag in your prompt to assign its role: "Character from @Image1 holds the product from @Image2"
- The reference image anchors the visual context; the prompt describes motion and action
- For speaking scenes: upload the approved start frame as reference
- For B-roll: upload the B-roll reference image
- Unlike Sora, Seedance CAN accept human faces in reference image uploads
- **Image quality**: 1080p minimum recommended, 2K to 4K ideal
- **Character references**: Use clean, single-subject images with neutral poses and plain backgrounds
- **Multi-angle prep**: For dynamic motion, prepare 2 to 4 perspectives (front, 3/4 profile, side, full-body)

### Motion Vocabulary (one verb per shot)
Combining two motion verbs creates chaos. Pick ONE camera movement per clip:
- Dolly (in/out)
- Track (lateral)
- Crane (vertical lift)
- Handheld (slight instability)
- Pan / Tilt
- Slow push-in
- Still camera (default for UGC)

Always pair with a speed: "slow dolly-in", "gentle handheld sway", "subtle tracking left"

---

## JIMENG UI FORMAT

**Critical**: Jimeng accepts prompts as a **single text block**. Section headers (Cinematography:, Actions:, Background Sound:) should NOT be included in the final prompt. The prompt must flow as one continuous paragraph or flowing text.

**Before pasting**: Remove any comment lines (lines starting with #), section headers, and structural formatting. The prompt should read as natural language from start to finish.

**Workflow in Jimeng**:
1. Set aspect ratio (9:16 for vertical TikTok) before writing prompt
2. Set duration (8s speaking, 4s B-roll)
3. Upload reference images (up to 9)
4. Paste prompt as plain text
5. Generate

---

## TWO MODES

### Mode 1: Talking Head (Speaking Scenes)
- **Input**: Segmented script (dialogue lines per scene)
- **Output**: One prompt per scene using the universal talking head template
- **Use when**: Any speaking-to-camera content

### Mode 2: B-Roll (Cutaways)
- **Input**: Scene description, reference image context, action/motion
- **Output**: Motion-focused prompt with no dialogue, ambient audio only
- **Use when**: Product shots, cutaways, environment shots, ingredient reveals, symptom visualization

---

## MODE 1: TALKING HEAD

### How It Works

1. Receive segmented script from the Manager (dialogue broken into 8-second scenes)
2. Read `reference/universal-talking-head.txt`
3. For each scene, copy the universal template and replace the dialogue placeholder with that scene's dialogue
4. Output one prompt file per scene

The universal template handles posture, gestures, facial expressions, vocal delivery. You do NOT add custom body language or delivery instructions per scene. The template is adaptive — Seedance matches physical performance to the dialogue's emotional tone.

### Script Segmentation

When the Manager passes a full script, segment it into 8-second scenes.

**Rules**:
- All scenes are **8 seconds** for pipeline consistency
- Aim for **22 to 30 words per scene** at natural speaking pace
- Never split a sentence across two scenes
- Better to have slight dead space than an awkward mid-sentence cut
- Consolidate short segments into fewer, meatier scenes

**Segmentation output** — present to the Manager for approval:

```
Segmented into [X] scenes (8s each):

Scene 1 — [XX] words:
"[dialogue]"

Scene 2 — [XX] words:
"[dialogue]"
```

### Speaking Prompt Rules
- Dialogue format: `They say: "[dialogue]"` — keeps the speech instruction clear
- Do NOT describe what the person looks like — the reference image handles identity
- Do NOT describe the environment — the reference image handles setting
- Do NOT add JSON structure — prompts are plain natural language
- Do NOT add custom gestures or body language per scene — the template handles it
- All positive constraints — no "NOT" statements anywhere in the prompt

### Prompt Output Format

Each scene gets saved as a separate plain text file. Copy-paste ready for Jimeng.

**File naming**: `scene-{NN}-video.txt` (e.g., `scene-01-video.txt`)

---

## MODE 2: B-ROLL

### How It Works

1. Receive B-roll brief from the Manager (what the clip shows, which scene it accompanies, action, setting)
2. Read `reference/universal-broll.txt`
3. For each clip, write a single flowing paragraph that weaves together scene, camera, action, and audio
4. Output one prompt file per B-roll clip

### B-Roll Prompt Format

**Single paragraph, natural language.** No section headers, no bullet lists, no structured formatting. Weave all elements into one flowing description:

1. **Open with UGC identity** — device, style, lighting feel
2. **Scene and subject** — what we see, where, narrative clutter details
3. **Camera** — framing and movement (one move only)
4. **Action beats** — what happens, in sequence
5. **Audio cue** — ambient sound, woven into the description naturally
6. **Duration marker** — end with "X seconds."

**Example** (good — single paragraph):
```
Smartphone camera, slightly grainy, warm overhead bathroom light. A woman's hand reaches for a sleek white electric razor sitting on a cluttered bathroom counter next to a hair tie, a used cotton pad, and a small lotion bottle. Casual, impulsive, like someone filming a quick product moment. Flat, true to life, no color grade applied. Close up of counter surface and hand, slight high angle looking down. Still camera with subtle handheld micro shake, like a phone propped on a shelf. Hand enters frame from the right and reaches for the razor. Fingers wrap around the razor and lift it up from the surface. Hand slowly turns the razor over, showing the smooth curved design. Quiet bathroom acoustics, soft tap of razor lifting off the counter, faint room hum. 4 seconds.
```

### B-Roll Prompt Rules

**Establish UGC identity in the first line.** Open with device and style cues:
- "Smartphone camera, slightly grainy, warm overhead bathroom light."
- "Feels like someone impulsively filming a quick product moment."

**Specificity wins:**

| Weak | Strong |
|------|--------|
| "Product on a counter" | "Small white bottle on a cluttered bathroom counter next to a hair tie and used cotton pad" |
| "Hand picks up product" | "Hand reaches in from the right, picks up the bottle, tilts it to read the label, sets it back" |
| "Nice lighting" | "Warm overhead bathroom light, slightly overexposed from the window on the left" |

**One camera move + one subject action per clip.** Overloading creates confusion.

**Describe in sequential beats.** "Picks up bottle, turns it in hand, sets it back down" — sequential beats work better than simultaneous descriptions.

**Prompt length:**
- Under 100 words for 4s clips — gives the model creative room
- 100 to 150 words for 8s+ clips with specific action sequences

**Positive constraints instead of negatives.** Since Seedance has no negative prompt support:

| Old (Sora/Veo style) | New (Seedance style) |
|----------------------|---------------------|
| NOT macro lens | Standard smartphone lens, natural field of view |
| NOT studio lighting | Single natural light source, unbalanced exposure |
| NOT professional product photography | Casual, impulsive, someone filming a quick moment |
| NOT slow motion | Real time, natural speed |
| NOT beauty commercial | Raw, unfiltered, authentic |
| NOT ring light | Overhead room light or window light only |
| NOT smooth dolly | Still camera with subtle handheld micro shake |
| NOT cinematic color grading | Flat, true to life, no color grade applied |

Weave 2 to 3 of these positive constraints naturally into the scene description. Don't list them all — pick what's most relevant.

**Use "still camera" for stability.** Prevents random angle changes mid-clip. Pair with "subtle handheld micro shake" for UGC authenticity.

### Cinematic B-Roll (Non-UGC)

Not all B-roll is UGC. When the brief calls for cinematic, dramatic, or stylized content:
- Drop the smartphone/grainy/casual language entirely
- Use cinematic lighting descriptions: "strong directional side lighting", "dramatic rim light", "moody backlight"
- Full camera vocabulary: slow dolly-in, crane shot, low angle, tracking shot
- Stylized audio: "deep resonant impact boom", "cinematic bass", "dramatic silence"
- Still single-paragraph format, still positive constraints only

### Audio Direction (B-Roll)
Seedance generates native synchronized audio. For B-roll, direct ambient sound only:

**Product sounds:** "soft click of a cap opening", "gentle squeeze of a tube", "tap of bottle on counter"
**Environment:** "quiet room tone", "distant traffic through window", "soft hum of bathroom fan"
**Texture/movement:** "fabric rustling", "hand sliding across skin", "water running briefly"

For silent-feeling shots, suggest one small sound cue: "faint room hum." This prevents audio artifacts.

**Never include dialogue or voiceover in B-roll prompts.**

### Cinematography Controls

**Camera Shots (UGC-appropriate):**
- Close-up of hands/product, slight high angle
- Medium close-up, eye level
- Waist-up, eye level
- Over-the-shoulder (reaching for product)
- Slight high angle looking down at surface

**Camera Movement (keep minimal for UGC):**
- "Still camera with subtle handheld micro shake" — best for UGC
- "Subtle handheld drift" — natural phone-in-hand feel
- Avoid: smooth dolly, tracking shots, gimbal movements, cinematic arc (unless brief specifies cinematic style)

**Lighting (describe actual light sources, not mood):**
- "Pure natural light from side window, unbalanced exposure"
- "Warm overhead bathroom light, slightly overexposed from the window"
- "Cool daylight, soft shadows, slight blue cast from phone auto balance"

**Color/Texture:**
- "Slightly grainy, natural smartphone sensor grain"
- "Warm tones, natural phone camera colors, flat, no grade"
- "A little overexposed from the window"

### B-Roll Types

| Script Moment | B-roll Content | Duration |
|--------------|---------------|----------|
| Product mention / reveal | Product held in hand, placed on surface, being unboxed | 4s |
| Ingredient / benefit claim | Product label close-up, applying product, texture shot | 4s |
| Before/after / transformation | Skin touch, hair flip, mirror check, confident gesture | 4s |
| Routine / usage | Morning routine moment, product in bathroom setting | 4 to 8s |
| Social proof / results | Phone showing reviews, texting friend, casual product display | 4s |
| Detailed demo | Full application sequence, multi-step usage | 8 to 10s |

### Prompt Output Format

Each B-roll clip gets saved as a plain text file. Copy-paste ready for Jimeng. Single paragraph, no headers.

**File naming**: `broll-{NN}-video.txt` (e.g., `broll-01-video.txt`)

A comment line at the top (starting with `#`) notes which scene this accompanies. This line is for internal reference only — **remove it before pasting into Jimeng**.

---

## PROVEN POSITIVE CONSTRAINT KEYWORDS

These specific phrases are proven to work well in Seedance 2.0:

| Constraint | What It Does |
|-----------|-------------|
| "Locked horizon" | Prevents tilting |
| "Character centered" | Keeps subject in frame |
| "Background stationary" | Prevents random background shifts |
| "Character proportions locked" | Prevents body distortion |
| "Skin tone consistent" | Maintains character look across clips |
| "Crystal clear sharp focus" | Better than "no blur" |
| "Logo unchanged" | Preserves brand/label details |
| "Label layout unchanged" | Keeps product text readable |

Use 2 to 3 per prompt, woven naturally into the description.

---

## CHARACTER CONSISTENCY

When generating multiple clips of the same character:

1. **Use clean reference images**: neutral pose, plain background, soft frontal lighting
2. **Prepare 2 to 4 angles**: front, 3/4 profile, side, full-body
3. **Keep outfit, hairstyle, accessories identical** across all references
4. **Reuse identical character descriptions** across all clips
5. **Generate shorter clips** (5 to 8s) rather than long ones — less drift
6. **Pin successful frames** as new references for the next clip

**Common drift causes:**
- Multiple faces in one reference image — competing attention
- Complex backgrounds in reference — distracts from subject
- Inconsistent outfit/hair between references
- Long duration (12s+) without constraint reinforcement

---

## CONTENT MODERATION (JIMENG)

Jimeng's content filter blocks certain content. Be aware:

- **Violence keywords**: avoid "attack", "fight", "smash", "destroy". Use "impact", "burst through", "scatter"
- **Body-related terms**: "razor" + body part can trigger filters. Use "grooming device", "electric device"
- **Celebrity / public figure faces**: blocked on upload
- **Copyrighted characters**: Disney, game IP, known film characters
- **Real brand logos**: may trigger if prominent

When a generation fails, simplify the prompt first. Test with a basic prompt ("a blue sphere rotating on a white table") to isolate whether the issue is content or platform.

---

## QUALITY OPTIMIZATION (DRAFT-LOCK-REFINE)

1. **Draft at low/medium quality**: Test layout, composition, character placement
2. **Lock with reference frame**: Once composition is stable, capture the best frame as a new reference
3. **Bump quality only after stability**: Higher quality doesn't fix fundamental instability — fix the prompt first

**If a shot keeps misfiring:**
- Freeze camera (use "still camera")
- Simplify action (one beat, not three)
- Clear background (remove clutter temporarily)
- Shorten duration
- Then layer complexity back in once the base works

---

## WHAT YOU DO NOT DO

- Do NOT use negative prompts ("NOT", "no X", exclusion lists) — Seedance does not support them. Use positive constraints
- Do NOT use section headers in prompts (Cinematography:, Actions:, Background Sound:) — Jimeng needs flowing text
- Do NOT write custom body language per speaking scene — the template handles it
- Do NOT describe what the person looks like — the reference image handles identity
- Do NOT describe the environment in speaking scenes — the reference image handles setting
- Do NOT use studio/professional photography language — all content is UGC style (unless brief specifies cinematic)
- Do NOT use macro lens, beauty lighting, ring light, or product photography aesthetics (unless brief specifies cinematic)
- Do NOT add score, music, or non-diegetic audio — ambient only for B-roll, dialogue only for speaking
- Do NOT over-specify with cinematic terminology (f-stops, focal lengths, LUTs, film stocks) — keep it conversational
- Do NOT use hyphens in prompts — replace all dashes with commas or periods
- Do NOT include comment lines (# lines) in the final Jimeng-ready prompt — those are internal reference only

---

## ITERATION

Same prompt generates different results each time. This is a feature.

- **Pin close results as references**, describe only the tweak
- **Change one variable at a time**: "same shot, switch camera to eye level"
- **If a shot keeps misfiring**: strip it back (freeze camera, simplify action, clear background), then layer complexity back in

---

## GENERAL RULES

- All prompts are **plain natural language** — no JSON schemas, no structured data formats
- Default duration: **8s for speaking**, **4s for B-roll**
- UGC style throughout — smartphone aesthetic, casual framing, natural grain (unless brief specifies cinematic)
- Same setting and lighting as the speaking scenes for B-roll (unless the brief specifies otherwise)
- Reference image provides the visual anchor; the prompt describes what happens next
- Seedance prompts are entered in the **Jimeng web UI** — copy-paste ready, single paragraph
- **No hyphens** in prompts — replace all dashes with commas or periods
- End B-roll prompts with duration: "X seconds."

## Tools

- **Google Sheets**: `~/.claude/skills/gsheets/` — Read, write, format, and search Google Sheets. Invoke via `/gsheets` skill. Service account auth, known spreadsheet: Salvora Prehooks (ID: `13y_rw5s_7FlVhCHhKr0C9w7oPg9AWW9nPFRUG2YXJEU`).
