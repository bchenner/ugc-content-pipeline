#!/usr/bin/env python3
"""
Auth management for Google Sheets skill.
Handles service account key discovery and configuration.
"""

import argparse
import json
import os
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
CONFIG_FILE = DATA_DIR / "config.json"

DEFAULT_KEY_LOCATIONS = [
    os.environ.get("GSHEETS_SERVICE_ACCOUNT_KEY", ""),
    str(Path.home() / "Downloads" / "crypto-quasar-489706-a8-9530762b9b2d.json"),
    "C:/Users/Privat/Downloads/crypto-quasar-489706-a8-9530762b9b2d.json",
]


def load_config():
    """Load config from data/config.json."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_config(config):
    """Save config to data/config.json."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def find_key_path():
    """Find the service account key, checking config first, then default locations."""
    config = load_config()

    # Check configured path first
    configured = config.get("service_account_key")
    if configured and Path(configured).exists():
        return configured

    # Search default locations
    for loc in DEFAULT_KEY_LOCATIONS:
        if not loc:
            continue
        if Path(loc).exists():
            # Auto-save to config
            config["service_account_key"] = loc
            save_config(config)
            return loc

    return None


def get_service_account_email(key_path):
    """Extract the service account email from the key file."""
    try:
        with open(key_path, 'r') as f:
            key_data = json.load(f)
        return key_data.get("client_email", "unknown")
    except Exception:
        return "unknown"


def cmd_status(args):
    """Show current auth status."""
    key_path = find_key_path()

    if key_path:
        email = get_service_account_email(key_path)
        print(f"Auth status: OK")
        print(f"Key file: {key_path}")
        print(f"Service account: {email}")
        print(f"\nShare spreadsheets with this email to grant access:")
        print(f"  {email}")

        # Quick validation
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            creds = service_account.Credentials.from_service_account_file(
                key_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            service = build('sheets', 'v4', credentials=creds)
            print(f"\nAPI connection: OK")
        except Exception as e:
            print(f"\nAPI connection: FAILED - {e}")
    else:
        print("Auth status: NOT CONFIGURED")
        print("\nNo service account key found.")
        print("Use: python scripts/run.py auth.py set-key <path-to-key.json>")
        print(f"\nSearched locations:")
        for loc in DEFAULT_KEY_LOCATIONS:
            print(f"  {loc}")
        sys.exit(1)


def cmd_set_key(args):
    """Set or change the service account key path."""
    key_path = args.key_path

    if not Path(key_path).exists():
        print(f"File not found: {key_path}")
        sys.exit(1)

    # Validate it's a valid service account key
    try:
        with open(key_path, 'r') as f:
            key_data = json.load(f)
        if 'client_email' not in key_data or 'private_key' not in key_data:
            print("Invalid service account key file (missing client_email or private_key).")
            sys.exit(1)
    except json.JSONDecodeError:
        print("File is not valid JSON.")
        sys.exit(1)

    config = load_config()
    config["service_account_key"] = str(Path(key_path).resolve())
    save_config(config)

    email = key_data.get("client_email", "unknown")
    print(f"Key configured successfully.")
    print(f"Key file: {config['service_account_key']}")
    print(f"Service account: {email}")


def main():
    parser = argparse.ArgumentParser(description="Google Sheets auth management")
    subparsers = parser.add_subparsers(dest="command")

    # status
    subparsers.add_parser("status", help="Show current auth status")

    # set-key
    sk = subparsers.add_parser("set-key", help="Set service account key path")
    sk.add_argument("key_path", help="Path to the service account JSON key file")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status(args)
    elif args.command == "set-key":
        cmd_set_key(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
