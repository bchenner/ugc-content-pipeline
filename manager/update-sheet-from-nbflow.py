import json
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

def retry_api(fn, max_retries=5, delay=5):
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  API error (attempt {attempt+1}/{max_retries}): {e}")
                time.sleep(delay * (attempt + 1))
            else:
                raise

# Load the generated .nbflow
with open('c:/Users/Privat/Documents/Claude Code/claude-projects/patchwork-importer/output/salvora-prehooks-week1.nbflow') as f:
    project = json.load(f)

# Extract Testing tab prompt nodes
testing_tab = project["tabs"][0]
nodes = testing_tab["graphData"]["nodes"]
prompt_nodes = [n for n in nodes if n["type"] == "nanobanana/Prompt"]
print(f"Found {len(prompt_nodes)} prompt nodes in Testing tab")

# Build update map
updates = {}
for n in prompt_nodes:
    node_id = str(n["id"])
    updates[node_id] = {"content": n["properties"]["text"], "title": n["title"]}

# Connect to Google Sheets
creds = service_account.Credentials.from_service_account_file(
    'C:/Users/Privat/Downloads/crypto-quasar-489706-a8-9530762b9b2d.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
service = build('sheets', 'v4', credentials=creds)
SPREADSHEET_ID = '13y_rw5s_7FlVhCHhKr0C9w7oPg9AWW9nPFRUG2YXJEU'
SHEET = 'Salvora Prehooks - Week 1_prompts (5)'

# Get row mapping with retry
print("Reading sheet row mapping...")
result = retry_api(lambda: service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range=f'{SHEET}!A1:A50'
).execute())
rows = result.get('values', [])
id_to_row = {}
for i, row in enumerate(rows):
    if row:
        id_to_row[row[0]] = i + 1
print(f"Found {len(id_to_row)} rows")

# Build batch update data
batch_data = []
for node_id, info in updates.items():
    if node_id in id_to_row:
        row_num = id_to_row[node_id]
        batch_data.append({
            'range': f'{SHEET}!D{row_num}',
            'values': [[info['content']]]
        })
        print(f"  Queued: Node {node_id} ({info['title']}) -> row {row_num}")

# Single batch update with retry
print(f"\nSending batch update for {len(batch_data)} cells...")
retry_api(lambda: service.spreadsheets().values().batchUpdate(
    spreadsheetId=SPREADSHEET_ID,
    body={'valueInputOption': 'RAW', 'data': batch_data}
).execute())
print(f"Done. Updated {len(batch_data)} prompts.")
