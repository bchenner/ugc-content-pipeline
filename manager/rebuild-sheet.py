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

# Extract Testing tab prompt nodes (exclude dynamic character nodes)
testing_tab = project["tabs"][0]
nodes = testing_tab["graphData"]["nodes"]
prompt_nodes = [n for n in nodes if n["type"] == "nanobanana/Prompt" and not n["properties"].get("dynamicMode", False)]
prompt_nodes.sort(key=lambda n: n["id"])
print(f"Found {len(prompt_nodes)} prompt nodes (excluding dynamic nodes)")

# Connect to Google Sheets
creds = service_account.Credentials.from_service_account_file(
    'C:/Users/Privat/Downloads/crypto-quasar-489706-a8-9530762b9b2d.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
service = build('sheets', 'v4', credentials=creds)
SPREADSHEET_ID = '13y_rw5s_7FlVhCHhKr0C9w7oPg9AWW9nPFRUG2YXJEU'
SHEET = 'Salvora Prehooks - Week 1_prompts (5)'

# Clear existing data (keep header row 1)
print("Clearing existing rows...")
retry_api(lambda: service.spreadsheets().values().clear(
    spreadsheetId=SPREADSHEET_ID,
    range=f'{SHEET}!A2:D100'
).execute())

# Build new rows: Node ID, Node Title, Mode, Content
rows = []
for n in prompt_nodes:
    node_id = str(n["id"])
    title = n["title"]
    mode = "template" if n["properties"].get("templateMode") else "static"
    content = n["properties"]["text"]
    rows.append([node_id, title, mode, content])
    print(f"  {node_id}: {title} ({mode})")

# Write all rows
print(f"\nWriting {len(rows)} rows...")
retry_api(lambda: service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=f'{SHEET}!A2',
    valueInputOption='RAW',
    body={'values': rows}
).execute())

print(f"Done. Rebuilt sheet with {len(rows)} prompt nodes.")
