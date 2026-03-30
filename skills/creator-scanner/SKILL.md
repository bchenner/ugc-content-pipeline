# Creator Scanner

Scan a TikTok or Instagram creator account to analyze their viral content from the last 30 days.

## Usage

```
/creator-scanner @username [--platform tiktok|instagram] [--min-views 100000] [--max-videos 5] [--days 30]
```

## Running

```bash
python ~/.claude/skills/creator-scanner/scripts/scan.py @username --platform tiktok --min-views 100000 --max-videos 5 --days 30
```

For Instagram:
```bash
python ~/.claude/skills/creator-scanner/scripts/scan.py @username --platform instagram --min-views 100000 --max-videos 3 --days 30
```

Instagram uses the ScrapeCreators API (key in `manager/.sensitive/api-keys.env`). Each API call costs credits. Check credits_remaining in output.

## What It Does

1. Lists videos from the account (yt-dlp for TikTok, ScrapeCreators API for Instagram)
2. Filters to last N days and minimum view count
3. Downloads top N by views
4. Extracts prehook frames (first 5 seconds at 2fps = 10 frames)
5. Extracts body frames (rest of video at 1 frame per 5 seconds)
6. Transcribes with Whisper

## Output

```
C:/Users/Privat/AppData/Local/Temp/video-analysis/scan-{username}/
  {username}_01.mp4
  {username}_01.txt           — Whisper transcript
  {username}_01_meta.json     — Views, date, caption, URL
  frames/{username}_01/
    prehook_01.jpg ... prehook_10.jpg
    frame_001.jpg ... frame_NNN.jpg
  scan-summary.json
```

## After Scanning — Analysis Checklist

Read the prehook frames and answer:

1. **Prehook** (prehook_01 through prehook_10):
   - Is there a separate prehook clip, or does the video start with the hook directly?
   - What stops the scroll? (text overlay, visual shock, face expression, action)
   - What text appears on screen in the first 2 seconds?
   - Any celebrity/authority image overlaid?

2. **Hook** (first spoken line from transcript):
   - What's the opening line?
   - What emotional trigger? (outrage, curiosity, fear, relatability)

3. **B-roll** (body frames):
   - Any cutaways or is it one continuous shot?
   - Any background imagery cycling?
   - What video type? (talking head, greenscreen, PiP, mixed-media, split-screen)

4. **Comments** (if accessible):
   - What are people responding to?
   - What drives engagement?

5. **Map to existing types** — Is this a known video type or something new?

## Requirements

- yt-dlp, ffmpeg, whisper (system installs)
- requests (pip) for Instagram
- ScrapeCreators API key for Instagram (in manager/.sensitive/api-keys.env)
