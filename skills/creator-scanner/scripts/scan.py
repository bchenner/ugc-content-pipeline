"""Creator Scanner — Download and prepare viral videos for analysis.

Supports TikTok (via yt-dlp) and Instagram (via ScrapeCreators API).
Filters to last N days and minimum view count.
Extracts prehook frames (first 5s at 2fps) + body frames + Whisper transcript.
Saves structured analysis cards to the creator library.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

TEMP_DIR = Path("C:/Users/Privat/AppData/Local/Temp/video-analysis")
FFMPEG_DIR = "C:/Users/Privat/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1-full_build/bin"
SENSITIVE_DIR = Path("C:/Users/Privat/Documents/Claude Code/claude-projects/manager/.sensitive")
LIBRARY_DIR = Path("C:/Users/Privat/Documents/Claude Code/claude-projects/visual-planner/reference/creator-library")

os.environ["PATH"] = FFMPEG_DIR + os.pathsep + os.environ.get("PATH", "")


def load_api_key():
    env_file = SENSITIVE_DIR / "api-keys.env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").strip().split("\n"):
            if line.startswith("SCRAPECREATORS_API_KEY="):
                return line.split("=", 1)[1].strip()
    return os.environ.get("SCRAPECREATORS_API_KEY", "")


def scan_tiktok(username, min_views, max_videos, days):
    """List TikTok videos via yt-dlp, filter, download top N."""
    clean_name = username.lstrip("@")
    print(f"[TikTok] Scanning @{clean_name}...")

    result = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--print", "%(id)s\t%(view_count)s\t%(timestamp)s\t%(title)s",
         f"https://www.tiktok.com/@{clean_name}"],
        capture_output=True, timeout=120,
        encoding="utf-8", errors="replace"
    )

    if result.returncode != 0 or not result.stdout:
        print(f"  Error: {(result.stderr or 'No output')[:200]}")
        return []

    cutoff_ts = (datetime.now(timezone.utc) - timedelta(days=days)).timestamp()

    videos = []
    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("\t", 3)
        if len(parts) < 4:
            continue

        vid_id, views_str, ts_str, title = parts
        try:
            views = int(views_str) if views_str != "NA" else 0
            ts = int(ts_str) if ts_str != "NA" else 0
        except (ValueError, TypeError):
            continue

        if ts and ts < cutoff_ts:
            continue
        if views < min_views:
            continue

        videos.append({
            "id": vid_id, "views": views, "timestamp": ts,
            "title": title[:100],
            "url": f"https://www.tiktok.com/@{clean_name}/video/{vid_id}",
            "platform": "tiktok"
        })

    videos.sort(key=lambda x: x["views"], reverse=True)
    videos = videos[:max_videos]
    print(f"  Found {len(videos)} viral videos (>{min_views} views, last {days} days)")
    return videos


def scan_instagram(username, min_views, max_videos, days, max_pages=5):
    """List Instagram reels via ScrapeCreators API with pagination."""
    import requests

    clean_name = username.lstrip("@")
    api_key = load_api_key()
    if not api_key:
        print("  No SCRAPECREATORS_API_KEY found.")
        return []

    print(f"[Instagram] Scanning @{clean_name}...")

    cutoff_ts = (datetime.now(timezone.utc) - timedelta(days=days)).timestamp()
    all_videos = []
    max_id = None

    for page in range(max_pages):
        params = {"handle": clean_name}
        if max_id:
            params["max_id"] = max_id

        try:
            resp = requests.get(
                "https://api.scrapecreators.com/v1/instagram/user/reels",
                params=params,
                headers={"x-api-key": api_key},
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"  API error on page {page+1}: {e}")
            break

        if page == 0:
            print(f"  Credits remaining: {data.get('credits_remaining', '?')}")

        items = data.get("items", [])
        if not items:
            break

        # Check if we've gone past our date cutoff
        hit_cutoff = False
        for item in items:
            media = item.get("media", item)
            taken_at = media.get("taken_at", 0)

            if taken_at and taken_at < cutoff_ts:
                hit_cutoff = True
                continue

            play_count = media.get("play_count", 0) or 0
            code = media.get("code", "")
            caption = media.get("caption", {})
            caption_text = caption.get("text", "") if isinstance(caption, dict) else str(caption or "")

            video_versions = media.get("video_versions", [])
            video_url = ""
            if video_versions and isinstance(video_versions, list):
                best = max(video_versions, key=lambda v: v.get("height", 0) * v.get("bandwidth", 0))
                video_url = best.get("url", "")

            all_videos.append({
                "id": code, "views": play_count, "timestamp": taken_at,
                "title": caption_text[:100],
                "url": f"https://www.instagram.com/reel/{code}/",
                "video_url": video_url,
                "like_count": media.get("like_count", 0),
                "comment_count": media.get("comment_count", 0),
                "platform": "instagram"
            })

        # Check pagination
        paging = data.get("paging_info", {})
        if not paging.get("more_available") or hit_cutoff:
            break
        max_id = paging.get("max_id")
        if not max_id:
            break

        print(f"  Page {page+1}: {len(items)} reels (total so far: {len(all_videos)})")

    # Filter by min views and sort
    viral = [v for v in all_videos if v["views"] >= min_views]
    viral.sort(key=lambda x: x["views"], reverse=True)
    viral = viral[:max_videos]

    print(f"  Total reels scanned: {len(all_videos)} | Viral (>{min_views}): {len(viral)} | Last {days} days")
    return viral


def download_video(video, scan_dir, index):
    """Download a single video."""
    username = scan_dir.name.replace("scan-", "")
    filename = f"{username}_{index:02d}.mp4"
    filepath = scan_dir / filename

    if filepath.exists():
        print(f"  Already downloaded: {filename}")
        return filepath

    if video["platform"] == "tiktok":
        result = subprocess.run(
            ["yt-dlp", "-o", str(filepath), video["url"]],
            capture_output=True, timeout=120, encoding="utf-8", errors="replace"
        )
        if result.returncode != 0:
            print(f"  Download failed: {(result.stderr or '')[:100]}")
            return None
    elif video["platform"] == "instagram":
        result = subprocess.run(
            ["yt-dlp", "-o", str(filepath), video["url"]],
            capture_output=True, timeout=120, encoding="utf-8", errors="replace"
        )
        if result.returncode != 0 and video.get("video_url"):
            import requests
            try:
                r = requests.get(video["video_url"], timeout=60)
                filepath.write_bytes(r.content)
            except Exception as e:
                print(f"  Download failed: {e}")
                return None

    if filepath.exists():
        print(f"  Downloaded: {filename} ({filepath.stat().st_size // 1024}KB)")
        return filepath
    return None


def extract_frames(filepath, scan_dir, index):
    """Extract prehook frames (first 5s at 2fps) + body frames."""
    username = scan_dir.name.replace("scan-", "")
    frame_dir = scan_dir / "frames" / f"{username}_{index:02d}"
    frame_dir.mkdir(parents=True, exist_ok=True)

    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(filepath)],
        capture_output=True, text=True
    )
    try:
        dur = float(r.stdout.strip())
    except:
        return 0, 0, 0

    # Prehook: first 5 seconds at 2fps
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(filepath), "-t", "5", "-vf", "fps=2", "-q:v", "2",
         str(frame_dir / "prehook_%02d.jpg")], capture_output=True)

    # Body: 1 frame per 5 seconds
    interval = max(1, int(dur / 12))
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(filepath), "-vf", f"fps=1/{interval}", "-q:v", "2",
         str(frame_dir / "frame_%03d.jpg")], capture_output=True)

    ph = len([f for f in frame_dir.iterdir() if f.name.startswith("prehook")])
    bd = len([f for f in frame_dir.iterdir() if f.name.startswith("frame")])
    print(f"  Frames: {ph} prehook + {bd} body ({dur:.0f}s)")
    return ph, bd, dur


def transcribe(filepath, scan_dir, index):
    """Transcribe with Whisper."""
    username = scan_dir.name.replace("scan-", "")
    txt_path = scan_dir / f"{username}_{index:02d}.txt"

    if txt_path.exists():
        print(f"  Already transcribed")
        return

    result = subprocess.run(
        ["whisper", str(filepath), "--model", "small", "--language", "en",
         "--output_format", "txt", "--output_dir", str(scan_dir)],
        capture_output=True, text=True, timeout=300,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}
    )
    if result.returncode == 0:
        print(f"  Transcribed")
    else:
        print(f"  Whisper error: {result.stderr[:100]}")


def save_video_card(video, scan_dir, index, duration):
    """Save a compact analysis card for the creator library."""
    username = scan_dir.name.replace("scan-", "")
    card = {
        "id": video["id"],
        "url": video["url"],
        "platform": video["platform"],
        "views": video["views"],
        "likes": video.get("like_count", 0),
        "comments": video.get("comment_count", 0),
        "date": datetime.fromtimestamp(video["timestamp"]).strftime("%Y-%m-%d") if video["timestamp"] else "unknown",
        "duration_seconds": round(duration) if duration else 0,
        "caption": video["title"],
        "frames_dir": f"scan-{username}/frames/{username}_{index:02d}",
        "transcript_file": f"scan-{username}/{username}_{index:02d}.txt",
        "analysis": {
            "prehook": "PENDING — read prehook_01.jpg through prehook_05.jpg",
            "hook_line": "PENDING — read transcript first line",
            "video_type": "PENDING",
            "broll": "PENDING",
            "cta": "PENDING",
            "notable": "PENDING"
        }
    }

    # Save card
    card_path = scan_dir / f"{username}_{index:02d}_card.json"
    card_path.write_text(json.dumps(card, indent=2, ensure_ascii=False), encoding="utf-8")
    return card


def save_library_index(username, platform, videos, scan_dir):
    """Save/update the creator library index."""
    lib_dir = LIBRARY_DIR / username
    lib_dir.mkdir(parents=True, exist_ok=True)

    profile = {
        "username": username,
        "platform": platform,
        "scanned_at": datetime.now().isoformat(),
        "scan_dir": str(scan_dir),
        "total_viral_videos": len(videos),
        "videos": [{
            "id": v["id"],
            "views": v["views"],
            "date": datetime.fromtimestamp(v["timestamp"]).strftime("%Y-%m-%d") if v["timestamp"] else "?",
            "caption": v["title"][:60],
            "card": f"{v['id']}_card.json"
        } for v in videos],
        "analysis_status": "FRAMES_EXTRACTED — needs visual analysis"
    }

    (lib_dir / "profile.json").write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Library index saved: creator-library/{username}/profile.json")


def main():
    parser = argparse.ArgumentParser(description="Scan a creator for viral videos")
    parser.add_argument("username", help="@username")
    parser.add_argument("--platform", choices=["tiktok", "instagram", "auto"], default="auto")
    parser.add_argument("--min-views", type=int, default=100000)
    parser.add_argument("--max-videos", type=int, default=5)
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--skip-transcribe", action="store_true")
    parser.add_argument("--skip-download", action="store_true", help="List only, no download")

    args = parser.parse_args()
    clean_name = args.username.lstrip("@")
    platform = args.platform if args.platform != "auto" else "tiktok"

    scan_dir = TEMP_DIR / f"scan-{clean_name}"
    scan_dir.mkdir(parents=True, exist_ok=True)

    # Scan
    if platform == "tiktok":
        videos = scan_tiktok(clean_name, args.min_views, args.max_videos, args.days)
    else:
        videos = scan_instagram(clean_name, args.min_views, args.max_videos, args.days)

    if not videos:
        print(f"\nNo viral videos found for @{clean_name}.")
        return

    # Print summary table
    print(f"\nTop {len(videos)} viral videos:")
    for v in videos:
        date_str = datetime.fromtimestamp(v["timestamp"]).strftime("%Y-%m-%d") if v["timestamp"] else "?"
        print(f"  {v['views']:>10,} views | {date_str} | {v['title'][:50]}")

    if args.skip_download:
        # Save summary and exit
        (scan_dir / "scan-summary.json").write_text(
            json.dumps({"username": clean_name, "platform": platform, "videos": videos},
                       indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nListing saved. Use without --skip-download to download and extract frames.")
        return

    # Download + extract + transcribe
    downloaded = []
    for i, video in enumerate(videos, 1):
        print(f"\n--- Video {i}/{len(videos)} ({video['views']:,} views) ---")

        filepath = download_video(video, scan_dir, i)
        if not filepath:
            continue

        _, _, dur = extract_frames(filepath, scan_dir, i)

        if not args.skip_transcribe:
            transcribe(filepath, scan_dir, i)

        save_video_card(video, scan_dir, i, dur)
        downloaded.append(video)

    # Save to library
    save_library_index(clean_name, platform, downloaded, scan_dir)

    # Save full summary
    (scan_dir / "scan-summary.json").write_text(
        json.dumps({"username": clean_name, "platform": platform,
                     "videos_found": len(videos), "videos_downloaded": len(downloaded),
                     "scan_dir": str(scan_dir), "videos": videos},
                   indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"Scan complete: @{clean_name} ({platform})")
    print(f"  {len(downloaded)} videos in {scan_dir}")
    print(f"  Library: creator-library/{clean_name}/profile.json")
    print(f"  Next: Read prehook frames + transcripts for analysis")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
