import os
import json
import subprocess
from pathlib import Path

# Get the git root directory
def get_git_root():
    try:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
        return root
    except:
        return os.getcwd()

# Use absolute path for VERSION_FILE
GIT_ROOT = get_git_root()
VERSION_FILE = os.path.join(GIT_ROOT, "data", "version.json")

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
    except subprocess.CalledProcessError as e:
        print(f"Error getting git hashes: {e}")
        return None, None

def update_commit_hashes():
    """Update the commit hashes in version.json after commit."""
    print("Starting update_commit_hashes...")
    try:
        with open(VERSION_FILE, "r") as f:
            data = json.load(f)
        
        long_hash, short_hash = get_git_hashes()
        if long_hash and short_hash:
            data["LastCommitLong"] = long_hash
            data["LastCommitShort"] = short_hash
            
            with open(VERSION_FILE, "w") as f:
                json.dump(data, f, indent=4)
            
            print(f"Updated version.json with hashes")
            print(f"Long hash: {long_hash}")
            print(f"Short hash: {short_hash}")
            
            # Stage and commit the updated version.json
            subprocess.run(["git", "add", VERSION_FILE], check=True)
            subprocess.run(["git", "commit", "--amend", "--no-edit", "--no-verify"], check=True)
            print("Successfully amended commit")
        else:
            print("Failed to get commit hashes")
            
    except Exception as e:
        print(f"Error updating commit hashes: {e}")
        raise

if __name__ == "__main__":
    print(f"Post-commit script starting...")
    print(f"Version file path: {VERSION_FILE}")
    update_commit_hashes()
    print("Post-commit script completed")