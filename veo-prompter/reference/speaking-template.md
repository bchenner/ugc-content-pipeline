# Veo 3 Speaking-to-Camera Template
<!-- date: 2026-03-13 -->

Master template for generating natural, engaging speaking-to-camera videos. Based on research from TED Talk analysis (1,000+ talks), public speaking science, and content creator best practices.

---

## THE PRINCIPLE

Veo 3 generates better speaking videos when you describe WHAT the person DOES physically — not just what they say. The more specific the physical behavior, the more natural and engaging the output.

Key insight from TED research: **viral speakers use 71% more hand gestures** than low-performing speakers. The #1 predictor of engagement is not what someone says — it's how much they move while saying it.

---

## TEMPLATE STRUCTURE

Every speaking-to-camera video prompt should include these 5 sections:

```
1. SETUP — Who, where, framing, camera
2. DIALOGUE — What they say, delivery style
3. BODY — Posture, weight shifts, leans
4. HANDS — Specific gestures synced to speech beats
5. FACE — Micro-expressions synced to emotional beats
```

---

## 1. SETUP

Describe the physical scene. Keep it simple — Veo handles complex setups poorly.

```
A [age] [gender] sitting in a [setting], [framing] shot.
[Lighting description]. [Camera style].
```

**Framing options:**
- `waist-up` — standard podcast/talking head (most reliable)
- `close-up shoulders and above` — intimate, emotional content
- `medium shot from hips up` — shows more gesture range

**Camera options:**
- `camera is stationary at eye level` — clean, professional
- `slight handheld drift` — use start/end frame offset for natural sway
- `(thats where the camera is)` — Veo 3 syntax for camera-aware processing

---

## 2. DIALOGUE

Use colon format to prevent subtitle generation:

```
She says: "[dialogue]"
```

**Delivery descriptors that Veo responds to:**

| Energy Level | Descriptors |
|-------------|------------|
| High energy | "animated, emphatic, passionate, urgent, fast-paced" |
| Conversational | "casual, warm, like talking to a friend, relaxed pace" |
| Authoritative | "confident, measured, deliberate, steady" |
| Vulnerable | "quiet, honest, slightly hesitant, intimate" |
| Contrarian | "firm, challenging, raised eyebrows, slight head shake" |

**Pacing descriptors:**
- `speaks at a natural conversational pace with brief pauses between thoughts`
- `starts slow and builds energy as she reaches the key point`
- `pauses after the question to let it land, then answers directly`

---

## 3. BODY — Posture & Movement

Static speakers look dead on camera. Add these physical anchors:

### Posture Base
```
Sitting upright but relaxed, shoulders back and down, slight forward lean toward the camera.
```

### Weight Shifts (pick 1-2 per scene)

| Movement | When to Use | Prompt Language |
|----------|-------------|-----------------|
| **Lean forward** | Emphasizing a key point, sharing something important | "leans slightly forward toward the camera as she says [key phrase]" |
| **Lean back** | Reflecting, pausing for effect, casual aside | "leans back slightly, takes a breath" |
| **Head tilt to one side** | Showing empathy, asking a question, being thoughtful | "tilts her head slightly to one side" |
| **Slight head shake** | Disagreeing, negating, myth-busting | "gives a slight head shake as she says 'that's not true'" |
| **Single nod** | Affirming, agreeing with the viewer, landing a point | "nods once, firmly" |
| **Posture reset** | Between major beats, transitioning topics | "settles back into her chair, resets her posture" |

---

## 4. HANDS — Gesture Library

Hands are the #1 engagement driver. Every 8-second scene should have at least 1-2 intentional hand movements. Keep them between shoulders and waist for best Veo results.

### Gesture Types

| Gesture | Physical Description | When to Use |
|---------|---------------------|-------------|
| **Open palms** | "holds both hands open, palms facing up" | Being honest, presenting facts, "here's the truth" |
| **Counting** | "holds up one finger, then two, then three" | Listing items, steps, reasons |
| **Pinch/precision** | "brings thumb and index finger together" | Emphasizing a specific detail, "this ONE thing" |
| **Spread apart** | "moves both hands apart, palms facing each other" | Showing scale, contrast, "the difference between X and Y" |
| **Bring together** | "brings both hands together in front of her" | Connecting two ideas, "when you combine these" |
| **Dismissive wave** | "waves one hand to the side dismissively" | Rejecting a bad idea, "forget what you've heard" |
| **Point at camera** | "points one finger toward the camera" | Direct address, "YOU need to hear this" — use sparingly |
| **Touch chest** | "places one hand on her chest" | Personal story, "I went through this" |
| **Rest on surface** | "rests one hand flat on the table/desk" | Grounding, authority, calm confidence |
| **Hold product** | "picks up [product] with one hand, holds it at chest level" | Product reveal, showing what she's talking about |
| **Steeple** | "fingers touching in a tent/steeple shape" | Authority, confidence, processing a thought |

### Gesture Rules for Veo 3
- **Keep gestures broad and simple** — Veo struggles with complex finger positions
- **Anchor hands to a surface when possible** — prevents floating/distorted hands
- **One gesture at a time** — don't stack multiple simultaneous movements
- **Give hands a starting position** — "hands resting on the desk" or "one hand on her lap"

---

## 5. FACE — Micro-Expression Library

The face is where emotional connection happens. Veo can render these when prompted explicitly.

| Expression | Physical Description | When to Use |
|-----------|---------------------|-------------|
| **Eyebrow raise** | "raises her eyebrows slightly" | Revealing a surprising fact, asking a rhetorical question |
| **Eyebrow furrow** | "furrows her brow" | Concern, confusion, "this is serious" |
| **Duchenne smile** | "smiles genuinely — eyes crinkle, whole face lifts" | Warmth, connection, positive moments, after landing a point |
| **Half-smile / knowing look** | "gives a slight knowing smile" | Sharing insider info, "here's what they don't tell you" |
| **Pursed lips / thinking** | "presses her lips together briefly, thinking" | Processing, pausing before an important revelation |
| **Wide eyes** | "eyes widen slightly" | Shock, emphasis, "can you believe this?" |
| **Soft eyes** | "softens her expression, looks directly into the camera" | Empathy, vulnerability, "I understand what you're going through" |
| **Eye roll to side** | "glances to the side briefly, then back to camera" | Recalling something, casual "oh and one more thing" |

### Expression Rules for Veo 3
- **Avoid "bug eyes" or "cartoonish" expressions** — add to negative prompt
- **Sync expressions to speech beats** — "raises her eyebrows AS she says 'did you know'"
- **One expression transition per scene** — don't rapid-fire expressions

---

## PUTTING IT ALL TOGETHER

### Example: Educational Talking Head (Cortisol Video)

```json
{
  "mode": "first-to-last-frame",
  "duration": "8s",
  "scene": "A woman in her late 20s sitting at a clean desk, waist-up shot. Soft natural window light from the left. Neutral wall behind her with a small plant. Smartphone camera at eye level, slight handheld feel (thats where the camera is). She wears a casual cream knit top. One hand resting on the desk, the other in her lap.",
  "dialogue": {
    "speaker": "woman",
    "line": "So why do you wake up at 3am every single night? It's not insomnia. It's cortisol.",
    "delivery": "conversational, warm, like explaining something to a friend. Starts with a curious tone on the question, then shifts to confident and direct on the answer."
  },
  "body": "Sitting upright but relaxed, slight forward lean. Tilts her head slightly to one side as she asks the question. Gives a single firm nod as she delivers the answer.",
  "hands": "Right hand rests on the desk. As she asks the question, she lifts her left hand with open palm. When she says 'cortisol' she brings her thumb and index finger together in a precision pinch gesture, then rests her hand back down.",
  "face": "Raises her eyebrows slightly on 'why do you wake up at 3am' — curious expression. Brief pause. Then her expression shifts to knowing confidence — slight half-smile, direct eye contact — as she says 'It's cortisol.'",
  "negative_prompt": "cartoonish eyes, bug eyes, exaggerated expressions, stiff posture, hands in lap the entire time, monotone delivery, looking away from camera, background music, subtitles, text overlays"
}
```

### Example: Myth-Busting (Contrarian Hook)

```json
{
  "mode": "first-to-last-frame",
  "duration": "8s",
  "scene": "Same woman, same desk setup. Waist-up, soft natural light, neutral background. Smartphone at eye level (thats where the camera is). Wearing the same cream knit top.",
  "dialogue": {
    "speaker": "woman",
    "line": "Stop taking melatonin for your 3am wake-ups. You don't have a melatonin problem. You have a cortisol problem.",
    "delivery": "firm and direct on 'stop taking melatonin' — almost a command. Then softens slightly to conversational authority as she explains why."
  },
  "body": "Leans forward as she says 'stop.' Slight head shake on 'you don't have a melatonin problem.' Settles back and nods once on 'cortisol problem.'",
  "hands": "Starts with hands resting on desk. Raises one hand palm-out in a 'stop' gesture on the first word. Waves that hand dismissively to the side on 'melatonin problem.' Then brings thumb and index finger together on 'cortisol problem' — precision gesture.",
  "face": "Eyebrows slightly raised and firm expression on 'stop taking melatonin.' Slight head shake with eyebrow furrow on 'you don't have a melatonin problem.' Then shifts to knowing half-smile, direct eye contact, slight nod on 'you have a cortisol problem.'",
  "negative_prompt": "cartoonish eyes, bug eyes, exaggerated expressions, aggressive pointing, angry expression, background music, subtitles, text overlays"
}
```

### Example: Vulnerable / Relatable Content

```json
{
  "mode": "first-to-last-frame",
  "duration": "8s",
  "scene": "Same woman, same desk. Waist-up. Softer lighting — slightly dimmer, warmer. Smartphone at eye level (thats where the camera is).",
  "dialogue": {
    "speaker": "woman",
    "line": "If you forgot a word mid-sentence today... if you stood in a room and forgot why you walked in... this is for you.",
    "delivery": "quiet, honest, slightly slower pace. Like sharing something personal. Pauses between the two 'if' statements."
  },
  "body": "Relaxed posture, slight lean forward. Stays mostly still — the stillness conveys intimacy. Slight head tilt on 'this is for you.'",
  "hands": "Both hands resting on the desk. Minimal movement — she lifts one hand slightly on 'this is for you' with an open palm gesture, then rests it back.",
  "face": "Soft eyes throughout — empathetic, understanding. Slight pursed lips between the two 'if' statements, as if remembering. Then a gentle genuine smile — eyes crinkle slightly — on 'this is for you.'",
  "negative_prompt": "big smile, overly cheerful, energetic gestures, fast movements, background music, subtitles, text overlays"
}
```

---

## QUICK REFERENCE: MATCHING CONTENT TYPE TO PHYSICAL STYLE

| Content Type | Energy | Gestures | Face | Body |
|-------------|--------|----------|------|------|
| **Hook / Question** | Medium-high | Open palm on question, precision on answer | Eyebrow raise → knowing look | Lean forward, head tilt |
| **Contrarian / Myth-bust** | High | Stop gesture, dismissive wave, precision pinch | Firm brow → head shake → half-smile | Lean forward, head shake, nod |
| **Educational / Fact** | Medium | Counting, spread apart, bring together | Eyebrow raise on facts, nod on conclusions | Upright, steady, slight lean |
| **Recipe / How-to** | Medium-warm | Counting steps, open palms, pointing at items | Friendly smile, eyebrow raise on tips | Relaxed, occasional lean |
| **Relatable / Emotional** | Low-medium | Minimal — hand on chest, one open palm | Soft eyes, pursed lips, gentle smile | Still, slight lean, head tilt |
| **Product Reveal** | Medium-high | Pick up product, hold at chest, open palm | Genuine smile, slight eyebrow raise | Lean forward on reveal |
| **CTA / Close** | Medium | Open palm toward camera, counting benefits | Direct eye contact, confident smile, nod | Lean forward, single nod |

---

## NEGATIVE PROMPT DEFAULTS

Always include in every speaking video prompt:

```
"cartoonish eyes, bug eyes, exaggerated eye popping, unrealistic eye widening, stiff robotic posture, hands frozen in lap, monotone flat delivery, looking away from camera, wandering eyes, background music, sound effects, subtitles, captions, text overlays, words on screen"
```

Add scene-specific negatives as needed (e.g., "angry expression" for warm content, "big smile" for vulnerable content).

---

## SOURCES

Research basis for this template:

- [TED Talk body language analysis — 10 patterns from 1,000 talks](https://vegoutmag.com/lifestyle/gen-i-studied-1000-ted-talks-here-are-the-10-body-language-patterns-all-great-speakers-share/)
- [TED Blog — 5 nonverbal features that make talks go viral](https://blog.ted.com/body-language-survey-points-to-5-nonverbal-features-that-make-ted-talks-take-off/)
- [Science of People — 760 volunteers decode TED talks](https://www.scienceofpeople.com/secrets-of-a-successful-ted-talk/)
- [7 ways to be a better communicator via body language (TED Ideas)](https://ideas.ted.com/7-ways-to-be-a-better-communicator-by-tweaking-your-body-language/)
- [Fast Company — hand gestures make you look more competent](https://www.fastcompany.com/91454761/talking-hand-gestures-look-more-competent-ted-talks)
- [Toastmasters — gestures and body language guide](https://www.toastmasters.org/resources/public-speaking-tips/gestures-and-body-language)
- [vidIQ — YouTube skills for speaking on camera](https://vidiq.com/blog/post/youtube-skills-speaking-on-camera/)
- [Teleprompter.com — 5 tips for camera confidence](https://www.teleprompter.com/blog/5-tips-to-speak-well-on-camera)
