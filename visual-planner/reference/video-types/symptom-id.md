# Symptom ID

<!-- analysis-date: 2026-03-28 -->
> **Reference data**: Developed 2026-03-28. Based on @wellnessmaddie1 format (videos 03 and 08, 133K and 68K views, March 2026). Adapted for AI avatar pipeline.

Avatar physically examines a patient's body parts on camera, naming symptoms one by one. After the examination, the patient leaves frame and the avatar speaks to camera alone — connecting the symptoms to one root cause. Ends with product hold CTA.

The examination IS the hook. The tactile, clinical touch on visible body parts stops the scroll from frame 1.

Reference: @wellnessmaddie1 video 03 (133K views, 2026-03-15) — "If your chin looks like this, your belly looks like this, and your arms look like this, you are not overweight."

## When to Use

- Symptom awareness content where multiple visible signs connect to one cause
- Authority positioning — the avatar is a practitioner who can see what the viewer can't
- When the target audience experiences multiple symptoms but hasn't connected them
- Sales videos where the hook needs to be visual, not verbal
- When you have 2-4 visible body symptoms to point at (dark circles, thinning hair, neck texture, skin changes, nail condition)

## Visual Structure

```
[EXAM: Avatar touches patient body part 1, names symptom]
    ↓ hard cut (NOT Veo morph)
[EXAM: Avatar touches patient body part 2, names symptom]
    ↓ hard cut
[EXAM: Avatar touches patient body part 3, names symptom]
    ↓ hard cut
[SPEAKING: Patient gone. Avatar alone, faces camera. Connects symptoms to one cause]
    ↓ same shot
[SPEAKING: Mechanism explanation, why this happens]
    ↓ same shot
[PRODUCT: Avatar holds up product. CTA]
```

Each exam scene is a standalone clip. Scene-to-scene transitions are hard cuts done in post editing, NOT Veo-generated morphing between frames.

## Beat Structure

```
EXAM HOOK (first 10-15 seconds, 2-4 body parts):
  Each body part gets ~3-5 seconds
  Avatar's hand touches/points at the area
  Text: "If your [body part] looks like this"
  Rapid, clinical energy. Boom boom boom. One per sentence.
  The physical examination IS the scroll-stop
  Patient faces camera, avatar stands slightly behind/beside

REFRAME (5-8 seconds):
  Patient exits frame (hard cut, not animated)
  Avatar faces camera alone
  "You do not have three separate problems."
  Connects all symptoms to one root cause
  This is the retention hook at ~10 second mark

MECHANISM (15-25 seconds):
  Avatar speaks to camera, explains why this happens
  No patient, no props, no visual changes. Just speaking.
  Authority delivery, not emotional

PRODUCT CTA (5-10 seconds):
  Avatar holds up product bottle
  Names the product
  Comment keyword CTA
```

## Image Generation — Foundation-Anchor-Fan Pattern

This format uses the Foundation-Anchor-Fan approach for image consistency:

### Layer 1 — Foundations (depth 0, generated independently)

| Foundation | What | Purpose |
|---|---|---|
| Office setting | Empty room, no people. Camera angle matches exam scenes. | Grounds all scenes in the same room |
| Patient character | Full character reference from scratch. Must show ALL symptoms visibly (dark circles, thinning hair, neck lines, etc.) | Consistent patient identity across scenes |
| Avatar | Uploaded photo (not generated) | Consistent avatar identity |
| Product | Uploaded photo | For product hold scene |
| Symptom close-ups | One per body part examined. Each refs patient character. Extreme close-up showing the specific symptom detail. | Visual evidence of each symptom, used as reference for exam scenes |

### Layer 2 — Anchor (depth 1)

The FIRST exam scene (body part 1) combines all foundations:
- Avatar + Patient character + Office setting + Close-up of symptom 1
- This approved image becomes the anchor — ground truth for the video's visual identity

### Layer 3 — Fan-out (depth 1, all reference the anchor)

Every remaining scene references the anchor directly:
- Exam scene 2: Avatar + Patient + Office + Close-up 2 + **Anchor approval**
- Exam scene 3: Avatar + Patient + Office + Close-up 3 + **Anchor approval**
- Speaking scene: Avatar + Office + **Anchor approval**
- Product scene: Avatar + Product + Office + **Anchor approval**

No daisy-chaining between scenes. Max depth stays at 1.

### Veo Structure

| Veo Node | Start Frame | End Frame | Notes |
|---|---|---|---|
| Exam scene 1 | Exam 1 approval | None | Standalone clip |
| Exam scene 2 | Exam 2 approval | None | Standalone clip |
| Exam scene 3 | Exam 3 approval | None | Standalone clip |
| Speaking scenes | Speaking approval (Dynamic/Template with {dialogue}) | None | Multiple dialogues from dropdown |
| Product reveal | Speaking approval | Product approval | Only transition that uses end frame |
| Product CTA | Product approval | None | Standalone clip |

## PatchWork Structure

```
MEDIA NODES:
  Avatar (upload)
  Product (upload)

FOUNDATION GEN CHAINS:
  Office setting: Prompt → NanobananaAPI → Approval
  Patient character: Prompt → NanobananaAPI → Approval
  Close-up 1: Prompt → NanobananaAPI (refs patient approval) → Approval
  Close-up 2: Prompt → NanobananaAPI (refs patient approval) → Approval
  Close-up 3: Prompt → NanobananaAPI (refs patient approval) → Approval

ANCHOR:
  Exam 1: Prompt → NanobananaAPI (refs avatar + patient + office + closeup 1) → Approval
  ↓ This approval fans out to everything below

FAN-OUT SCENES:
  Exam 2: Prompt → NanobananaAPI (refs avatar + patient + office + closeup 2 + ANCHOR) → Approval
  Exam 3: Prompt → NanobananaAPI (refs avatar + patient + office + closeup 3 + ANCHOR) → Approval
  Speaking: Prompt → NanobananaAPI (refs avatar + office + ANCHOR) → Approval
  Product: Prompt → NanobananaAPI (refs avatar + product + office + ANCHOR) → Approval

VEO NODES:
  Exam 1-3: Start frame only → Approval (video)
  Speaking: Dynamic/Template → Start frame only → Approval (video)
  Product reveal: Start = speaking approval, End = product approval → Approval (video)
  Product CTA: Start frame only → Approval (video)
```

## Scene Layout

| Element | Frame Position |
|---|---|
| Avatar | Slightly behind and to the side of patient. Standing. |
| Patient | Facing camera, center frame. Upper body visible. |
| Avatar's hand | On the specific body part being examined. Anchored. |
| Text overlay | Mid-screen, bold, "IF YOUR [PART] LOOKS LIKE THIS" |

After patient leaves:
| Element | Frame Position |
|---|---|
| Avatar alone | Center frame, direct to camera |
| Product (CTA) | Held at mid-chest height, label facing camera |

## Camera

- Same angle for ALL exam scenes and speaking scenes (established by office setting image)
- Slightly off center, eye level
- Upper body framing — enough room for two people side by side
- Static. No camera movement. Smartphone propped across the room.
- 9:16 vertical

## Key Differences from Other Formats

**vs. Talking Head**: Talking head is one person speaking. Symptom ID has two people in the exam scenes, with physical contact/examination. The patient's body IS the visual content.

**vs. Practitioner Demo**: Practitioner demo has the avatar interacting with ingredients/objects. Symptom ID has the avatar interacting with a PERSON's body. The patient is the subject, not ingredients.

**vs. Mixed-Media PiP**: Mixed-media cycles rendered backgrounds behind a PiP speaker. Symptom ID is full-frame, real people, one continuous setting. No PiP, no rendered backgrounds.

## Pipeline Mapping

| Component | Agent | Notes |
|---|---|---|
| Office setting image | Image Prompter | Empty room, no people. Establishes angle and environment |
| Patient character image | Image Prompter | From scratch, no reference. Must show all symptoms |
| Symptom close-ups | Image Prompter | One per body part. Refs patient approval |
| Exam scene images | Image Prompter | Two people in office. Refs avatar + patient + office + close-up + anchor |
| Speaking image | Image Prompter | Avatar alone in same office. Refs anchor |
| Product hold image | Image Prompter | Avatar with product. Refs anchor |
| Exam Veo clips | Veo Prompter | Start frame only. Standalone clips |
| Speaking Veo clips | Veo Prompter | Dynamic/Template with {dialogue}. Start frame only |
| Product reveal Veo | Veo Prompter | Start = speaking, End = product hold. Only Veo with end frame |
| Post-production | Manual | Hard cuts between exam clips, text overlays |

## Storyboard Adjustments

When planning this video type:
- Decide the 2-4 body parts FIRST. Each one needs a visible, relatable symptom that photographs well
- The patient character prompt must describe ALL symptoms in one image (the overall reference)
- Each exam scene only changes the hand position — everything else (room, people, angle) stays identical
- The patient exits between exam and speaking sections. This is a hard cut, not animated
- Speaking section is standard talking head (same rules as talking-head.md)
- Product reveal is the only transition with an end frame
- Total duration typically 45-75 seconds (10-15s exam + 20-30s speaking + 5-10s CTA)
