# UGC Content Pipeline

A multi-agent AI content production system built on Claude Code. Takes a product brief and produces ready-to-render video assets — scripts, visual storyboards, image prompts, video prompts, and connected PatchWork workflow files.

Built for TikTok Shop, Amazon, and Meta Shop sales content.

## Architecture

```
Product Brief → STRATEGIST → MANAGER → SCRIPT WRITER → VISUAL PLANNER → PROMPTERS → PATCHWORK
                                ↑                                            ↓
                          VIRAL SCANNER                              IMAGE PROMPTER
                          (trend research)                           VEO PROMPTER
                                                                     SEEDANCE PROMPTER
                                                                     PATCHWORK IMPORTER
```

The **Manager** is the director — it coordinates all agents, manages the approval flow, and ensures consistency across outputs.

## Current Campaign

**Product**: Salvora Rhodiola Rosea (adaptogen supplement, cortisol management)
**Accounts**: 6 total (3 English, 3 Spanish), each with a distinct AI avatar
**Daily volume**: 18 videos/day (3 per account: 2 growth + 1 sales)
**Sales channels**: Amazon (keyword CTA), Meta Shop (FB/IG)
**Target**: Women 35-55 dealing with stress, cortisol, menopause, fatigue

See `manager/reference/accounts.md` for avatar details and `manager/reference/products.md` for product guidelines.

## Weekly Production SOP

See `manager/sop/weekly-content-production.md` for the full workflow:

```
1. Review last week's data + decide carryover
2. Plan growth topics (4/day x 5 days = 20 scripts)
3. Plan sales scripts + prehook rotation
4. Write EN scripts → translate to ES (Script Writer Mode 2)
5. Visual storyboards → image prompts → video prompts
6. Generate Testing tab .nbflow → test in PatchWork
7. Generate account tabs → import and run
8. Post-production → schedule and post
```

## Agents

| Agent | Folder | Purpose |
|-------|--------|---------|
| Manager | `manager/` | Pipeline coordinator, approval flow, consistency enforcement |
| Strategist | `strategist/` | Content briefs, audience research, prehook selection, content calendars |
| Script Writer | `script-writer/` | UGC scripts (Schwartz framework, 5 modes, 22 patterns A-V, TikTok compliance) |
| Visual Planner | `visual-planner/` | Scene-by-scene storyboards, video type selection (13 types + 5 prehook types) |
| Image Prompter | `nanobanana-prompter/` | Image generation prompts (plain text + compact/full JSON) |
| Veo Prompter | `veo-prompter/` | Veo 3.1 video prompts (speaking scenes + B-roll) |
| Seedance Prompter | `seedance-prompter/` | Seedance 2.0 video prompts (Jimeng web UI, no negative prompts) |
| Sora Prompter | `sora-prompter/` | Sora 2 B-roll video prompts |
| PatchWork Importer | `patchwork-importer/` | .nbflow workflow file generation |
| Viral Scanner | `viral-scanner/` | Trend scanning, hook research, creative templates |
| Knowledge Updater | `knowledge-updater/` | Ingests new info, updates agent reference files |

## Skills

Claude Code skills used by the pipeline (install to `~/.claude/skills/`):

| Skill | Purpose |
|-------|---------|
| `gsheets` | Read/write Google Sheets (prompt storage, content calendars) |
| `agent-auditor` | Audit agent CLAUDE.md files for token bloat, duplication, broken refs |
| `creator-scanner` | Scan TikTok/Instagram creators for viral videos, extract frames + transcripts |
| `last30days` | Trend research from Reddit, X, TikTok, YouTube, HN, Polymarket |
| `notebooklm` | Query Google NotebookLM for source-grounded answers |
| `whisper` | Transcribe and visually analyze videos |
| `skill-builder` | Create and audit Claude Code skills |

## Script Patterns

22 patterns (A-V) covering short-form and extended formats:

| Range | Type | Examples |
|-------|------|---------|
| A-J | Short-form direct sales | Symptom recognition, command structure, visual proof, misdirection, authority |
| K-O | Extended mechanics | Pre-hooks, visual symptom pyramid, podcast revival, content ratio, keyword CTA |
| P-R | Storytelling | Health history conspiracy, long-form personal storytelling, pain personification |
| S-V | New formats (March 2026) | Controversial hook, lifestyle transformation, dating glow-up, expert ranking |

Storytelling scripts follow a mandatory 6-beat structure: Pain → Pressure → Breaking Point → Discovery → Transformation → CTA.

## Content Strategy (March 2026)

- **50/50 content split**: Half current viral styles (podcast), half proven frameworks from 60-90 days ago
- **3:1 posting ratio** while under 50k followers (2 growth + 1 sales per account)
- **Growth videos**: 30-60s, educational, no product mention, no CTA. Categories: Cortisol Education, Relatable Moment, Recipe/Hack, Motivation/Identity
- **Sales videos**: 1:30-2:30, storytelling framework, Amazon keyword CTA
- **Approved angles**: Menopause, aging, loss of energy, stress. NO weight loss claims
- **Comment-driven engagement**: Every script needs one quotable line, mild debate framing, and specificity over vagueness

## Reference Files

| File | Purpose |
|------|---------|
| `manager/reference/accounts.md` | All 6 accounts with avatars, settings, wardrobe, video types |
| `manager/reference/products.md` | Salvora Rhodiola Rosea: approved angles, CTA keywords, production rules |
| `manager/sop/weekly-content-production.md` | Full weekly production SOP |
| `script-writer/reference/products/salvora.md` | Product doc for script writing |
| `script-writer/reference/directory.md` | Pattern library index |
| `visual-planner/reference/video-types/` | 13 video types + 5 prehook subtypes |
| `visual-planner/reference/creator-library/` | Scanned creator accounts with hook analysis |

## External Dependencies

| Dependency | Install | Used For |
|------------|---------|----------|
| **Python 3.12+** | [python.org](https://www.python.org/) | Runtime for skills and utilities |
| **yt-dlp** | `pip install yt-dlp` | Download videos for analysis |
| **ffmpeg + ffprobe** | `winget install Gyan.FFmpeg` (Win) / `brew install ffmpeg` (Mac) | Frame extraction, audio processing |
| **OpenAI Whisper** | `pip install openai-whisper` | Speech-to-text transcription |

## Setup

1. Clone this repo
2. Copy skills to `~/.claude/skills/` (gsheets, agent-auditor, creator-scanner, etc.)
3. Install external dependencies (see above)
4. Install skill dependencies: `cd ~/.claude/skills/<skill> && pip install -r requirements.txt`
5. Set up Google Sheets service account (see `gsheets` skill docs)
6. Open the `manager/` folder in Claude Code to start the pipeline
