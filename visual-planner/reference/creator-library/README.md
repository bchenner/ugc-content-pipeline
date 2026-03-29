# Creator Library

Reference library of scanned creator accounts. Each account has a profile.json with metadata and links to downloaded frames for visual analysis.

## Scan Status

### Fresh Data (last 30 days as of 2026-03-28)

| Account | Platform | Category | Top Views | Videos | Scan Date | Data Freshness |
|---------|----------|----------|-----------|--------|-----------|---------------|
| @wellnessmaddie1 | Instagram | Practitioner Demo + Patient exam | 256K | 10 | 2026-03-28 | **FRESH** — videos from Mar 2026 |
| @naturefixhealth1 | Instagram | B-roll source (faceless recipe) | 1.5M | 5 | 2026-03-28 | **FRESH** — videos from Mar 2026 |

### Older Data (analyzed but source videos may be outdated)

| Account | Platform | Category | Analyzed | Source Video Age | Status |
|---------|----------|----------|----------|-----------------|--------|
| @sidneystea | TikTok | Hooks (greenscreen commentary) | 2026-03-27 | Videos from Dec 2025 — Feb 2026 | Mixed freshness |
| @ardenremedy | Instagram | Practitioner Demo | 2026-03-27 | Videos ~Mar 2026 | Likely fresh |
| @dailyhealthtalk | TikTok | AI Podcast | 2026-03-26 | Upload date unknown, likely 2025 | ⚠️ STALE |
| @catpnut | TikTok | Mixed-Media Animation | 2026-03-26 | Upload date unknown, likely 2025 | ⚠️ STALE |
| @misshealer_ | TikTok | Storytelling Confession | 2026-03-26 | Upload date unknown, likely 2025 | ⚠️ STALE |
| @leefar.podcast | TikTok | Borrowed Authority | 2026-03-26 | Upload date unknown, likely 2025 | ⚠️ STALE |
| @zxaspoa | TikTok | AI Avatar Historical | 2026-03-26 | Upload date unknown, likely 2025 | ⚠️ STALE |
| Old Hook Vault | TikTok | 16 individual URLs | 2026-03-28 | **2025-02 to 2025-08 (7-13 months old)** | ⚠️ OUTDATED |

## Not Scannable

| Account | Platform | Issue |
|---------|----------|-------|
| @ancient.amani | TikTok | yt-dlp impersonation error, ScrapeCreators returns 0 items |
| @livefreehealthco | TikTok | 0 videos found (account may be dead or renamed) |
| @shelfcritism | TikTok | 0 videos found |
| @healthh.tipsss_ | Instagram | ScrapeCreators 404 (handle may be wrong) |
| @trucos.debelleza8 | Instagram | ScrapeCreators 404 |
| @bodyhealing101 | Instagram | No viral content in last 30 days |
| @alchemy_glowlab | Instagram | 1.1M top views but NOT in last 30 days |

## Account Categories

### Format References (study the video TYPE)
Accounts that demonstrate distinct visual formats worth replicating:
- @wellnessmaddie1 — Practitioner Demo with patient interaction
- @ardenremedy — Practitioner Demo (AI avatar version)
- @dailyhealthtalk — AI Podcast with prehook
- @catpnut — Mixed-Media Animation (pure, no speaker)
- @misshealer_ — Storytelling Confession (car, zero B-roll)
- @leefar.podcast — Borrowed Authority (speaker wallpaper + text)
- @zxaspoa — AI Avatar Historical

### Hook References (study the HOOK TEXT, not the format)
- @sidneystea — Outrage/urgency hook formulas, greenscreen commentary

### B-Roll Sources (download their footage to overlay avatar on)
- @naturefixhealth1 — High-quality faceless recipe clips (14-24s, 1.5M views)
- @bodyhealing101 — Recipe/health B-roll
- @wonderfulrecipesandtips — Recipe B-roll
- @alchemy_glowlab — Recipe/glow B-roll (older content, high views)

## New Formats Found

No new video types discovered beyond the 13 already documented. All scanned accounts map to existing types:
- Practitioner Demo (wellnessmaddie1, ardenremedy)
- Green Screen Commentary (sidneystea)
- Faceless Hands-Only (naturefixhealth1 — B-roll source)

## How to Use

1. Run `/creator-scanner @username --platform instagram --min-views 50000` to scan new accounts
2. Read prehook frames in `scan-{username}/frames/{username}_NN/prehook_01.jpg`
3. Add findings to this README
4. If a new video type is found, create a reference file in `../video-types/`
