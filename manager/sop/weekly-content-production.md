# Weekly Content Production SOP

Standard operating procedure for producing one week of Salvora Rhodiola content across 6 accounts (3 EN, 3 ES).

## Weekly Output

| Content Type | Per Account/Day | Daily Total | Weekly Total | Script Length |
|-------------|----------------|------------|-------------|---------------|
| Sales videos | 1 | 6 | 30 | 1:30 to 2:30 |
| Growth videos | 2 | 12 | 60 | 0:30 to 1:00 |
| **Total** | **3** | **18** | **90** | |

## Unique Scripts Needed

| Type | Unique EN | Translated ES | Total Scripts |
|------|-----------|--------------|---------------|
| Sales body scripts | 3 | 3 | 6 |
| Prehooks | 10 | 10 | 20 |
| Growth scripts | 20 | 20 | 40 |
| **Total** | **33** | **33** | **66** |

## Account Structure

| Account | Avatar | Archetype | Sales Body | Growth Scripts |
|---------|--------|-----------|------------|----------------|
| EN-1 | Black guy | Naturopath | Assigned body script | Shares pool of 4/day |
| EN-2 | Asian Doctor | Doctor/Pharmacist | Assigned body script | Shares pool of 4/day |
| EN-3 | White Female 50s | Nurse Practitioner | Assigned body script | Shares pool of 4/day |
| ES-1 | Holistic Mom | Nutritionist | Translated EN-1 body | Translated pool |
| ES-2 | Old Indian Man | Ayurvedic Scholar | Translated EN-2 body | Translated pool |
| ES-3 | Korean Doctor | Doctor | Translated EN-3 body | Translated pool |

## Weekly Production Timeline

### Day 1 (Planning Day, ideally Friday before)

**Step 1: Review last week's data**
- Check account health: any accounts under 1K views for 15-20 posts? → test new style
- Under 200 views for first 10-15 posts? → trash account
- FB working but IG not? → stop cross-posting same file, change prehook for IG
- Identify top-performing prehooks and body scripts from last week

**Step 2: Decide what carries over**
- Pick 2 prehooks from last week to keep (best performers)
- Decide which body scripts continue vs. which get replaced
- Plan 8 new prehook concepts for the week

**Step 3: Plan growth content**
- Choose 20 unique topics across 4 categories (4/day):
  - Cortisol Education (how the body works)
  - Relatable Moment (emotional validation)
  - Recipe/Hack (actionable tips)
  - Motivation/Identity (reframing, empowerment)
- Apply 50/50 format split: half podcast style, half proven throwback formats

**Step 4: Plan sales content**
- Assign body scripts to accounts (or keep existing)
- Plan prehook rotation: 2 per day, Mon-Fri

### Day 2-3 (Script Production)

**Step 5: Write growth scripts**
Delegate to Script Writer (Mode 5) in batches of 5:

```
Agent → Script Writer
Brief: 5 growth scripts, educational, NO product mention, NO CTA
Format: 30-60 seconds (75-120 words each)
Target: Women 35-55, cortisol/menopause/stress
Tone: Rotate between doctor (educational) and NP (relatable)
Output: Save to projects/[project-folder]/growth-scripts-week[N]-batch[N].md
```

Run 4 batches in parallel = 20 scripts.

**Step 6: Write new sales scripts (if any)**
Delegate to Script Writer (Mode 5):

```
Agent → Script Writer
Brief: Sales script with specific pattern (Q, V, T, etc.)
Avatar: Assigned account avatar
Sales channel: Amazon keyword CTA ("comment LINK")
Format: 1:30 to 2:30 (250-350 words)
Include: Open loop after hook, natural skepticism, specific transformation timeline
Output: Save to projects/[project-folder]/
```

**Step 7: Write prehook voiceovers**
Delegate to Script Writer:

```
Agent → Script Writer
Brief: 10 prehook scripts (2-3 second visual hook + voiceover line)
Format: 1-2 sentences each, punchy, symptom-focused
Output: Save to projects/[project-folder]/prehook-scripts-week[N].md
```

**Step 8: Translate all scripts to Spanish**
Delegate to Script Writer (Mode 2) in batches:

```
Agent → Script Writer (Mode 2)
Input: All EN scripts from Steps 5-7
Target language: Spanish
Output: Save with -es suffix
```

### Day 3-4 (Visual Production)

**Step 9: Visual storyboard for each script**
Delegate to Visual Planner:

```
Agent → Visual Planner
Input: Approved script, visual direction, B-roll density, product info, avatar details
Output: User summary + internal detail
```

For growth videos (30-60s): minimal B-roll, mostly talking head.
For sales videos (1:30-2:30): medium B-roll density.

**Step 10: Generate image + video prompts**
Delegate to Image Prompter + Veo Prompter:

```
Agent → Image Prompter: Scene reference images (one per shared group)
Agent → Veo Prompter: Speaking scene video prompts (universal template, swap dialogue)
Agent → Veo Prompter: B-roll video prompts (natural language, no dialogue)
```

**Step 11: Generate PatchWork files**
Delegate to PatchWork Importer:

```
Agent → PatchWork Importer
Input: All image prompts, video prompts, scene structure
Output: .nbflow file in patchwork-importer/output/
```

### Day 4-5 (Assembly + QA)

**Step 12: Import and run PatchWork workflows**
- Import .nbflow files into PatchWork
- Load reference images (avatar photo, product photo)
- Run image generation
- Review and approve images
- Run video generation
- Review and approve videos

**Step 13: Post-production**
- Edit prehook clips together with voiceover/text overlay
- Attach B-roll clips to speaking scenes
- Add any text overlays or captions
- Export final videos

**Step 14: Schedule and post**
- Upload to posting tool
- Set captions/descriptions per platform
- Schedule: 3 videos/day per account (2 growth + 1 sales)
- Ensure ManyChat keyword matches video topic (Amazon channel)

## Prehook Rotation Template

| Day | Prehook A | Prehook B |
|-----|-----------|-----------|
| Mon | [Kept from last week] | [New] |
| Tue | [Kept from last week] | [New] |
| Wed | [New] | [New] |
| Thu | [New] | [New] |
| Fri | [New] | [New] |

All 6 accounts on a given day use one of that day's two prehooks. Batched for production efficiency.

## Growth Script Categories

| Category | Purpose | Tone | Example Hook |
|----------|---------|------|-------------|
| Cortisol Education | Teach how the body works | Doctor, educational | "Why you wake up at 3am every night" |
| Relatable Moment | Emotional validation | NP, warm, "I see you" | "When your kids ask why mom is always angry" |
| Recipe/Hack | Actionable tips | Doctor, practical | "Stop drinking coffee first thing" |
| Motivation/Identity | Reframe, empower | NP, empowering | "You're not lazy. Your body is in survival mode" |

Distribute: 4 scripts/day, rotate categories. Friday = mixed best-of.

## Content Strategy Rules

- **50/50 split**: Half current viral styles (podcast), half proven formats from 60-90 days ago
- **3:1 posting ratio** while under 50k followers (2 growth + 1 sales per account)
- **At 50k followers**: Shift to 1:1 engaging:salesy
- **Cross-platform**: Pull winning TikTok frameworks from 2-3 months ago → Amazon/Meta
- **Amazon content**: No violations, can use extreme visuals, strong authority figures, copyrighted music
- **Growth videos**: No CTA, no product mention, pure value
- **Sales videos**: Amazon keyword CTA ("comment LINK" → ManyChat auto-DM)

## File Organization

```
manager/projects/
  [product-start-date]/          (e.g., salvora-march-16-2026)
    growth-scripts-week[N]-batch[1-4].md
    sales-[pattern]-[avatar].md
    prehook-scripts-week[N].md
    [video-project-folders]/
      video-plan.md
      main-body/
      prehooks/
      broll/
```

## Agent Delegation Quick Reference

| Task | Agent | What to Pass |
|------|-------|-------------|
| Growth/sales scripts | Script Writer (Mode 5) | Brief, audience, pattern, constraints |
| Script translation | Script Writer (Mode 2) | EN script, target language |
| Visual storyboard | Visual Planner | Script, visual direction, B-roll density |
| Image prompts | Image Prompter | Scene brief from storyboard |
| Video prompts (speaking) | Veo Prompter | Dialogue line (template handles rest) |
| Video prompts (B-roll) | Veo Prompter | Scene brief, natural language |
| PatchWork file | PatchWork Importer | All prompts, scene structure |
| Strategy/research | Strategist | Product info, audience, constraints |
| Trend scanning | Researcher (Viral Scanner) | Product/niche, what to look for |
