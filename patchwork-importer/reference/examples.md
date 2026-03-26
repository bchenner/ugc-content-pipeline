# Construction Examples

## Full Pipeline: 2 Image Groups (5 Scenes) + 3 B-Roll Clips

### Mainbody Tab

**Image Gen Group 1** (used by scenes 1, 2, 5 — requires avatar + product):

```
Nodes:
  id:1  Prompt         [-2000, -324]  text = image prompt JSON      order:0
  id:5  ReferenceImage [-2118, -81]   imageData = avatar URL        order:1
  id:33 ReferenceImage [-1748, 105]   imageData = product URL       order:2
  id:2  NanobananaAPI  [-1228, -110]  imageCount = 2                order:3
  id:28 Approval       [-812, -71]                                  order:4

Links:
  [1, 1, 0, 2, 0, "string"]    — Prompt → API prompt
  [10, 5, 0, 2, 1, "image"]    — Avatar ref → API image 1
  [49, 33, 0, 2, 2, "image"]   — Product ref → API image 2
  [39, 2, 0, 28, 0, "*"]       — API → Approval
```

**Image Gen Group 2** (used by scenes 3, 4):

```
Same pattern, different Y positions (~600px below group 1)
```

**Scene Videos** (one per scene — each Veo3 feeds into a video Approval):

```
Scene 1:
  id:13 Prompt    [-164, -114]  text = scene 1 video prompt JSON    order:5
  id:11 Veo3      [242, -98]    durationSeconds = "8"                order:6
  id:34 Approval  [700, -98]    (video review)                       order:7

Links:
  [14, 13, 0, 11, 0, "string"]   — Prompt → Veo3 prompt
  [40, 28, 0, 11, 1, "image"]    — Approval (group 1) → Veo3 start frame
  [50, 11, 0, 34, 0, "*"]        — Veo3 → video Approval

Scene 2:
  id:32 Prompt    [-213, 432]   text = scene 2 video prompt JSON    order:8
  id:20 Veo3      [690, 375]    durationSeconds = "8"                order:9
  id:35 Approval  [1148, 375]   (video review)                       order:10

Links:
  [48, 32, 0, 20, 0, "string"]
  [41, 28, 0, 20, 1, "image"]    — Same Approval (group 1) fans out
  [51, 20, 0, 35, 0, "*"]        — Veo3 → video Approval
```

**Approval fan-out**: Image Approval node id:28 output links = `[40, 41, ...]` — one per scene/hook that references this image group.

### BRoll Tab

**B-roll 1** (with start + end frames):

```
Start frame:
  id:9  ReferenceImage [-822, 527]   imageData = product URL        order:0
  id:4  Prompt         [-958, 191]   text = start frame prompt       order:1
  id:1  NanobananaAPI  [-340, 180]   imageCount = 1                  order:2
  id:7  Approval       [144, -94]                                    order:3

Links:
  [2, 4, 0, 1, 0, "string"]     — Prompt → API prompt
  [10, 9, 0, 1, 1, "image"]     — Product ref → API image 1
  [5, 1, 0, 7, 0, "*"]          — API → Approval (start)

End frame:
  id:5  Prompt         [-890, 947]   text = end frame prompt         order:4
  id:2  NanobananaAPI  [359, 588]    imageCount = 3                  order:5
  id:6  Approval       [936, 592]                                    order:6

Links:
  [1, 5, 0, 2, 0, "string"]     — Prompt → API prompt
  [11, 9, 0, 2, 1, "image"]     — Product ref → API image 1 (same ReferenceImage, 2nd link)
  [35, 7, 0, 2, 2, "image"]     — Start Approval output → API image 2 (consistency ref)
  [6, 2, 0, 6, 0, "*"]          — API → Approval (end)

Video:
  id:8  Prompt    [972, 102]    text = video prompt                   order:7
  id:3  Veo3      [1444, 449]   durationSeconds = "8"                 order:8
  id:10 Approval  [1900, 449]   (video review)                        order:9

Links:
  [9, 8, 0, 3, 0, "string"]     — Prompt → Veo3 prompt
  [8, 7, 0, 3, 1, "image"]      — Start Approval → Veo3 start frame
  [7, 6, 0, 3, 2, "image"]      — End Approval → Veo3 end frame
  [12, 3, 0, 10, 0, "*"]        — Veo3 → video Approval
```

**Start Approval fan-out**: Approval id:7 output links = `[8, 35]` — start frame to Veo3 AND reference to end frame NanobananaAPI.

**Subsequent B-roll clips** follow the same pattern at offset Y + 1200px per clip.
