import os
import json
import subprocess
import sys
from pathlib import Path

VERSION_FILE = "data/version.json"
LOCK_FILE = ".git/post-commit.lock"

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

def get_current_commit_hashes():
    """Get the current commit hashes before any amend."""
    try:
        # Get the current commit hash
        long_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip()
        short_hash = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True
        ).strip()
        return long_hash, short_hash
    except subprocess.CalledProcessError as e:
        print(f"Error getting git hashes: {e}")
        return None, None

def update_commit_hashes():
    if check_lock():
        return

    try:
        create_lock()
        
        # Get the current commit hash BEFORE any changes
        long_hash, short_hash = get_current_commit_hashes()
        print(f"Current commit hash: {long_hash}")
        
        if long_hash and short_hash:
            with open(VERSION_FILE, "r") as f:
                data = json.load(f)
            
            # Update the hashes
            data["LastCommitLong"] = long_hash
            data["LastCommitShort"] = short_hash
            
            # Write back to version.json
            with open(VERSION_FILE, "w") as f:
                json.dump(data, f, indent=4)
            
            # Stage and amend the commit one final time
            subprocess.run(["git", "add", VERSION_FILE])
            subprocess.run(["git", "commit", "--amend", "--no-edit", "--no-verify"])
            
            print(f"Updated commit hashes in {VERSION_FILE}")
            print(f"Long hash: {long_hash}")
            print(f"Short hash: {short_hash}")
        else:
            print("Failed to get commit hashes")
            
    except Exception as e:
        print(f"Error updating commit hashes: {e}")
    finally:
        remove_lock()

if __name__ == "__main__":
    print("Starting post-commit hook...")
    update_commit_hashes()
    print("Post-commit hook completed")