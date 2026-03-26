# Reaction PiP Prehook

Speaker appears as a PiP overlay reacting to external footage. The external footage (medical exam, other creator's video, treatment clip) provides the scroll-stop. The speaker's reaction provides the "I'm going to explain this" promise.

## What's On Screen

- Background: external footage (doctor examining patient, before/after transformation, treatment video)
- Speaker: PiP in bottom corner, reacting with surprise, concern, or commentary
- Speaker may be in a different setting than the main video (this is the prehook, not the body)

## Examples Observed

- burner_004: Woman in surgical cap as small PiP reacting to medical examination footage (doctor + patient). Then hard-cuts to same woman in car for the main body
- @sheisapaigeturner style: Speaker reacting to their own or others' before/after footage

## Visual Details

- Background footage is the attention-getter. Speaker PiP is the anchor
- Speaker PiP: ~20-25% of frame, bottom-left or bottom-right
- Speaker shows visible emotional reaction (wide eyes, mouth open, nodding)
- Text overlay: hook line ("This is how women over 40 can bounce back their PRIME")
- Duration: 3-8s
- Hard cut to main body format after the reaction clip

## Pipeline

- Background footage: external (filmed or someone else's clip) or AI-generated
- Speaker PiP: Image Prompter (reaction expression) or Veo short clip (2-3s reaction)
- Compositing: post-production overlay
- The reaction PiP speaker may be the SAME avatar as the main body speaker, or a different person entirely
