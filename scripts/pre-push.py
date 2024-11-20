import os
import json
import subprocess
import sys
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from pathlib import Path

VERSION_FILE = "data/version.json"
LOG_FILE = "content/log.md"
LOCK_FILE = ".git/pre-push.lock"

def check_lock():
    """Check if the lock file exists."""
    return os.path.exists(LOCK_FILE)

def create_lock():
    """Create the lock file."""
    Path(LOCK_FILE).touch()

def remove_lock():
    """Remove the lock file."""
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

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

def get_unpushed_commits():
    """Get all commits that haven't been pushed yet."""
    try:
        # Get the remote branch we're pushing to
        remote_branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "@{u}"],
            text=True
        ).strip()
        
        # Get all commits between the remote and local branch
        commits = subprocess.check_output(
            ["git", "log", f"{remote_branch}..HEAD", "--pretty=format:%h|%s"],
            text=True
        ).strip().split('\n')
        
        # Filter out empty strings
        return [commit for commit in commits if commit]
    except subprocess.CalledProcessError:
        return []

def update_changelog(commits):
    """Update the changelog with new commits."""
    if not os.path.exists(LOG_FILE):
        # Create log file if it doesn't exist
        with open(LOG_FILE, "w") as f:
            f.write("<!--LOG_PLACEHOLDER_START-->\n\n<!--LOG_PLACEHOLDER_END-->")
    
    # Read existing content
    with open(LOG_FILE, "r") as f:
        content = f.read()
    
    # Find the placeholders
    start_marker = "<!--LOG_PLACEHOLDER_START-->"
    end_marker = "<!--LOG_PLACEHOLDER_END-->"
    
    start_idx = content.find(start_marker) + len(start_marker)
    end_idx = content.find(end_marker)
    
    # Format new commits
    current_date = datetime.now().strftime("%Y-%m-%d")
    new_logs = [f"- {commit.split('|')[1]} ({commit.split('|')[0]})" for commit in commits]
    changelog_entry = f"\n## {current_date}\n" + "\n".join(new_logs) + "\n"
    
    # Insert between placeholders
    new_content = (
        content[:start_idx] + 
        "\n" + changelog_entry + 
        (content[start_idx:end_idx].strip() + "\n" if content[start_idx:end_idx].strip() else "") +
        content[end_idx:]
    )
    
    # Write back to file
    with open(LOG_FILE, "w") as f:
        f.write(new_content)

def pre_push():
    """Handle pre-push tasks."""
    if check_lock():
        return

    create_lock()

    try:
        # Get unpushed commits
        commits = get_unpushed_commits()
        if not commits:
            print("No unpushed commits found.")
            return

        # Read and update version
        version_data = read_version_file()
        current_push_count = version_data.get("PushCount", 0)
        new_push_count = current_push_count + 1
        current_date = datetime.now().strftime("%d%m")
        
        # Use U for Update as default type for push version bump
        version = f"24.{new_push_count}.U.{current_date}"
        
        version_data["Version"] = version
        version_data["PushCount"] = new_push_count

        # Write updated version
        with open(VERSION_FILE, "w") as f:
            json.dump(version_data, f, indent=4)

        # Update changelog
        update_changelog(commits)

        # Stage and commit version and log updates
        subprocess.run(["git", "add", VERSION_FILE, LOG_FILE])
        subprocess.run(["git", "commit", "-m", f"Pre-push update: Bump version to {version} and update changelog"])
        
    finally:
        remove_lock()

if __name__ == "__main__":
    pre_push()