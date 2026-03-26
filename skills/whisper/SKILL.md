---
name: whisper
description: "Use when someone asks to transcribe a video, extract dialogue from a video or audio file, get a transcript, get the script from a video, analyze a video visually, break down a video, or says 'what does this say' about a media file. Also trigger when a video URL is provided and the user wants the spoken content or visual content extracted."
argument-hint: "[file path or URL] [--lang language] [--frames N] [--visual]"
---

# Video Analysis & Transcription Skill

Two capabilities in one skill:
1. **Transcription** (Whisper) — extracts spoken dialogue from audio/video. Free, local, no API key.
2. **Visual analysis** (ffmpeg + Claude vision) — extracts frames at intervals and presents them for visual analysis. Uses Claude's built-in vision.

Both can run together on the same video.

## Steps

### Step 1: Determine input type

Check if the argument is a URL or a local file path.

**If URL**: Download the video first using yt-dlp.

```bash
FFMPEG_DIR="/c/Users/Privat/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1-full_build/bin"
export PATH="$PATH:$FFMPEG_DIR"
YTDLP="C:\Users\Privat\AppData\Local\Programs\Python\Python312\Scripts\yt-dlp"
"$YTDLP" -o "/tmp/whisper_download.%(ext)s" "$URL" 2>&1
```

Find the downloaded file:
```bash
ls /tmp/whisper_download.* 2>/dev/null
```

**If local file**: Use the path directly. Verify the file exists first.

### Step 2: Determine what to do

| User says | Action |
|-----------|--------|
| "transcribe", "get the transcript", "what does this say" | Transcription only |
| "analyze this video", "break down this video", "what's happening in this video" | Visual analysis only |
| "transcribe and analyze", "full breakdown", or `--visual` flag with transcription | Both |
| Default (ambiguous) | Ask user: "Want just the transcript, visual analysis, or both?" |

### Step 3: Transcription (if needed)

Run Whisper with ffmpeg in PATH:

```bash
export PATH="$PATH:/c/Users/Privat/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1-full_build/bin"
whisper "$FILE_PATH" --model small --language $LANGUAGE --output_format txt 2>&1 | grep -v "%|"
```

- Default model: `small` (good accuracy/speed balance on CPU)
- Default language: `en` (override with `--lang` argument)
- The `grep -v` filters out progress bar noise

Present the transcript. Clean up Whisper warnings (FP16 not supported, etc.) and show just the timestamped text.

### Step 4: Visual analysis (if needed)

Extract frames from the video at regular intervals using ffmpeg.

**Step 4a: Get video duration**

```bash
export PATH="$PATH:/c/Users/Privat/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1-full_build/bin"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$FILE_PATH"
```

**Step 4b: Calculate frame interval**

Default: extract 10 frames evenly spaced across the video. User can override with `--frames N`.

```
interval = duration / number_of_frames
```

For a 90s video with 10 frames: one frame every 9 seconds.

**Step 4c: Extract frames**

```bash
mkdir -p /tmp/whisper_frames
export PATH="$PATH:/c/Users/Privat/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1-full_build/bin"
ffmpeg -i "$FILE_PATH" -vf "fps=1/$INTERVAL" -q:v 2 /tmp/whisper_frames/frame_%03d.jpg 2>&1
```

This outputs `frame_001.jpg`, `frame_002.jpg`, etc.

**Step 4d: Read frames with Claude vision**

Use the Read tool to view each extracted frame. For each frame, note the timestamp it corresponds to:

```
Frame 1 = 0:00
Frame 2 = 0:09
Frame 3 = 0:18
...
```

Read all frames and analyze them together.

**Step 4e: Present visual analysis**

After viewing all frames, provide a structured breakdown:

```
VISUAL ANALYSIS: [filename]
Duration: [X]s | Frames analyzed: [N]

SCENE BREAKDOWN:
Frame 1 (0:00): [What's visible — subject, setting, camera angle, text overlays, action]
Frame 2 (0:09): [What's visible]
Frame 3 (0:18): [What's visible]
...

VISUAL PATTERNS:
- Camera: [dominant style — selfie/tripod/top-down/handheld]
- Framing: [close-up/waist-up/full-body/product shot]
- Setting: [environment description]
- Text overlays: [style, placement, content if readable]
- Transitions: [cuts observed between frames]
- Layout: [full-screen / PiP / split-screen]

PRODUCTION STYLE:
- Aesthetic: [raw UGC / semi-polished / professional]
- Lighting: [natural/artificial, direction]
- Color palette: [warm/cool/neutral]
```

### Step 5: Combined output (if both)

When both transcription and visual analysis are requested, present them together:

```
FULL VIDEO BREAKDOWN: [filename]
Duration: [X]s

TRANSCRIPT:
[timestamped transcript from Whisper]

VISUAL ANALYSIS:
[scene breakdown from frame extraction]

SYNC NOTES:
[observations about how the visuals align with the dialogue — e.g., "at 0:18 the speaker says 'coffee' and the frame shows coffee being added to a bowl"]
```

### Step 6: Clean up

```bash
rm -rf /tmp/whisper_frames 2>/dev/null
rm /tmp/whisper_download.* 2>/dev/null
```

## Supported Formats

**Video:** mp4, mkv, webm, avi, mov, flv
**Audio:** mp3, wav, m4a, ogg, flac, aac (transcription only, no visual analysis)
**URLs:** Any platform supported by yt-dlp (TikTok, YouTube, Facebook, Instagram, Twitter/X, etc.)

## Whisper Models

| Model | Size | Speed (CPU) | Accuracy | When to Use |
|-------|------|-------------|----------|-------------|
| tiny | 39 MB | Fast | Low | Quick check, clear audio |
| base | 74 MB | Fast | Medium | Decent quality, fast |
| small | 244 MB | Moderate | Good | **Default.** Best balance |
| medium | 769 MB | Slow | High | Noisy audio, accents |
| large | 1.5 GB | Very slow | Highest | Maximum accuracy needed |

## Language Codes

Common: `en` (English), `es` (Spanish), `zh` (Chinese), `de` (German), `fr` (French), `ja` (Japanese), `ko` (Korean), `pt` (Portuguese), `hi` (Hindi)

If language is not specified, default to `en`.

## Frame Count Guidance

| Video Length | Default Frames | Result |
|---|---|---|
| Under 30s | 6 | One frame every ~5s |
| 30-60s | 8 | One frame every ~5-8s |
| 60-120s | 10 | One frame every ~6-12s |
| Over 120s | 15 | One frame every ~10-15s |

More frames = better coverage but more tokens for Claude to process. For most UGC videos (30-90s), 8-10 frames captures all the key moments.

## Notes

- Whisper runs on **CPU** (no GPU). The `small` model takes roughly 1-2x the audio duration to process
- FP16 warning is expected on CPU. Ignore it
- First run of a new model size downloads the model weights (~244 MB for small)
- yt-dlp supports Facebook Reels, TikTok, YouTube, Instagram, Twitter/X, and hundreds more
- If yt-dlp fails on a URL, suggest the user download the video manually
- Frame extraction is near-instant (ffmpeg is very fast)
- Visual analysis uses Claude's built-in vision. No extra API cost beyond the conversation
- For audio-only files (mp3, wav), skip visual analysis automatically
