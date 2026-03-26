# Prehook Types

Prehooks are the first 2-15 seconds of a video, before the main speaking content begins. Their only job is to stop the scroll and create enough curiosity to keep watching. They are visually distinct from the main body and often use a completely different visual format.

Prehooks are edited together in post-production. They are NOT part of the main Veo speaking video. They are separate clips (images or short video loops) with text overlay and/or voiceover added in editing.

## Prehook Types

| Type | File | Duration | What's On Screen |
|------|------|----------|-----------------|
| Transformation Before/After | [transformation.md](transformation.md) | 3-8s | Side-by-side or sequential before→after body shots |
| Body Close-Up | [body-closeup.md](body-closeup.md) | 2-5s | Macro close-up of symptom (cracked heels, yellow teeth, thinning hair, belly fat) |
| Reaction PiP | [reaction-pip.md](reaction-pip.md) | 3-8s | Speaker PiP reacting to external footage (medical exam, other creator's clip) |
| Visceral Render | [visceral-render.md](visceral-render.md) | 3-8s | Giant 3D organ render, diseased tissue, medical imagery with speaker PiP |
| Mirror Selfie | [mirror-selfie.md](mirror-selfie.md) | 2-5s | Real or AI-generated mirror selfie showing body condition |

## How Prehooks Connect to Main Body

The prehook ends with a **hard cut** to the main video format. There is no transition or fade. The visual register shift (gross close-up → speaking head, or 3D render → talking avatar) IS the structural hook that signals "now I'm going to explain this."

## Pipeline Notes

- Prehook clips are generated separately from main body scenes
- Each prehook needs its own reference image (Image Prompter) and optionally a short video prompt (Veo/Seedance for motion, or static image with text overlay)
- Prehooks are NOT in the PatchWork file — they are assembled in post-production
- A single video may use 1-3 prehook clips edited together before the hard cut
- Text overlays on prehooks are added in post-production
