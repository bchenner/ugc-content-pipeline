"""Scrape TikTok creator profiles via ScrapeCreators API.

Fetches recent high-performing videos from a list of creators,
extracts transcripts, and saves organized output.

Usage:
    python scripts/scrape_creators.py
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timezone, timedelta

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
from pathlib import Path

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system(f"{sys.executable} -m pip install requests -q")
    import requests

# --- Config ---
API_KEY = "NKDaU3aS77aJ8rBgU3sAGZ56LrO2"
BASE_URL = "https://api.scrapecreators.com/v1/tiktok"
HEADERS = {"x-api-key": API_KEY, "Content-Type": "application/json"}

# Creators to scrape (from NotebookLM storytelling accounts list)
CREATORS = [
    "catstoriesss",
    "naestradamus",
    "isabelleshoppinghauls",
    "mshellly",
    "kateysuperspam",
    "kelsgordon",
    "jamie.nelson98",
    "sandrasitto",
    "misshealer_",
    "taimqbfjtr7",
]

# Date range: last 30 days
NOW = datetime.now(timezone.utc)
THIRTY_DAYS_AGO = NOW - timedelta(days=30)
MIN_VIEWS = 100_000  # Only grab high performers

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "research" / "creator-scrape"


def clean_webvtt(text):
    """Strip WebVTT timestamps and headers, return clean transcript."""
    if not text:
        return ""
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('WEBVTT'):
            continue
        if re.match(r'^\d{2}:\d{2}', line):
            continue
        if '-->' in line:
            continue
        cleaned.append(line)
    return ' '.join(cleaned)


def fetch_profile(handle):
    """Get creator profile info."""
    try:
        resp = requests.get(
            f"{BASE_URL}/profile",
            params={"handle": handle},
            headers=HEADERS,
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            user = data.get("user", {})
            stats = data.get("stats", user)
            return {
                "handle": handle,
                "nickname": user.get("nickname", ""),
                "bio": user.get("signature", ""),
                "followers": stats.get("followerCount", stats.get("follower_count", 0)),
                "total_likes": stats.get("heartCount", stats.get("total_favorited", 0)),
                "video_count": stats.get("videoCount", stats.get("aweme_count", 0)),
            }
    except Exception as e:
        print(f"  [!] Profile fetch failed for {handle}: {e}")
    return {"handle": handle, "nickname": "", "bio": "", "followers": 0, "total_likes": 0, "video_count": 0}


def fetch_videos(handle, max_pages=5):
    """Fetch all recent videos from a creator (paginated)."""
    all_videos = []
    seen_ids = set()
    cursor = 0

    for page in range(max_pages):
        try:
            resp = requests.get(
                f"{BASE_URL}/profile/videos",
                params={"handle": handle, "cursor": cursor},
                headers=HEADERS,
                timeout=15,
            )
            if resp.status_code != 200:
                print(f"  [!] Page {page+1} failed: HTTP {resp.status_code}")
                break

            data = resp.json()
            videos = data.get("aweme_list", [])
            if not videos:
                break

            for v in videos:
                vid_id = v.get("aweme_id", "")
                if vid_id in seen_ids:
                    continue
                seen_ids.add(vid_id)
                create_time = v.get("create_time", 0)
                dt = datetime.fromtimestamp(create_time, tz=timezone.utc)

                # Skip videos older than 30 days
                if dt < THIRTY_DAYS_AGO:
                    continue

                stats = v.get("statistics", {})
                views = stats.get("play_count", 0)

                # Duration is in ms, convert to seconds
                duration_ms = v.get("video", {}).get("duration", 0)
                duration_s = duration_ms / 1000 if duration_ms > 100 else duration_ms

                all_videos.append({
                    "video_id": v.get("aweme_id", ""),
                    "desc": v.get("desc", ""),
                    "date": dt.strftime("%Y-%m-%d"),
                    "views": views,
                    "likes": stats.get("digg_count", 0),
                    "comments": stats.get("comment_count", 0),
                    "shares": stats.get("share_count", 0),
                    "duration_s": round(duration_s, 1),
                    "url": f"https://www.tiktok.com/@{handle}/video/{v.get('aweme_id', '')}",
                    "hashtags": [t.get("hashtag_name", "") for t in v.get("text_extra", [])
                                 if isinstance(t, dict) and t.get("hashtag_name")],
                })

            has_more = data.get("has_more", 0)
            if not has_more:
                break
            cursor = data.get("max_cursor", cursor + 10)
            time.sleep(0.3)  # Be nice to the API

        except Exception as e:
            print(f"  [!] Page {page+1} error: {e}")
            break

    return all_videos


def fetch_transcript(url):
    """Fetch transcript for a single video."""
    try:
        resp = requests.get(
            f"{BASE_URL}/video/transcript",
            params={"url": url},
            headers=HEADERS,
            timeout=20,
        )
        if resp.status_code == 200:
            data = resp.json()
            transcript = data.get("transcript", "")
            if isinstance(transcript, list):
                transcript = " ".join(str(s) for s in transcript)
            return clean_webvtt(transcript)
    except Exception as e:
        print(f"  [!] Transcript failed: {e}")
    return ""


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_results = {}
    total_transcripts = 0

    # Check for --skip N flag to resume
    skip = 0
    if "--skip" in sys.argv:
        idx = sys.argv.index("--skip")
        if idx + 1 < len(sys.argv):
            skip = int(sys.argv[idx + 1])

    # Load existing results for skipped creators
    for handle in CREATORS[:skip]:
        creator_file = OUTPUT_DIR / f"{handle}.json"
        if creator_file.exists():
            with open(creator_file, "r", encoding="utf-8") as f:
                all_results[handle] = json.load(f)

    print(f"Scraping {len(CREATORS) - skip} creators for videos from last 30 days (skipping first {skip})")
    print(f"Date range: {THIRTY_DAYS_AGO.strftime('%Y-%m-%d')} to {NOW.strftime('%Y-%m-%d')}")
    print(f"Min views threshold: {MIN_VIEWS:,}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    for i, handle in enumerate(CREATORS):
        if i < skip:
            continue
        print(f"\n[{i+1}/{len(CREATORS)}] @{handle}")

        # Get profile
        profile = fetch_profile(handle)
        print(f"  {profile['nickname']} | {profile['followers']:,} followers | {profile['video_count']} videos")

        # Get videos
        videos = fetch_videos(handle)
        print(f"  Found {len(videos)} videos in last 30 days")

        # Filter high performers
        high_perf = [v for v in videos if v["views"] >= MIN_VIEWS]
        high_perf.sort(key=lambda x: x["views"], reverse=True)
        print(f"  {len(high_perf)} videos above {MIN_VIEWS:,} views")

        # Fetch transcripts for high performers
        for j, video in enumerate(high_perf):
            print(f"  Fetching transcript {j+1}/{len(high_perf)}: {video['views']:,} views - {video['desc'][:50]}...")
            transcript = fetch_transcript(video["url"])
            video["transcript"] = transcript
            if transcript:
                total_transcripts += 1
                print(f"    Got {len(transcript.split())} words")
            else:
                print(f"    No transcript available")
            time.sleep(0.3)

        # Save per-creator file
        creator_data = {
            "profile": profile,
            "scrape_date": NOW.strftime("%Y-%m-%d"),
            "date_range": f"{THIRTY_DAYS_AGO.strftime('%Y-%m-%d')} to {NOW.strftime('%Y-%m-%d')}",
            "total_videos_in_range": len(videos),
            "high_performers": len(high_perf),
            "videos": high_perf,
        }

        creator_file = OUTPUT_DIR / f"{handle}.json"
        with open(creator_file, "w", encoding="utf-8") as f:
            json.dump(creator_data, f, indent=2, ensure_ascii=False)

        all_results[handle] = creator_data

    # Save summary
    summary = {
        "scrape_date": NOW.strftime("%Y-%m-%d %H:%M UTC"),
        "date_range": f"{THIRTY_DAYS_AGO.strftime('%Y-%m-%d')} to {NOW.strftime('%Y-%m-%d')}",
        "min_views": MIN_VIEWS,
        "creators_scraped": len(CREATORS),
        "total_high_perf_videos": sum(r["high_performers"] for r in all_results.values()),
        "total_transcripts": total_transcripts,
        "per_creator": {
            handle: {
                "followers": data["profile"]["followers"],
                "videos_in_range": data["total_videos_in_range"],
                "high_performers": data["high_performers"],
                "top_video_views": data["videos"][0]["views"] if data["videos"] else 0,
            }
            for handle, data in all_results.items()
        }
    }

    with open(OUTPUT_DIR / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n" + "=" * 60)
    print("SCRAPE COMPLETE")
    print(f"Creators: {len(CREATORS)}")
    print(f"High-perf videos found: {summary['total_high_perf_videos']}")
    print(f"Transcripts extracted: {total_transcripts}")
    print(f"\nPer creator:")
    for handle, stats in summary["per_creator"].items():
        print(f"  @{handle}: {stats['videos_in_range']} videos, {stats['high_performers']} high-perf, top={stats['top_video_views']:,} views")

    print(f"\nFiles saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
