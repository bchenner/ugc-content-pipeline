# Veo 3 Prompt Engineer

Generates Veo 3 video prompts for UGC-style content. Two modes: talking head and B-roll.

## Reference Files

- `reference/universal-talking-head.txt` — The universal talking head prompt template. This is the foundation for ALL talking head video prompts. Read it before generating any Mode 1 prompts.
- `reference/speaking-template.md` — Research-backed guide on body language, gestures, facial expressions, and vocal delivery for speaking-to-camera videos. Supplementary reference.
- `reference/veo-3.1-prompt-guide.pdf` — Official Veo 3.1 prompting best practices and technical specs.
- **Google Sheets**: `~/.claude/skills/gsheets/` — Read, write, format, and search Google Sheets. Invoke via `/gsheets` skill. Service account auth, known spreadsheet: Salvora Prehooks (ID: `13y_rw5s_7FlVhCHhKr0C9w7oPg9AWW9nPFRUG2YXJEU`).

---

## TWO MODES

### Mode 1: Talking Head (Default)
- **Input**: Segmented script (dialogue lines per scene)
- **Output**: One prompt per scene, each using the universal talking head template with the scene's dialogue inserted
- **Use when**: Any speaking-to-camera content — podcast, educational, sales, UGC

### Mode 2: B-Roll
- **Input**: Scene description, start frame, optional end frame
- **Output**: Motion-focused prompt with no dialogue
- **Use when**: Product shots, cutaways, environment shots, transition clips
- **Status**: Template TBD — will be built separately

---

## MODE 1: TALKING HEAD

### How It Works

1. Receive segmented script from the Manager/Script Writer (dialogue broken into 8-second scenes)
2. Read `reference/universal-talking-head.txt`
3. For each scene, copy the universal template and replace `___REPLACE THIS WITH YOUR DIALOGUE___` with that scene's dialogue
4. Output one prompt file per scene

That's it. The universal template handles everything — posture, gestures, facial expressions, vocal delivery, camera, grain, negative prompts. You do NOT add custom body language, gestures, or delivery instructions per scene. The template is designed to be adaptive — Veo matches the physical performance to whatever the dialogue's emotional tone is.

### Script Segmentation

When the Manager passes a full script, segment it into 8-second scenes before generating prompts.

**Rules**:
- All scenes are **8 seconds** (only supported duration with reference images)
- Aim for **22-30 words per scene** at natural speaking pace
- Never split a sentence across two scenes
- Better to have slight dead space than an awkward mid-sentence cut
- Consolidate short segments into fewer, meatier scenes
- Scenes with fewer words will naturally get filled by gesture beats from the template

**Segmentation output** — present to the Manager for approval:

```
Segmented into [X] scenes (8s each):

Scene 1 — [XX] words:
"[dialogue]"

Scene 2 — [XX] words:
"[dialogue]"

Scene 3 — [XX] words:
"[dialogue]"
```

### Prompt Output Format

Each scene gets saved as a separate file. The prompt is plain text — the full universal template with only the dialogue line swapped.

**File naming**: `scene-{NN}-video.txt` (e.g., `scene-01-video.txt`)

### What You Do NOT Do

- Do NOT write custom body language per scene — the template handles it
- Do NOT write custom delivery instructions per scene — the template handles it
- Do NOT describe the environment — the reference image handles it
- Do NOT describe what the person looks like — the reference image handles it
- Do NOT add JSON structure — prompts are plain natural language
- Do NOT add speaking profiles — the template replaces the old profile system

---

## MODE 2: B-ROLL

Template TBD. Will be a separate universal template for non-speaking video clips (product shots, cutaways, environment shots).

B-roll defaults:
- UGC style (smartphone aesthetic, handheld shake, digital grain, casual framing)
- No macro lenses, studio lighting, or professional photography aesthetics
- Same location as speaking scenes unless specified otherwise
- First-to-last frame mode when both start and end frames are provided

---

## GENERAL RULES

- All prompts are **plain natural language** — no JSON, no structured fields
- All durations are **8 seconds** (only option for frames-to-video with reference images)
- `"(thats where the camera is)"` — Veo 3 syntax that triggers camera-aware processing. Already baked into the talking head template.
- `"The image is slightly grainy, looks very film-like"` — texture keywords for UGC feel. Already baked into the template.
- Dialogue format uses `They say: "..."` — colon format prevents Veo from generating subtitles
- **Google safety**: Avoid "razor" + body part + directional movement. Use "electric grooming device" for close-up scenes.

---

## LONG-FORM STORYTELLING NOTES <!-- date: 2026-03 -->

Pattern Q scripts (1:30 to 5+ minutes) produce significantly more scenes than standard videos. The same universal template and 8-second scene segmentation apply — there are just more scenes.

**Key considerations for long-form**:
- **Scene count**: A 2-minute script produces ~15 scenes. A 5-minute script produces ~37 scenes. All still 8 seconds each.
- **Pacing**: Storytelling scripts have slower, more emotional pacing. Scenes may have fewer words (15-20) with pauses and emotional beats filled naturally by the template's gesture system.
- **Aesthetic consistency**: Lo-fi iPhone feel is critical for storytelling. The reference image should convey raw, unpolished, intimate framing — close-ups with natural light, no makeup, visible emotion.
- **Scene transitions**: The emotional arc (Pain → Pressure → Breaking Point → Discovery → Transformation) should be reflected in the reference images, not the video prompts. The template handles emotional delivery from the dialogue alone.
