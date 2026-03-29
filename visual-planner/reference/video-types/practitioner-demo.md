# Practitioner Demo

<!-- analysis-date: 2026-03-27 -->
> **Reference data**: Analyzed 2026-03-27. Source accounts: @ardenremedy (3 videos). Videos downloaded 2026-03-27. Upload dates within ~2 weeks of download.

Full-frame AI avatar performs a hands-on remedy or treatment on camera. The avatar is NOT a small PiP overlay — they occupy the full frame and physically demonstrate the technique: applying paste to a patient's skin, holding ice to their own foot, mixing ingredients on a table in front of them. The avatar is both speaker and practitioner.

Reference: @ardenremedy (3 videos analyzed, 36-80s) — AI elderly Chinese healer demonstrating remedies in outdoor pergola setting.

## When to Use

- Recipe/remedy content where the avatar physically demonstrates the technique (not just describes it)
- "Ancient wisdom" or traditional medicine positioning where a healer figure treats a patient on camera
- When the remedy involves visible action (applying paste, brushing nails, pressing ice, bandaging)
- Product CTA that uses a physical prop (book, bottle) held up to camera at the end
- When you want higher trust than PiP overlay — the avatar "doing the work" reads as more authentic

## Visual Structure

```
[FULL-FRAME AVATAR: Hook — demonstrates action or shows the problem on patient/self]
    ↓
[SAME FRAME: Recipe preparation — ingredients on table, mixing in bowl, hands visible]
    ↓
[SAME FRAME: Application — avatar applies remedy to patient or self]
    ↓
[SAME FRAME: Mechanism explanation — avatar speaks directly to camera]
    ↓
[SAME FRAME: CTA — avatar holds up book/product, "comment [keyword]"]
```

Key: The camera angle and setting stay CONSTANT. There are no cuts, no PiP, no background changes. The visual variety comes from what the avatar is DOING in the frame: showing a foot, chopping ingredients, mixing in a bowl, applying a bandage, holding up a book.

## Setting and Props

The format requires a fixed setting with a work surface and ingredients within arm's reach. Avatar, setting, and props are all determined by the brief — there is no default. The Visual Planner chooses these based on the avatar archetype, product, and visual direction from the Manager.

| Element | What to Define | Examples |
|---------|---------------|----------|
| Setting | Fixed location where the practitioner works. Must have room for a table/surface and a patient (if applicable) | Outdoor pergola at night, kitchen counter, clinic exam room, garden table, apothecary shop |
| Avatar | The healer/practitioner archetype. Defined by the brief, not this reference file | Elderly Chinese healer, African herbalist, holistic mom, Ayurvedic doctor, Caribbean elder |
| Work Surface | Table or counter within arm's reach. Holds ingredients during recipe portion | Wooden side table, kitchen counter, clinic tray, woven mat |
| Ingredients | Specific to the remedy being demonstrated. Varies per video | Baking soda, apple cider vinegar, lemons, mixing bowl, castor oil, honey, herbs |
| Patient (optional) | Second person in frame receiving the treatment. Only body parts visible, NOT face | Shirtless back (skin tags), extended foot (fungus), hand (nails), scalp (hair) |
| CTA Prop | Physical object held up to camera at the end | Book, product bottle, supplement jar, herb bundle |

**@ardenremedy example implementation**: Elderly Asian male (white hair, beard, glasses, traditional Chinese tunic, surgical mask on chin) on an outdoor night pergola with string lights, dried herbs hanging from rafters, fire pit, American flag. Holds up "Ancient Chinese Healing Wisdom" book for CTA. This is ONE possible execution of the format.

## Beat Structure

```
HOOK (3-8s):
  Avatar demonstrates the core action immediately — ice cube on foot, brushing nails, pointing at skin tags
  Text: Bold claim as caption ("Put an ice cube on the bottom of your foot")
  Purpose: Scroll-stop through unusual physical action. "What is this person doing?"

RECIPE PREP (8-15s):
  Avatar gathers/shows ingredients on table, mixes in bowl
  Text: Step-by-step instructions as captions
  Hands and ingredients are clearly visible in frame
  Purpose: Actionable, saveable content. "Here's how you make it"

APPLICATION (5-10s):
  Avatar applies the mixture to patient or self
  Text: Application instructions
  Purpose: Show the remedy being used. Visual proof it's practical

MECHANISM (8-15s):
  Avatar speaks directly to camera, explains WHY it works
  Text: Science/tradition explanation
  "This is ancient knowledge, not a new discovery"
  Purpose: Authority through tradition. Cultural credibility

CTA (8-15s):
  Avatar holds up book/product to camera
  Text: "Comment [keyword] and I will send it to you"
  Purpose: Conversion via comment keyword → ManyChat funnel
```

## Text Overlay Style

- Title Case On Every Word (not standard sentence case)
- White text with slight shadow, bottom-third positioning
- No yellow keyword highlights (unlike mixed-media)
- Clean, readable, one line at a time
- Captions describe what the avatar is saying, not what they're doing

## Camera

- Static, locked-off shot. No camera movement throughout the entire video
- Medium shot: avatar visible from waist up, with enough room to show the table and patient
- Slight low angle (camera at table height, looking slightly up at avatar)
- Night setting: warm string light illumination, fire pit glow as fill light
- 9:16 vertical, full-frame (no PiP, no split screen, no overlays)
- Depth of field: moderate, background (dried herbs, fence) slightly soft

## Pipeline Mapping

| Component | Agent | Notes |
|-----------|-------|-------|
| Avatar + setting image (start frame) | Image Prompter | Full-frame avatar at table with ingredients. Character reference for consistency |
| Patient body (if applicable) | Image Prompter | Second person in frame. Only body parts visible (back, foot), not face |
| Recipe step variations | Image Prompter (modification mode) or Veo motion | Hands mixing, applying paste. May need multiple reference images for different moments |
| Veo speaking scenes | Veo Prompter | Avatar speaking with hands in frame. Subtle gestures (pointing, holding ice, holding book). Keep hand movements SIMPLE |
| CTA frame (book hold) | Image Prompter | Avatar holding up physical book/product to camera |
| Text overlays | Post-production | Title Case captions synced to voiceover |

## Key Differences from Other Formats

**vs. Recipe Demo PiP**: Recipe Demo PiP has the speaker as a small overlay in the corner while recipe B-roll fills the background. Practitioner Demo has the speaker full-frame PERFORMING the recipe themselves. The avatar's hands, the table, and the ingredients are all in the same shot as the speaking avatar. No compositing, no PiP.

**vs. Talking Head**: Standard talking head has the speaker in a static pose, speaking to camera, with occasional B-roll cutaways. Practitioner Demo has the speaker physically doing things throughout — mixing, applying, demonstrating. The visual variety comes from the avatar's actions, not from cutaways.

**vs. Mixed-Media Animation**: Mixed-media cycles multiple rendered visual modes as backgrounds. Practitioner Demo stays in ONE continuous shot with ONE setting. No visual mode changes. The variety is in the physical action, not the background imagery.

## Storyboard Adjustments

When planning this video type:
- One continuous setting throughout. Plan a single detailed reference image with avatar + table + ingredients + setting
- Hands MUST be anchored to real objects (table surface, bowl, patient's skin, book). This prevents AI hand distortion
- Keep hand movements broad and simple in Veo prompts. "Holds up book" not "flips through pages while pointing"
- Patient (if present) is a BODY PART only — back, foot, hand. Never a full second face in frame. This avoids face consistency issues
- Props on the table are specific to each remedy. Specify exact props in the scene brief
- CTA prop (book, product bottle) appears ONLY at the end. Not visible on table during recipe portion
- No B-roll. No cutaways. No PiP. The format's strength is "one continuous scene, one authentic practitioner"
- Duration typically 35-80s. Shorter than mixed-media because there's less visual complexity to sustain attention
