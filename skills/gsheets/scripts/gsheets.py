#!/usr/bin/env python3
"""
Google Sheets CLI tool.
Subcommands: read, write, append, list-sheets, create-sheet, clear, format, info, find, get-url
"""

import argparse
import csv
import io
import json
import sys
from pathlib import Path

# Add scripts dir so we can import auth
sys.path.insert(0, str(Path(__file__).parent))
from auth import find_key_path, get_service_account_email


def get_service():
    """Build and return an authorized Sheets API service."""
    key_path = find_key_path()
    if not key_path:
        print("No service account key configured.")
        print("Run: python scripts/run.py auth.py set-key <path-to-key.json>")
        sys.exit(1)

    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    try:
        creds = service_account.Credentials.from_service_account_file(
            key_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        service = build('sheets', 'v4', credentials=creds)
        return service
    except Exception as e:
        email = get_service_account_email(key_path)
        print(f"Auth failed: {e}")
        print(f"\nMake sure the spreadsheet is shared with: {email}")
        sys.exit(1)


def handle_api_error(e, spreadsheet_id):
    """Handle common API errors with helpful messages."""
    from googleapiclient.errors import HttpError
    if isinstance(e, HttpError):
        status = e.resp.status
        if status == 404:
            print(f"Spreadsheet not found: {spreadsheet_id}")
            print("Check the spreadsheet ID (the long string between /d/ and /edit in the URL).")
        elif status == 403:
            key_path = find_key_path()
            email = get_service_account_email(key_path) if key_path else "unknown"
            print(f"Permission denied for spreadsheet: {spreadsheet_id}")
            print(f"\nShare the spreadsheet with this service account email:")
            print(f"  {email}")
        elif status == 400:
            detail = str(e)
            print(f"Invalid request: {detail}")
            if "Unable to parse range" in detail:
                print("\nRange format: 'SheetName!A1:Z100' or just 'A1:Z100' for the first sheet.")
                print("Use list-sheets to see available sheet names.")
        else:
            print(f"API error ({status}): {e}")
    else:
        print(f"Error: {e}")
    sys.exit(1)


def format_table(values):
    """Format values as an aligned text table."""
    if not values:
        print("(empty)")
        return

    # Calculate column widths
    col_count = max(len(row) for row in values)
    # Pad rows to same length
    padded = [row + [''] * (col_count - len(row)) for row in values]

    widths = []
    for col in range(col_count):
        w = max(len(str(padded[row][col])) for row in range(len(padded)))
        widths.append(min(w, 60))  # cap at 60 chars per column

    # Print header
    header = padded[0]
    header_line = " | ".join(str(header[i]).ljust(widths[i])[:widths[i]] for i in range(col_count))
    print(header_line)
    print("-+-".join("-" * widths[i] for i in range(col_count)))

    # Print data rows
    for row in padded[1:]:
        line = " | ".join(str(row[i]).ljust(widths[i])[:widths[i]] for i in range(col_count))
        print(line)


def format_csv_output(values):
    """Format values as CSV."""
    if not values:
        return
    output = io.StringIO()
    writer = csv.writer(output)
    for row in values:
        writer.writerow(row)
    print(output.getvalue(), end='')


# === SUBCOMMANDS ===

def cmd_read(args):
    """Read a sheet range."""
    service = get_service()
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=args.spreadsheet_id,
            range=args.range
        ).execute()
    except Exception as e:
        handle_api_error(e, args.spreadsheet_id)

    values = result.get('values', [])
    row_count = len(values)
    col_count = max(len(r) for r in values) if values else 0

    if args.json:
        print(json.dumps(values, indent=2, ensure_ascii=False))
    elif args.csv:
        format_csv_output(values)
    else:
        format_table(values)

    print(f"\n{row_count} rows x {col_count} columns")


def cmd_write(args):
    """Write to a range."""
    service = get_service()

    if args.csv_file:
        csv_path = Path(args.csv_file)
        if not csv_path.exists():
            print(f"CSV file not found: {args.csv_file}")
            sys.exit(1)
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            values = [row for row in reader]
    elif args.values:
        try:
            values = json.loads(args.values)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON for --values: {e}")
            print('Expected format: \'[["row1col1","row1col2"],["row2col1","row2col2"]]\'')
            sys.exit(1)
    else:
        print("Provide either --values or --csv-file")
        sys.exit(1)

    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=args.spreadsheet_id,
            range=args.range,
            valueInputOption=args.value_input_option,
            body={'values': values}
        ).execute()
    except Exception as e:
        handle_api_error(e, args.spreadsheet_id)

    updated = result.get('updatedCells', 0)
    print(f"Updated {updated} cells in {result.get('updatedRange', args.range)}")


def cmd_append(args):
    """Append rows to end of sheet."""
    service = get_service()

    try:
        values = json.loads(args.values)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON for --values: {e}")
        print('Expected format: \'[["col1","col2"],["col1","col2"]]\'')
        sys.exit(1)

    range_str = f"{args.sheet_name}!A1" if args.sheet_name else "A1"

    try:
        result = service.spreadsheets().values().append(
            spreadsheetId=args.spreadsheet_id,
            range=range_str,
            valueInputOption=args.value_input_option,
            insertDataOption='INSERT_ROWS',
            body={'values': values}
        ).execute()
    except Exception as e:
        handle_api_error(e, args.spreadsheet_id)

    updates = result.get('updates', {})
    print(f"Appended {updates.get('updatedRows', 0)} rows to {updates.get('updatedRange', range_str)}")


def cmd_list_sheets(args):
    """List all tabs in a spreadsheet."""
    service = get_service()

    try:
        result = service.spreadsheets().get(
            spreadsheetId=args.spreadsheet_id,
            fields='sheets.properties'
        ).execute()
    except Exception as e:
        handle_api_error(e, args.spreadsheet_id)

    sheets = result.get('sheets', [])
    print(f"Found {len(sheets)} sheet(s):\n")
    for s in sheets:
        props = s['properties']
        title = props['title']
        sheet_id = props['sheetId']
        rows = props.get('gridProperties', {}).get('rowCount', '?')
        cols = props.get('gridProperties', {}).get('columnCount', '?')
        print(f"  {title} (id: {sheet_id}, {rows} rows x {cols} cols)")


def cmd_create_sheet(args):
    """Create a new tab."""
    service = get_service()

    body = {
        'requests': [{
            'addSheet': {
                'properties': {
                    'title': args.sheet_name
                }
            }
        }]
    }

    try:
        result = service.spreadsheets().batchUpdate(
            spreadsheetId=args.spreadsheet_id,
            body=body
        ).execute()
    except Exception as e:
        handle_api_error(e, args.spreadsheet_id)

    new_sheet = result['replies'][0]['addSheet']['properties']
    print(f"Created sheet: {new_sheet['title']} (id: {new_sheet['sheetId']})")


def cmd_clear(args):
    """Clear a range."""
    service = get_service()

    try:
        service.spreadsheets().values().clear(
            spreadsheetId=args.spreadsheet_id,
            range=args.range,
            body={}
        ).execute()
    except Exception as e:
        handle_api_error(e, args.spreadsheet_id)

    print(f"Cleared range: {args.range}")


def cmd_format(args):
    """Apply basic formatting to a range."""
    service = get_service()

    # Parse the range to get sheet name and cell range
    if '!' in args.range:
        sheet_name, cell_range = args.range.split('!', 1)
    else:
        sheet_name = None
        cell_range = args.range

    # Get the sheet ID
    try:
        meta = service.spreadsheets().get(
            spreadsheetId=args.spreadsheet_id,
            fields='sheets.properties'
        ).execute()
    except Exception as e:
        handle_api_error(e, args.spreadsheet_id)

    sheet_id = 0
    if sheet_name:
        for s in meta.get('sheets', []):
            if s['properties']['title'] == sheet_name:
                sheet_id = s['properties']['sheetId']
                break

    # Parse cell range (e.g. A1:Z1) into grid range
    grid_range = parse_a1_to_grid(cell_range, sheet_id)

    # Build format request
    cell_format = {}
    if args.bold:
        cell_format.setdefault('textFormat', {})['bold'] = True
    if args.italic:
        cell_format.setdefault('textFormat', {})['italic'] = True
    if args.font_size:
        cell_format.setdefault('textFormat', {})['fontSize'] = args.font_size
    if args.bg_color:
        cell_format['backgroundColor'] = hex_to_color(args.bg_color)
    if args.text_color:
        cell_format.setdefault('textFormat', {})['foregroundColor'] = hex_to_color(args.text_color)
    if args.h_align:
        cell_format['horizontalAlignment'] = args.h_align.upper()

    if not cell_format:
        print("No formatting options specified. Use --bold, --bg-color, --text-color, etc.")
        sys.exit(1)

    fields = []
    if 'textFormat' in cell_format:
        fields.append('userEnteredFormat.textFormat')
    if 'backgroundColor' in cell_format:
        fields.append('userEnteredFormat.backgroundColor')
    if 'horizontalAlignment' in cell_format:
        fields.append('userEnteredFormat.horizontalAlignment')

    request = {
        'requests': [{
            'repeatCell': {
                'range': grid_range,
                'cell': {
                    'userEnteredFormat': cell_format
                },
                'fields': ','.join(fields)
            }
        }]
    }

    try:
        service.spreadsheets().batchUpdate(
            spreadsheetId=args.spreadsheet_id,
            body=request
        ).execute()
    except Exception as e:
        handle_api_error(e, args.spreadsheet_id)

    print(f"Formatted range: {args.range}")


def cmd_info(args):
    """Show spreadsheet metadata."""
    service = get_service()

    try:
        result = service.spreadsheets().get(
            spreadsheetId=args.spreadsheet_id
        ).execute()
    except Exception as e:
        handle_api_error(e, args.spreadsheet_id)

    props = result.get('properties', {})
    sheets = result.get('sheets', [])

    print(f"Title: {props.get('title', 'Unknown')}")
    print(f"Locale: {props.get('locale', 'Unknown')}")
    print(f"URL: https://docs.google.com/spreadsheets/d/{args.spreadsheet_id}/edit")
    print(f"Sheets: {len(sheets)}")
    print()

    for s in sheets:
        sp = s['properties']
        gp = sp.get('gridProperties', {})
        print(f"  {sp['title']}")
        print(f"    ID: {sp['sheetId']}, Rows: {gp.get('rowCount', '?')}, Cols: {gp.get('columnCount', '?')}")


def cmd_find(args):
    """Search for a value in a sheet."""
    service = get_service()

    range_str = f"{args.sheet_name}!A1:ZZ10000" if args.sheet_name else "A1:ZZ10000"

    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=args.spreadsheet_id,
            range=range_str
        ).execute()
    except Exception as e:
        handle_api_error(e, args.spreadsheet_id)

    values = result.get('values', [])
    query = args.query.lower()
    matches = []

    for row_idx, row in enumerate(values):
        for col_idx, cell in enumerate(row):
            if query in str(cell).lower():
                col_letter = col_num_to_letter(col_idx)
                row_num = row_idx + 1
                cell_ref = f"{col_letter}{row_num}"
                matches.append((cell_ref, str(cell)))

    if matches:
        print(f"Found {len(matches)} match(es) for '{args.query}':\n")
        for ref, val in matches:
            # Truncate long values
            display = val[:100] + "..." if len(val) > 100 else val
            print(f"  {ref}: {display}")
    else:
        print(f"No matches found for '{args.query}'")


def cmd_get_url(args):
    """Return the Google Sheets URL for a spreadsheet ID."""
    print(f"https://docs.google.com/spreadsheets/d/{args.spreadsheet_id}/edit")


# === HELPERS ===

def hex_to_color(hex_str):
    """Convert hex color (#RRGGBB) to Google Sheets color dict."""
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6:
        print(f"Invalid hex color: #{hex_str}. Use format #RRGGBB.")
        sys.exit(1)
    r = int(hex_str[0:2], 16) / 255.0
    g = int(hex_str[2:4], 16) / 255.0
    b = int(hex_str[4:6], 16) / 255.0
    return {'red': r, 'green': g, 'blue': b}


def col_num_to_letter(col_num):
    """Convert 0-based column number to letter(s). 0=A, 25=Z, 26=AA."""
    result = ''
    col_num += 1  # 1-based
    while col_num > 0:
        col_num, remainder = divmod(col_num - 1, 26)
        result = chr(65 + remainder) + result
    return result


def col_letter_to_num(col_str):
    """Convert column letter(s) to 0-based number. A=0, Z=25, AA=26."""
    result = 0
    for char in col_str.upper():
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result - 1


def parse_a1_to_grid(cell_range, sheet_id=0):
    """Parse A1 notation (e.g. 'A1:Z10') to a GridRange dict."""
    import re

    parts = cell_range.split(':')
    start = parts[0]
    end = parts[1] if len(parts) > 1 else start

    match_start = re.match(r'^([A-Za-z]+)(\d+)$', start)
    match_end = re.match(r'^([A-Za-z]+)(\d+)$', end)

    if not match_start or not match_end:
        print(f"Cannot parse range: {cell_range}")
        sys.exit(1)

    return {
        'sheetId': sheet_id,
        'startRowIndex': int(match_start.group(2)) - 1,
        'endRowIndex': int(match_end.group(2)),
        'startColumnIndex': col_letter_to_num(match_start.group(1)),
        'endColumnIndex': col_letter_to_num(match_end.group(1)) + 1
    }


def main():
    parser = argparse.ArgumentParser(
        description="Google Sheets CLI tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command")

    # --- read ---
    p_read = subparsers.add_parser("read", help="Read a sheet range")
    p_read.add_argument("--spreadsheet-id", required=True, help="Spreadsheet ID")
    p_read.add_argument("--range", required=True, help="Range in A1 notation (e.g. 'Sheet1!A1:Z100')")
    p_read.add_argument("--json", action="store_true", help="Output as JSON")
    p_read.add_argument("--csv", action="store_true", help="Output as CSV")

    # --- write ---
    p_write = subparsers.add_parser("write", help="Write to a range")
    p_write.add_argument("--spreadsheet-id", required=True, help="Spreadsheet ID")
    p_write.add_argument("--range", required=True, help="Starting cell (e.g. 'Sheet1!A1')")
    p_write.add_argument("--values", help='JSON array of arrays: \'[["a","b"],["c","d"]]\'')
    p_write.add_argument("--csv-file", help="Path to CSV file to upload")
    p_write.add_argument("--value-input-option", default="RAW", choices=["RAW", "USER_ENTERED"],
                         help="How to interpret values (default: RAW)")

    # --- append ---
    p_append = subparsers.add_parser("append", help="Append rows to end of sheet")
    p_append.add_argument("--spreadsheet-id", required=True, help="Spreadsheet ID")
    p_append.add_argument("--sheet-name", help="Sheet tab name (default: first sheet)")
    p_append.add_argument("--values", required=True, help='JSON array of arrays')
    p_append.add_argument("--value-input-option", default="RAW", choices=["RAW", "USER_ENTERED"],
                          help="How to interpret values (default: RAW)")

    # --- list-sheets ---
    p_list = subparsers.add_parser("list-sheets", help="List all tabs in a spreadsheet")
    p_list.add_argument("--spreadsheet-id", required=True, help="Spreadsheet ID")

    # --- create-sheet ---
    p_create = subparsers.add_parser("create-sheet", help="Create a new tab")
    p_create.add_argument("--spreadsheet-id", required=True, help="Spreadsheet ID")
    p_create.add_argument("--sheet-name", required=True, help="Name for the new tab")

    # --- clear ---
    p_clear = subparsers.add_parser("clear", help="Clear a range")
    p_clear.add_argument("--spreadsheet-id", required=True, help="Spreadsheet ID")
    p_clear.add_argument("--range", required=True, help="Range to clear (e.g. 'Sheet1!A1:Z100')")

    # --- format ---
    p_fmt = subparsers.add_parser("format", help="Apply basic formatting")
    p_fmt.add_argument("--spreadsheet-id", required=True, help="Spreadsheet ID")
    p_fmt.add_argument("--range", required=True, help="Range to format (e.g. 'Sheet1!A1:Z1')")
    p_fmt.add_argument("--bold", action="store_true", help="Make text bold")
    p_fmt.add_argument("--italic", action="store_true", help="Make text italic")
    p_fmt.add_argument("--font-size", type=int, help="Font size in pt")
    p_fmt.add_argument("--bg-color", help="Background color as hex (#RRGGBB)")
    p_fmt.add_argument("--text-color", help="Text color as hex (#RRGGBB)")
    p_fmt.add_argument("--h-align", choices=["left", "center", "right"], help="Horizontal alignment")

    # --- info ---
    p_info = subparsers.add_parser("info", help="Show spreadsheet metadata")
    p_info.add_argument("--spreadsheet-id", required=True, help="Spreadsheet ID")

    # --- find ---
    p_find = subparsers.add_parser("find", help="Search for a value in a sheet")
    p_find.add_argument("--spreadsheet-id", required=True, help="Spreadsheet ID")
    p_find.add_argument("--sheet-name", help="Sheet tab name (default: searches first sheet)")
    p_find.add_argument("--query", required=True, help="Search term")

    # --- get-url ---
    p_url = subparsers.add_parser("get-url", help="Get the Google Sheets URL")
    p_url.add_argument("--spreadsheet-id", required=True, help="Spreadsheet ID")

    args = parser.parse_args()

    commands = {
        "read": cmd_read,
        "write": cmd_write,
        "append": cmd_append,
        "list-sheets": cmd_list_sheets,
        "create-sheet": cmd_create_sheet,
        "clear": cmd_clear,
        "format": cmd_format,
        "info": cmd_info,
        "find": cmd_find,
        "get-url": cmd_get_url,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
