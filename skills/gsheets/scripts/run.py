#!/usr/bin/env python3
"""
Universal runner for Google Sheets skill scripts.
Ensures all scripts run with the correct virtual environment and PYTHONIOENCODING=utf-8.
"""

import os
import sys
import subprocess
import venv
from pathlib import Path


def get_skill_dir():
    return Path(__file__).parent.parent


def get_venv_dir():
    return get_skill_dir() / ".venv"


def get_venv_python():
    """Get the virtual environment Python executable."""
    venv_dir = get_venv_dir()
    if os.name == 'nt':
        return venv_dir / "Scripts" / "python.exe"
    else:
        return venv_dir / "bin" / "python"


def get_venv_pip():
    """Get the virtual environment pip executable."""
    venv_dir = get_venv_dir()
    if os.name == 'nt':
        return venv_dir / "Scripts" / "pip.exe"
    else:
        return venv_dir / "bin" / "pip"


def ensure_venv():
    """Ensure virtual environment exists with dependencies installed."""
    venv_dir = get_venv_dir()
    skill_dir = get_skill_dir()
    venv_python = get_venv_python()
    venv_pip = get_venv_pip()
    requirements_file = skill_dir / "requirements.txt"

    if not venv_dir.exists():
        print("Setting up virtual environment (first-time, may take a minute)...")
        try:
            venv.create(venv_dir, with_pip=True)
        except Exception as e:
            print(f"Failed to create venv: {e}")
            sys.exit(1)

        # Upgrade pip
        subprocess.run(
            [str(venv_pip), "install", "--upgrade", "pip"],
            capture_output=True, text=True
        )

        # Install requirements
        if requirements_file.exists():
            result = subprocess.run(
                [str(venv_pip), "install", "-r", str(requirements_file)],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                print(f"Failed to install dependencies: {result.stderr}")
                sys.exit(1)

        print("Environment ready.")

    return venv_python


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/run.py <script_name> [args...]")
        print("\nAvailable scripts:")
        print("  gsheets.py  - Read, write, and manage Google Sheets")
        print("  auth.py     - Manage authentication")
        sys.exit(1)

    script_name = sys.argv[1]
    script_args = sys.argv[2:]

    # Handle both "scripts/script.py" and "script.py" formats
    if script_name.startswith('scripts/') or script_name.startswith('scripts\\'):
        script_name = script_name.split('/', 1)[-1].split('\\', 1)[-1]

    # Ensure .py extension
    if not script_name.endswith('.py'):
        script_name += '.py'

    # Get script path
    skill_dir = get_skill_dir()
    script_path = skill_dir / "scripts" / script_name

    if not script_path.exists():
        print(f"Script not found: {script_name}")
        print(f"Looked for: {script_path}")
        sys.exit(1)

    # Ensure venv exists
    venv_python = ensure_venv()

    # Build command
    cmd = [str(venv_python), str(script_path)] + script_args

    # Set PYTHONIOENCODING for Windows unicode compatibility
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'

    # Run the script
    try:
        result = subprocess.run(cmd, env=env)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
