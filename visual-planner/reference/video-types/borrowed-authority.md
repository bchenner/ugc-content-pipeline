# Borrowed Authority

<!-- analysis-date: 2026-03-26 -->
> **Reference data**: Analyzed 2026-03-26. Source accounts: @leefar.podcast, @kesefinds. Upload dates unknown — likely 2025.

Repurposed authority footage (conference speakers, stage presentations, podcast clips) used as visual WALLPAPER while text overlays do all the selling. The speaker is decorative, their specific words are irrelevant, their presence signals "expert talking." A separate voiceover delivers the actual script.

## When to Use

- Supplement education, ingredient explanations, benefit lists
- When the ARGUMENT (text) is stronger than the delivery (performance)
- Authority credibility without filming an actual expert
- Lowest production effort for the main body: one speaker clip reused for the entire video
- Long-form scripts (60-120s+) where visual variety isn't needed

## Visual Structure

```
[PREHOOK: Body close-up / transformation shot / symptom visual — separate from main body]
    ↓ hard cut
[FULL SCREEN: Authority figure speaking on stage/podium — single uncut clip]
[TEXT LAYER 1: Persistent headline badge — the promise, fixed position]
[TEXT LAYER 2: Kinetic captions — word-by-word, lower third, bold colors]
    ↓ static for 60-90s
[SAME CLIP: + red CTA arrow + "GRAB YOURS" text]
```

- Authority speaker clip occupies 100% of the frame for the entire main body
- Speaker's actual words are inaudible/irrelevant, replaced by separate voiceover
- Text does ALL the selling via two stacked layers
- Prehook is always a different visual register (body close-up, symptom shot, transformation proof)
- No product shown until CTA (or not at all)

## Scene Layout

| Element | Frame Position | Size |
|---------|---------------|------|
| Authority speaker | Full screen | 100% |
| Persistent headline badge | Mid-frame, centered | Pill-shaped overlay, bold color |
| Kinetic captions | Bottom third | Large bold text, phrase-by-phrase |
| Red CTA arrow | Mid-frame (final frames only) | Overlay, pointing down |
| PiP avatar (prehook only) | Bottom-right corner | ~15-20% inset |
| Prehook visual | Full screen | 100% (before hard cut to speaker) |

## Camera

- Speaker clip: medium shot, stage or podium, professional lighting (bokeh, colored stage lights)
- 9:16 vertical
- Single angle, single take
- Conference/keynote aesthetic (purple/blue/magenta stage lighting, formal backdrop)
- Speaker wears formal attire (suit, blazer), holds or stands near a microphone

## Reference Image Groups

- **Prehook image** (full prompt): Body close-up, symptom shot, or transformation proof. Separate visual register from the main body.
- **Authority speaker image** (full prompt): Person at podium/stage, formal attire, mic, professional lighting. This single image is the reference for the entire main body.
- **PiP avatar image** (optional, prehook only): Small inset of the narrator/avatar, used as picture-in-picture overlay during the prehook.

## Scene Segmentation

- Prehook: 1-2 clips (body close-up, symptom visual, before/after)
- Main body: ONE speaker clip, held for the entire duration (60-90+ seconds)
- The speaker clip does NOT need scene-by-scene segmentation since it's a single uncut take
- Text layers create all the "editing" — visual cuts are unnecessary
- CTA: Same speaker clip with red arrow overlay added in post

## Text Layer Architecture

Two persistent text layers run simultaneously over the speaker footage:

| Layer | Purpose | Behavior | Style |
|-------|---------|----------|-------|
| Headline badge | The promise / hook summary | Stays fixed for entire video | Pill-shaped, bold color (red, pink), mid-frame |
| Kinetic captions | The argument, word-by-word | Changes phrase-by-phrase, synced to voiceover | Large bold, lower third, high contrast (yellow, white) |

The headline badge anchors the viewer's attention on the core promise. The kinetic captions deliver the script argument one phrase at a time, keeping reading pace manageable.

## Beat Structure

This format has minimal visual transitions — a single speaker clip is held for the entire main body. Text layers do all the selling.

```
PREHOOK (0:00-0:10):
  Body close-up, transformation shot, or symptom visual. Separate visual register from main body.
  Visual: Full screen. No text. Optional PiP avatar inset in corner.

HARD CUT TO SPEAKER (0:10):
  Authority figure appears. Badge and captions begin immediately.
  Visual: Full screen speaker at podium/stage. Persistent headline badge + kinetic captions start.

MAIN BODY (0:10-1:10):
  Problem → failed solutions → mechanism → benefits → social proof. All on one uncut clip.
  Visual: Same speaker clip held static. Badge stays fixed. Kinetic captions change phrase-by-phrase synced to voiceover.

CTA (1:10-1:20):
  Offer, promotion, shop button reference.
  Visual: Same speaker clip. Red arrow appears. "GRAB YOURS" caption.
```

Key takeaway: ONE visual change in the entire video — the hard cut from prehook to speaker. After that, the frame never changes. The persistent badge and kinetic captions do all the selling. Voiceover drives pacing, not the speaker's lip movements.

## Pipeline Mapping

| Component | Agent | Notes |
|-----------|-------|-------|
| Prehook images | Image Prompter | Body close-up, symptom shot, or transformation proof |
| Prehook motion | Veo Prompter | Start image reference, subtle motion (skin texture, hand movement) |
| Authority speaker image | Image Prompter | Full prompt: person at podium, stage lighting, formal attire, mic |
| Authority speaker clip | Veo Prompter | Single take, natural speaking gestures, no specific dialogue needed. OR use stock conference footage |
| Persistent badge | Post-production | Static overlay, designed graphic (pill shape, bold color) |
| Kinetic captions | Post-production | Word-by-word or phrase-by-phrase sync to voiceover |
| Red CTA arrow | Post-production | Appears in final frames only |
| Voiceover | Separate recording | NOT the speaker's voice. Narrator voice delivers the actual script |
| PatchWork | PatchWork Importer | Minimal: prehook image+video nodes, one speaker image+video node. Text layers are post-production |

## Key Differences from Other Formats

| vs. Talking Head | vs. Podcast Authority |
|------------------|-----------------------|
| Talking head: speaker IS the content, their words matter | Podcast authority: speaker IS speaking the script at a desk/mic/bookshelf setup |
| Borrowed authority: speaker is WALLPAPER, text is the content | Borrowed authority: speaker's audio is REPLACED by a separate voiceover |
| Talking head: multiple scenes, angle changes, B-roll cutaways | Podcast authority: the speaker's performance delivers the argument |
| Borrowed authority: one clip, zero cuts, text does the editing | Borrowed authority: text overlays deliver the argument, speaker just looks credible |

## Example

Supplement education video: Prehook shows extreme close-up of aged hand skin (3s). Hard cut to full-screen conference speaker at podium with magenta stage lighting, suit, mic (held for 90s). Pink badge reads "How women over 40 feel like she's in her 20s again." Yellow kinetic captions deliver the ingredient explanation phrase-by-phrase. Red arrow appears at 1:15 with "GRAB YOURS." Total: ~90s, one Veo speaker clip, all selling done through text.

## Reference Videos

- @leefar.podcast (97s) — [TikTok](https://www.tiktok.com/@leefar.podcast/video/7573851044438871310)
- @kesefinds (134s) — [TikTok](https://www.tiktok.com/@kesefinds/video/7550989416030866701)
