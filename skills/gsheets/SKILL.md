---
name: gsheets
description: "Use when someone asks to read a Google Sheet, write to a spreadsheet, update sheet data, export to Google Sheets, import from a spreadsheet, format cells, search a sheet, or manage spreadsheet tabs. Also trigger when a Google Sheets URL or spreadsheet ID is mentioned."
disable-model-invocation: true
argument-hint: "[command] [options]"
---

# Google Sheets Skill

Read, write, and manage Google Sheets directly from Claude Code.

## When to Use This Skill

Trigger when user:
- Mentions Google Sheets, spreadsheet, or gsheets
- Wants to read/write/update a Google Sheet
- References a spreadsheet ID or Google Sheets URL
- Wants to export data to a sheet or import from one
- Asks to format, clear, or search within a spreadsheet

## Critical: Always Use run.py Wrapper

**NEVER call scripts directly. ALWAYS use `python scripts/run.py [script]`:**

All commands must be run from the skill directory. Set `SKILL_DIR` first:

```bash
SKILL_DIR="$HOME/.claude/skills/gsheets"
cd "$SKILL_DIR"
```

### Auth
```bash
python scripts/run.py auth.py status
python scripts/run.py auth.py set-key /path/to/key.json
```

### Read Data
```bash
# Default: formatted table
python scripts/run.py gsheets.py read --spreadsheet-id ID --range "Sheet1!A1:Z100"
# JSON output
python scripts/run.py gsheets.py read --spreadsheet-id ID --range "Sheet1!A1:Z100" --json
# CSV output
python scripts/run.py gsheets.py read --spreadsheet-id ID --range "Sheet1!A1:Z100" --csv
```

### Write Data
```bash
# From JSON array of arrays
python scripts/run.py gsheets.py write --spreadsheet-id ID --range "Sheet1!A1" --values '[["a","b"],["c","d"]]'
# From CSV file
python scripts/run.py gsheets.py write --spreadsheet-id ID --range "Sheet1!A1" --csv-file /path/to/data.csv
# With formula support
python scripts/run.py gsheets.py write --spreadsheet-id ID --range "Sheet1!A1" --values '[["=SUM(B2:B10)"]]' --value-input-option USER_ENTERED
```

### Append Rows
```bash
python scripts/run.py gsheets.py append --spreadsheet-id ID --sheet-name "Sheet1" --values '[["new","row"]]'
```

### Sheet Management
```bash
python scripts/run.py gsheets.py list-sheets --spreadsheet-id ID
python scripts/run.py gsheets.py create-sheet --spreadsheet-id ID --sheet-name "New Tab"
python scripts/run.py gsheets.py info --spreadsheet-id ID
```

### Clear Data
```bash
python scripts/run.py gsheets.py clear --spreadsheet-id ID --range "Sheet1!A1:Z100"
```

### Format Cells
```bash
python scripts/run.py gsheets.py format --spreadsheet-id ID --range "Sheet1!A1:Z1" --bold --bg-color "#333333" --text-color "#FFFFFF"
python scripts/run.py gsheets.py format --spreadsheet-id ID --range "Sheet1!A1:Z1" --italic --font-size 14 --h-align center
```

### Search
```bash
python scripts/run.py gsheets.py find --spreadsheet-id ID --sheet-name "Sheet1" --query "search term"
```

### Get URL
```bash
python scripts/run.py gsheets.py get-url --spreadsheet-id ID
```

## Known Spreadsheets

| Name | ID | Purpose |
|------|-----|---------|
| Salvora Prehooks | 13y_rw5s_7FlVhCHhKr0C9w7oPg9AWW9nPFRUG2YXJEU | Prehook image and video prompts |

## Core Workflow

### Step 1: Check Auth
```bash
cd "$HOME/.claude/skills/gsheets"
python scripts/run.py auth.py status
```
If auth is not configured, the status command shows the service account email. The user must share their spreadsheet with that email address.

### Step 2: Read Data
```bash
python scripts/run.py gsheets.py read --spreadsheet-id 13y_rw5s_7FlVhCHhKr0C9w7oPg9AWW9nPFRUG2YXJEU --range "Sheet1!A1:D10"
```
Default output is a formatted table. Add `--json` for raw JSON or `--csv` for CSV format.

### Step 3: Write Data
Values must be a JSON array of arrays (rows of cells):
```bash
python scripts/run.py gsheets.py write --spreadsheet-id ID --range "Sheet1!A1" --values '[["Name","Score"],["Alice","95"],["Bob","87"]]'
```

To upload from a CSV file:
```bash
python scripts/run.py gsheets.py write --spreadsheet-id ID --range "Sheet1!A1" --csv-file /path/to/data.csv
```

Use `--value-input-option USER_ENTERED` if values contain formulas (e.g. `=SUM(A1:A10)`).

### Step 4: Search
```bash
python scripts/run.py gsheets.py find --spreadsheet-id ID --sheet-name "Sheet1" --query "search term"
```
Returns cell references and values for all matches.

## Error Handling

| Error | What to Do |
|-------|-----------|
| `Permission denied` | Share the spreadsheet with the service account email shown in the error |
| `Spreadsheet not found` | Check the spreadsheet ID (between `/d/` and `/edit` in the URL) |
| `Unable to parse range` | Use `list-sheets` to check tab names. Format: `"SheetName!A1:Z100"` |
| `Auth not configured` | Run `python scripts/run.py auth.py status` and follow the setup instructions |

## Tips

- **Spreadsheet ID** is the long string in the Google Sheets URL between `/d/` and `/edit`
- **Range format**: `"SheetName!A1:Z100"` or just `"A1:Z100"` for the first sheet
- **Values** for write/append must be JSON array of arrays
- The **service account email** must be shared (as Editor) on any spreadsheet you want to access
- Use `list-sheets` to see all tab names before reading/writing
- Use `info` for a quick overview of the spreadsheet structure
- For formulas, use `--value-input-option USER_ENTERED`
- The skill auto-creates its virtual environment on first run

## Security

- Service account key is stored locally in `data/config.json` (path reference only, not the key itself)
- Key file and data directory are excluded from git via `.gitignore`
- The service account has access ONLY to spreadsheets explicitly shared with it
- No data is sent to any endpoint other than `googleapis.com`
