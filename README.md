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

The **Manager** is the director — it coordinates all agents, manages the approval flow, and ensures consistency across outputs. See [manager/README.md](manager/README.md) for full pipeline details.

## Agents

| Agent | Folder | Purpose |
|-------|--------|---------|
| Manager | `manager/` | Pipeline coordinator, approval flow, consistency enforcement |
| Strategist | `strategist/` | Content briefs, audience research, prehook selection |
| Script Writer | `script-writer/` | UGC scripts (Schwartz framework, 5 modes, TikTok compliance) |
| Visual Planner | `visual-planner/` | Scene-by-scene storyboards, video type selection (13 types + 5 prehook types) |
| Image Prompter | `nanobanana-prompter/` | Image generation prompts (plain text + compact/full JSON) |
| Veo Prompter | `veo-prompter/` | Veo 3.1 video prompts (speaking scenes + B-roll) |
| Seedance Prompter | `seedance-prompter/` | Seedance 2.0 video prompts (Jimeng web UI, no negative prompts) |
| PatchWork Importer | `patchwork-importer/` | .nbflow workflow file generation |
| Viral Scanner | `viral-scanner/` | Trend scanning, hook research, creative templates |
| Knowledge Updater | `knowledge-updater/` | Ingests new info, updates agent reference files |

## Skills

Claude Code skills used by the pipeline, located in `skills/`:

| Skill | Used By | Purpose |
|-------|---------|---------|
| `last30days` | Viral Scanner | Trend research from Reddit, X, TikTok, YouTube, etc. |
| `notebooklm` | Knowledge Updater | Query Google NotebookLM for source-grounded answers |
| `whisper` | Knowledge Updater | Transcribe and visually analyze videos |
| `gsheets` | Manager | Read/write Google Sheets (prehook tracking, content calendars) |

**Installation**: Copy the `skills/` contents to `~/.claude/skills/` and install each skill's dependencies via `pip install -r requirements.txt` (where applicable).

## External Dependencies

These must be installed on the system. They are NOT bundled in this repo.

| Dependency | Install | Used For |
|------------|---------|----------|
| **Python 3.12+** | [python.org](https://www.python.org/) | Runtime for skills and utilities |
| **yt-dlp** | `pip install yt-dlp` | Download videos for analysis (TikTok, YouTube, Facebook) |
| **ffmpeg + ffprobe** | `winget install Gyan.FFmpeg` (Win) / `brew install ffmpeg` (Mac) | Frame extraction, audio processing |
| **OpenAI Whisper** | `pip install openai-whisper` | Speech-to-text transcription |

### Verify installation

```bash
python --version        # Python 3.12+
yt-dlp --version        # 2026.03+
ffmpeg -version         # ffmpeg 7+
whisper --help          # OpenAI Whisper CLI
```

## Setup

1. Clone this repo
2. Copy `skills/*` to `~/.claude/skills/`
3. Install external dependencies (see above)
4. Install skill dependencies: `cd skills/<skill> && pip install -r requirements.txt`
5. Open the `manager/` folder in Claude Code to start the pipeline
