# Visceral Render Prehook

Giant 3D medical render or photorealistic AI imagery fills the screen as the first thing viewers see. Designed to be visually shocking or fascinating — diseased organs, anatomical cross-sections, cellular processes, extreme skin conditions.

## What's On Screen

- Full-screen 3D medical render: diseased lungs, giant teeth with plaque, ear canal with wax, inflamed intestines
- Or photorealistic AI: extreme close-up of skin condition, foam on cracked heels, infected nails
- Speaker may appear as tiny PiP in corner (common) or fully absent
- Scale is exaggerated — teeth are building-sized, organs fill the entire frame

## Examples Observed

- amazon_yellow_teeth (0:00-0:04): Giant 3D teeth with yellow plaque, one tooth clean, speaker PiP
- hook_fb5 (0:00-0:05): Massive diseased/blackened lungs with smoke, speaker PiP in yellow outfit
- burner_b006 (0:00-0:05): 3D ear canal macro with foam/syringe, speaker PiP in kente cloth
- hook_fb2 (0:00-0:04): 3D skeleton sitting on toilet, speaker PiP in scrubs

## Visual Details

- 3D renders use clinical lighting, dark or blue gradient backgrounds
- Scale is intentionally wrong — organs are gigantic relative to the (tiny) speaker PiP
- Lighting: dramatic, volumetric, cinematic. NOT flat clinical stock imagery
- Colors: often muted/gross for diseased state (browns, yellows, blacks) or vivid clinical (blue background, white bone)
- Duration: 3-8s. The render IS the hook
- Often the same visual mode continues into the main body (if the video is mixed-media throughout)

## Pipeline

- Image Prompter: "3D medical render" style prompt. Dark background, dramatic lighting, anatomical detail
- Can also use photorealistic extreme close-ups for skin/body conditions
- No Veo needed (static render with text overlay)
- Speaker PiP composited in post-production if needed
- Be careful with platform content policies — gross medical imagery may get flagged. Stylized 3D renders are safer than photorealistic gore
