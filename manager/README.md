# UGC Content Pipeline

An AI-powered content production system that takes a product brief and produces ready-to-render video assets — scripts, image prompts, video prompts, and a connected workflow file. Built for TikTok Shop, Amazon, and Meta Shop sales content.

## How It Works

```
Product Brief
     ↓
 STRATEGIST ──→ Content Brief (what to make, which angle, which audience)
     ↓
 MANAGER ──→ Video Plan (script + visual storyboard)
     ↓                          ↑
     ├→ SCRIPT WRITER           │ VIRAL SCANNER
     │   (write the script)     │ (trending video templates)
     │                          │
     ├→ VISUAL PLANNER          │
     │   (scene storyboard)     │
     │                          │
     ├→ IMAGE PROMPTER ─────────┤
     │   (reference images)     │
     │                          │
     ├→ VEO PROMPTER            │
     │   (speaking scene video) │
     │                          │
     ├→ SEEDANCE PROMPTER       │
     │   (alt speaking video)   │
     │                          │
     └→ PATCHWORK IMPORTER
         (.nbflow workflow file)
```

The pipeline runs in stages:

1. **Brief** — Gather product info, audience, visual direction, sales channel
2. **Script** — Generate a compliant script using Schwartz awareness framework
3. **Storyboard** — Break the script into visual scenes with full art direction
4. **Prompts & Workflow** — Generate all image/video prompts and bundle them into a PatchWork workflow file
5. **Delivery** — Hand off the `.nbflow` file + reference material checklist

The user approves the Video Plan (script + storyboard) once, then everything downstream generates automatically.

---

## Agents

### Manager (this project)

The director. Coordinates all other agents, owns the pipeline flow, and manages the approval loop. Does not write scripts, prompts, or strategy — delegates everything to the specialist agents.

**Produces**: Pipeline coordination, user-facing summaries and checklists.

### Strategist (`../strategist/`)

The intelligence layer above the pipeline. Decides *what* content to make based on strategy calls, platform compliance updates, and performance data. Researches story material and outputs Content Briefs that feed into the Manager.

**Produces**: Content Briefs with angle, audience, prehook selection, and story research.

### Script Writer (`../script-writer/`)

Writes UGC scripts using the Schwartz Breakthrough Advertising framework. Five operating modes:

| Mode | Purpose |
|------|---------|
| 1 | Adapt an existing script to a new product |
| 2 | Translate a script to another language |
| 3 | Segment a script into timed scenes |
| 4 | Create a variant of an existing script |
| 5 | Write a new script from scratch |

**Produces**: Full script text with Schwartz analysis, TikTok compliance notes, and CTA structure.

### Visual Planner (`../visual-planner/`)

Takes the approved script and visual direction, then produces a scene-by-scene visual storyboard. Selects the video type, plans reference image groups, camera angles, and B-roll placement. The storyboard is the source of truth for all downstream visual generation.

Maintains a library of 13 video type reference files (talking head, mixed-media animation, practitioner demo, hybrid two-part, etc.) plus 5 prehook type references.

**Produces**: Visual storyboard (user summary + internal detail for prompters).

### Image Prompter (`../nanobanana-prompter/`)

Generates image prompts for AI image generation (Gemini via Nanobanana API). Supports plain text for simple scenes and two JSON formats — compact and full analytical — for detailed, consistent output.

Key principles: conversational language over technical jargon, action over pose, narrative clutter for realism, no beauty descriptors, hand anchoring to prevent distortion.

**Produces**: Image prompt files (`.json` or `.txt`) for scene reference images, product hold variations, and B-roll stills.

### Veo Prompter (`../veo-prompter/`)

Generates Veo 3.1 video prompts for talking head (speaking) scenes. Uses a universal template approach — every scene uses the same base template, only the dialogue line changes.

**Produces**: One video prompt (`.json`) per speaking scene.

### Seedance Prompter (`../seedance-prompter/`)

Generates Seedance 2.0 video prompts for speaking and B-roll scenes. Alternative to Veo, runs through Jimeng web UI. Positive constraints only (no negative prompts).

**Produces**: Video prompt files for Seedance 2.0.

### PatchWork Importer (`../patchwork-importer/`)

Takes all generated prompts and builds a valid `.nbflow` workflow file for PatchWork. Wires up the full node chain: Prompt + Reference Images → Image Generation → Approval → Video Generation → Approval.

**Produces**: `.nbflow` project file with all prompts embedded and nodes connected.

### Viral Scanner (`../viral-scanner/`)

Scans for trending TikTok Shop videos. Breaks them down into reusable creative templates — pacing, camera angles, styling, story beats, visual direction. Uses the `/last30days` skill for trend research.

**Produces**: Creative template analysis (person, environment, camera, pacing, color palette, vibe).

### Knowledge Updater (`../knowledge-updater/`)

Ingests new information — docs, transcripts, links, platform updates, new techniques — and routes targeted edits to the correct agent projects. Works with NotebookLM for bulk analysis. Uses `/whisper` for video analysis (downloads via yt-dlp, transcribes, frame-grabs).

**Produces**: Targeted edits to agent reference files and CLAUDE.md instructions.

---

## Video Types

The Visual Planner maintains reference files for each video format the pipeline can produce:

| Type | Description |
|------|-------------|
| Talking Head | Standard UGC. Avatar speaks full-screen, B-roll as cutaways |
| Recipe Demo PiP | Ingredient walkthroughs. Demo footage main frame, speaker PiP |
| Podcast Authority | Expert at desk with mic, bookshelf, kinetic captions |
| Storytelling Confession | Raw emotional story, car/kitchen, zero B-roll |
| Split-Screen Storytelling | Creator bottom half, visual evidence cycles top half |
| Borrowed Authority | Repurposed speaker footage as wallpaper, text overlays sell |
| AI Avatar Historical | AI avatar alternates with AI historical imagery |
| Mixed-Media Animation | Rendered backgrounds cycling (3D anatomy, recipe close-ups). Speaker PiP or pure animation |
| Practitioner Demo | Full-frame healer performs remedy on patient/self, one continuous shot |
| Hybrid Two-Part | Two formats joined by hard cut — visual hook then talking sell |
| Text Wall Over B-Roll | Faceless. Text carries message over looping B-roll |
| Faceless Hands-Only | Product demos, unboxing. No face, hands + product |
| Green Screen Commentary | Speaker bottom, evidence/screenshots as background |

Prehook types (separate folder): Transformation Before/After, Body Close-Up, Reaction PiP, Visceral Render, Mirror Selfie.

Reference files: `../visual-planner/reference/video-types/`

---

## Project Structure

Each video gets its own folder under `projects/`:

```
manager/
  projects/
    {product-start-date}/
      S1-Bryan/
        video-plan.md              ← Script + storyboard
        main-body/
          scene-01-image-start.json
          scene-01-video.json
          ...
        prehooks/
          prehook-01-image.json
          prehook-01-video.json
        broll/
          broll-01-image.json
          broll-01-video.txt
```

Folder naming: `{Brand Acronym}{Number}-{User}` (e.g., `S1-Bryan` = Salvora video 1, Bryan's).

---

## Sales Channels

| Channel | CTA | Notes |
|---------|-----|-------|
| **TikTok Shop** | Shop button on video | AI Label Trick needed |
| **Amazon (via keyword)** | Comment keyword → ManyChat auto-DM | No AI label needed |
| **Meta Shop (FB/IG)** | Shop button on Reel → Amazon link | No AI label needed |

---

## B-roll Density Modes

Controls how much B-roll supplementary footage is generated for the main body:

| Mode | Coverage | Typical Clips |
|------|----------|---------------|
| **High** | Every speaking scene gets a companion cutaway | Matches scene count |
| **Medium** (default) | Visual moments — product reveals, ingredients, failed solutions | ~50% of scenes |
| **Low** | Only the product reveal + 1-2 high-impact moments | 2-3 clips |

Prehooks are unaffected by density mode.

---

## Skills (Claude Code)

These Claude Code skills are used by various agents in the pipeline. They live in `~/.claude/skills/` and are invoked via slash commands.

| Skill | Used By | Purpose |
|-------|---------|---------|
| `/last30days` | Viral Scanner | Trend research from Reddit, X, TikTok, YouTube, Instagram, etc. |
| `/notebooklm` | Knowledge Updater | Query Google NotebookLM notebooks for source-grounded answers |
| `/whisper` | Knowledge Updater | Transcribe and visually analyze videos (downloads via yt-dlp) |
| `/gsheets` | Manager | Read/write Google Sheets (prehook tracking, content calendars) |

---

## External Dependencies

These must be installed on the system for the pipeline to function. They are NOT bundled in the project.

| Dependency | Install | Used For |
|------------|---------|----------|
| **Python 3.12+** | [python.org](https://www.python.org/) | Runtime for yt-dlp, whisper, notebooklm scripts |
| **yt-dlp** | `pip install yt-dlp` | Download videos from TikTok, YouTube, Instagram, Facebook for analysis |
| **ffmpeg + ffprobe** | `winget install Gyan.FFmpeg` (Windows) or `brew install ffmpeg` (Mac) | Video frame extraction, audio processing, format conversion |
| **OpenAI Whisper** | `pip install openai-whisper` | Speech-to-text transcription for video analysis |

### Verify installation

```bash
python --version        # Python 3.12+
yt-dlp --version        # 2026.03.03+
ffmpeg -version         # ffmpeg 7+
whisper --help          # OpenAI Whisper CLI
```

Note: yt-dlp's Instagram extractor is currently broken (March 2026). Individual reel URLs still work, but profile-level scraping does not.
