import os
import json
import subprocess
import sys
import platform
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from pathlib import Path

VERSION_FILE = "data/version.json"
LOCK_FILE = ".git/post-commit.lock"

# Utility Functions
def check_lock():
    if os.path.exists(LOCK_FILE):
        print("Lock file exists, skipping post-commit hook")
        return True
    return False

def create_lock():
    Path(LOCK_FILE).touch()

def remove_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

def get_current_commit_hash():
    """Get the current commit hash."""
    try:
        # Get the current commit hash
        long_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip()
        short_hash = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True
        ).strip()
        return long_hash, short_hash
    except subprocess.CalledProcessError:
        return "", ""

def read_version_file():
    """Read the version file and return its data."""
    if not os.path.exists(VERSION_FILE):
        data = {
            "Version": "24.0.U.0000",
            "PushCount": 0,
            "LastCommitLong": "",
            "LastCommitShort": ""
        }
        with open(VERSION_FILE, "w") as f:
            json.dump(data, f, indent=4)
    with open(VERSION_FILE, "r") as f:
        return json.load(f)

def get_staged_changes():
    """Get the staged changes message."""
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-status"], text=True
    ).strip()
    return staged.split("\n") if staged else []

def is_cli():
    """Check if running in CLI mode."""
    return sys.stdin.isatty() and sys.stdout.isatty()

def custom_input(prompt=""):
    """Read input robustly, handling non-interactive environments."""
    try:
        if platform.system() == "Windows":
            print(prompt, end='', flush=True)
            return input()
        else:
            return input(prompt)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error reading input: {e}")
        return None

def get_commit_type_cli():
    """Get commit type via command line with robust input handling."""
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        print("\nSelect commit type:")
        print("F) Fix")
        print("N) New post")
        print("U) Update")
        print("X) Major change")
        
        choice = custom_input("Your choice: ")
        if choice is None:
            return None
            
        choice = choice.strip().upper()
        if choice in ["F", "N", "U", "X"]:
            return choice
            
        attempts += 1
        if attempts < max_attempts:
            print(f"Invalid choice '{choice}', please select F, N, U, or X. ({max_attempts - attempts} attempts remaining)")
        else:
            print("Maximum attempts reached. Aborting commit.")
            sys.exit(1)

# Main Functions
def pre_commit():
    """Handle pre-commit tasks."""
    # Check if there are staged changes
    staged_changes = get_staged_changes()
    if not staged_changes:
        print("No changes staged for commit.")
        exit(1)

    # Skip if version.json is the only change
    if len(staged_changes) == 1 and VERSION_FILE in staged_changes[0]:
        print("Skipping version update for version.json commit")
        exit(0)

    # Get commit type
    if is_cli():
        print("Running in CLI mode.")
        commit_type = get_commit_type_cli()
    else:
        commit_type = "U"  # Default type if not interactive (fallback)

    if not commit_type:
        print("No commit type selected. Aborting commit.")
        exit(1)

    # Read current version and push count
    version_data = read_version_file()
    current_push_count = version_data.get("PushCount", 0)
    new_push_count = current_push_count + 1

    # Get current date in DDMM format
    current_date = datetime.now().strftime("%d%m")

    # Generate version number (without hash)
    version = f"24.{new_push_count}.{commit_type}.{current_date}"

    print(f"Pre-commit: Setting version to {version}")

    # Update version.json with new version and placeholder for hash
    version_data["Version"] = version
    version_data["PushCount"] = new_push_count
    version_data["LastCommitLong"] = "TBD"
    version_data["LastCommitShort"] = "TBD"

    with open(VERSION_FILE, "w") as f:
        json.dump(version_data, f, indent=4)

    # Stage all changes
    subprocess.run(["git", "add", "-u"])

    # Create a commit
    subprocess.run(["git", "commit", "-m", f"Bump version to {version}"])


def post_commit():
    """Handle post-commit tasks."""
    if check_lock():
        return

    try:
        create_lock()

        # Get the current commit hash
        long_hash, short_hash = get_current_commit_hash()
        if not long_hash or not short_hash:
            print("Could not retrieve current commit hash.")
            return

        # Read the version file
        version_data = read_version_file()

        # Update with the current commit hash
        version_data["LastCommitLong"] = long_hash
        version_data["LastCommitShort"] = short_hash

        # Write the updated version file
        with open(VERSION_FILE, "w") as f:
            json.dump(version_data, f, indent=4)
        print(f"Post-commit: Updated version.json with commit hash {short_hash}")

        # Stage and amend the last commit
        subprocess.run(["git", "add", VERSION_FILE])
        subprocess.run(["git", "commit", "--amend", "--no-edit", "--no-verify"])

    except Exception as e:
        print(f"Error during post-commit: {e}")
    finally:
        remove_lock()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "post-commit":
        print("Starting post-commit hook...")
        post_commit()
        print("Post-commit hook completed")
    else:
        print("Starting pre-commit hook...")
        pre_commit()
