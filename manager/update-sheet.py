import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    'C:/Users/Privat/Downloads/crypto-quasar-489706-a8-9530762b9b2d.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
service = build('sheets', 'v4', credentials=creds)
SPREADSHEET_ID = '13y_rw5s_7FlVhCHhKr0C9w7oPg9AWW9nPFRUG2YXJEU'
SHEET = 'Salvora Prehooks - Week 1_prompts (5)'

# Get all rows to find row numbers by Node ID
result = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range=f'{SHEET}!A1:A50'
).execute()
rows = result.get('values', [])
id_to_row = {}
for i, row in enumerate(rows):
    if row:
        id_to_row[row[0]] = i + 1

# === P1 BEFORE IMAGE (Node 1) ===
p1_before = json.dumps({
    "subject": {
        "description": "A woman lying in bed at 3AM, holding her phone above her face with one hand, filming a front camera selfie. She just woke up and grabbed her phone. NOT posing, NOT acting.",
        "age": "late 50s",
        "expression": "naturally tired, slightly squinting from the phone screen light, mouth relaxed"
    },
    "face": {
        "preserve_original": True,
        "makeup": "bare face, no makeup"
    },
    "hair": {
        "style": "covered by a silk bonnet, a few edges of dark brown hair peeking out at the front"
    },
    "clothing": {
        "top": {
            "type": "oversized faded sleep shirt",
            "color": "washed out grey",
            "details": "soft cotton, stretched neckline, wrinkled from sleeping in it"
        }
    },
    "accessories": {
        "headwear": {
            "type": "silk bonnet",
            "color": "muted dusty rose",
            "details": "slightly shifted from tossing in sleep"
        }
    },
    "character_reference": {
        "instruction": "Use the attached reference sheet as the absolute ground truth for the subject's facial features, skin texture, and body proportions. The output must be a 1:1 match of the character provided."
    },
    "photography": {
        "camera_style": "front camera smartphone selfie, arm extended above face, slightly soft and warm",
        "angle": "directly above, looking up into the phone camera",
        "shot_type": "close up of face and shoulders, phone held in one hand above",
        "aspect_ratio": "9:16 vertical",
        "texture": "social media realism, front camera softness, warm tones from the lamp, NOT cinematic, NOT raw photorealism, NOT professional"
    },
    "background": {
        "setting": "dark bedroom at night, nightstand lamp on",
        "elements": [
            "rumpled pillow and sheets around her",
            "nightstand with a small warm lamp turned on",
            "half empty water glass on nightstand",
            "phone charger cable trailing off the nightstand",
            "digital clock barely visible"
        ],
        "atmosphere": "mundane, middle of the night, quiet, ordinary",
        "lighting": "small nightstand lamp casting warm flat light across her face, enough to see her clearly but nothing dramatic. The rest of the room falls into soft darkness. NOT directional, NOT creating shadows across the face"
    },
    "--no": "professional lighting, studio, cinematic, dramatic shadows, moody, film grain, raw photorealism, dark atmosphere, beauty lighting, rim light, backlight, overhead angle, bird's eye view"
}, separators=(',', ':'))

# === P2 BROLL BEFORE IMAGE (Node 208) - Baby monitor ===
p2_broll_before = json.dumps({
    "character_reference": {
        "instruction": "Use the attached reference sheet as the absolute ground truth for the subject's facial features, skin texture, and body proportions. The output must be a 1:1 match of the character provided."
    },
    "subject": {
        "description": "A woman lying face down on an unmade bed, one arm hanging limp off the mattress edge, barely moved since falling asleep. Captured from a high shelf or dresser corner looking down at the bed, like a baby monitor or room camera. She is not aware of the camera.",
        "age": "early 50s",
        "expression": "face buried in pillow, eyes shut, completely still"
    },
    "face": {
        "preserve_original": True,
        "makeup": "no makeup, bare skin, dark circles"
    },
    "hair": {
        "color": "dark, greying at the temples",
        "style": "messy and tangled from sleep, splayed across pillow"
    },
    "clothing": {
        "top": {
            "type": "wrinkled cotton nightgown",
            "color": "faded pale blue",
            "details": "plain fabric, twisted around her torso from tossing in sleep, one strap slipping off shoulder"
        }
    },
    "photography": {
        "camera_style": "baby monitor or room security camera mounted high on a shelf, looking down at the bed. Wide angle with slight barrel distortion at edges",
        "angle": "high angle from dresser corner, looking down diagonally across the bed",
        "shot_type": "wide shot, full bed visible, subject small in the frame",
        "aspect_ratio": "9:16 vertical",
        "texture": "digital surveillance quality, grainy, low resolution feel, slightly desaturated, NOT cinematic, NOT professional. Like a cheap IP camera feed"
    },
    "background": {
        "setting": "real lived in bedroom, early grey morning",
        "elements": [
            "rumpled sheets and blanket half kicked off the bed",
            "nightstand with digital alarm clock showing 6:47 AM",
            "half empty water glass on nightstand",
            "phone charger cable draped off nightstand edge",
            "curtains with pale grey morning light barely filtering through"
        ],
        "atmosphere": "still, quiet, depressing. She has not moved. The alarm already went off.",
        "lighting": "dim early morning daylight through curtains, grey and flat, no warmth"
    }
}, separators=(',', ':'))

# === P3 BROLL BEFORE IMAGE (Node 408) ===
p3_broll_before = json.dumps({
    "character_reference": {
        "instruction": "Use the attached reference sheet as the absolute ground truth for the subject's facial features, skin texture, and body proportions. The output must be a 1:1 match of the character provided."
    },
    "subject": {
        "description": "{character} in her kitchen, leaning hard on the counter with her left arm locked straight, right hand pressing into her lower back. Head dropped, staring down at the half prepped food she gave up on. All her weight is on the counter. She stopped mid cook and doesn't have the energy to finish.",
        "expression": "drained, eyes down, mouth slack, not dramatic, just done"
    },
    "face": {
        "preserve_original": True,
        "makeup": "none, bare face"
    },
    "hair": {
        "style": "loose low bun, messy, strands falling around her face and neck"
    },
    "clothing": {
        "top": {
            "type": "plain apron over a soft t-shirt",
            "color": "apron is off white with stains, shirt underneath is faded grey",
            "details": "apron ties loose, wrinkled, been cooking in it"
        },
        "bottom": {
            "type": "lounge pants",
            "color": "dark grey",
            "details": "elastic waist, lived in look"
        }
    },
    "photography": {
        "camera_style": "smartphone handheld, someone else filming her from across the kitchen",
        "angle": "eye level, slightly off center, about 6 feet away",
        "shot_type": "waist up, kitchen counter and stove visible behind her",
        "aspect_ratio": "9:16 vertical",
        "texture": "social media realism, sharp but not professional, natural indoor light, NOT cinematic, NOT raw photorealism"
    },
    "background": {
        "setting": "real home kitchen, overhead ceiling light on",
        "elements": [
            "cutting board with half chopped vegetables and a knife set down mid cut",
            "pot on stove with lid sitting crooked",
            "crumpled dish towel on the counter",
            "a few unwashed dishes near the sink"
        ],
        "atmosphere": "abandoned dinner prep, she ran out of gas halfway through",
        "lighting": "overhead kitchen ceiling light, neutral white, slightly harsh from above, not moody, not warm"
    },
    "--ar": "9:16",
    "--no": "professional lighting, cinematic, studio, bokeh, clean kitchen, makeup, beauty filter, dramatic lighting, moody atmosphere, polished look, golden hour"
}, separators=(',', ':'))

# === P4 AFTER VIDEO (Node 610) ===
p4_after_video = (
    'They say: "{dialogue}"\n\n'
    'They speak with calm, steady confidence. Not loud, not excited, just quietly sure of themselves. '
    'A small smile breaks through as they talk. Their voice is warm and grounded. They pause naturally, '
    'letting the words settle. Their pace is unhurried. There is a quiet strength in their delivery, '
    'like someone who has turned a corner and knows it.\n\n'
    "Selfie angle, doctor's office exam room. She sits on the edge of the exam chair, upright and composed. "
    'Light makeup, hair pulled back in a low clip, olive green crewneck, dark navy trousers. Clean and put together. '
    'Her expression is open and calm. Eyes steady, present. A small smile that builds gradually. One hand holds the phone, '
    'the other rests on her knee. She adjusts her sleeve once, a small confident movement. Her posture is easy and grounded. '
    'She showed up for herself and she knows it.\n\n'
    'NOT cartoonish eyes, bug eyes, exaggerated expressions, stiff robotic posture, frozen mannequin, '
    'hands hidden or frozen in lap, dead eyes, overly dramatic gestures, aggressive pointing, background music, '
    'sound effects, subtitles, text overlays, professional studio lighting, ring light, beauty filter, 3d render.'
)

# Build updates
updates = [
    (id_to_row['1'], p1_before, 'P1 before image'),
    (id_to_row['208'], p2_broll_before, 'P2 broll before image'),
    (id_to_row['408'], p3_broll_before, 'P3 broll before image'),
    (id_to_row['610'], p4_after_video, 'P4 after video'),
]

for row_num, content, label in updates:
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f'{SHEET}!D{row_num}',
        valueInputOption='RAW',
        body={'values': [[content]]}
    ).execute()
    print(f'Updated row {row_num}: {label}')

print('\nAll 4 prompts updated.')
