import os
import json
import subprocess
import sys
from pathlib import Path

VERSION_FILE = "data/version.json"
LOCK_FILE = ".git/post-commit.lock"

def check_lock():
    """Check if lock exists and is still valid"""
    if os.path.exists(LOCK_FILE):
        print("Lock file exists, skipping post-commit hook")
        return True
    return False

def create_lock():
    """Create lock file"""
    Path(LOCK_FILE).touch()

def remove_lock():
    """Remove lock file"""
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

def get_git_hashes():
    """Get the latest git commit hashes (long and short)."""
    try:
        long_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip()
        short_hash = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True
        ).strip()
        return long_hash, short_hash
    except subprocess.CalledProcessError:
        return None, None

def update_commit_hashes():
    """Update the commit hashes in version.json after commit."""
    if check_lock():
        return

    try:
        create_lock()
        
        with open(VERSION_FILE, "r") as f:
            data = json.load(f)
        
        # Stage and commit the updated version.json first
        subprocess.run(["git", "add", VERSION_FILE])
        subprocess.run(["git", "commit", "--amend", "--no-edit", "--no-verify"])
        
        # Now get the hashes AFTER the amend
        long_hash, short_hash = get_git_hashes()
        if long_hash and short_hash:
            data["LastCommitLong"] = long_hash
            data["LastCommitShort"] = short_hash
            
            with open(VERSION_FILE, "w") as f:
                json.dump(data, f, indent=4)
            
            # Stage and commit again with the correct hashes
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