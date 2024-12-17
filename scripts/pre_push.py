#!/usr/bin/env python3

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
        with open(VERSION_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
def get_current_commit_hash():
    """Get the current commit hash."""
    try:
        long_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], encoding="utf-8"
        ).strip()
        short_hash = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], encoding="utf-8"
        ).strip()
        return long_hash, short_hash
    except subprocess.CalledProcessError:
        return "", ""

def get_commit_type_gui(commit_msg):
    """Show a GUI window to select commit type."""
    result = {"type": None}

    def on_button_click(type_choice):
        result["type"] = type_choice
        root.quit()
        root.destroy()

    root = tk.Tk()
    root.title("Select Commit Type")

    window_width = 400
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    root.attributes('-topmost', True)

    label = ttk.Label(root, text=f"Select type for commit:\n{commit_msg}", padding=10, wraplength=350)
    label.pack()

    style = ttk.Style()
    style.configure('Custom.TButton', padding=5)

    buttons = [
        ("Fix", "F"),
        ("New Post", "N"),
        ("Update", "U"),
        ("Major Change", "X"),
        ("Removed", "R")
    ]

    for text, type_code in buttons:
        btn = ttk.Button(
            root,
            text=text,
            style='Custom.TButton',
            command=lambda t=type_code: on_button_click(t)
        )
        btn.pack(pady=5)

    root.mainloop()
    return result["type"]

def determine_version_type(commit_entries):
    """Determine version type based on commit entries."""
    if not commit_entries:
        return "U"  # Default
        
    types = set(entry[2] for entry in commit_entries)
    if len(types) > 1:
        return "M"
    return types.pop()

def update_changelog(commit_entries, version):
    """Update the changelog with new commits."""
    REPO_URL = "https://github.com/rishikeshsreehari/personal-blog/"
    
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("<!--LOG_PLACEHOLDER_START-->\n\n<!--LOG_PLACEHOLDER_END-->")
    
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    start_marker = "<!--LOG_PLACEHOLDER_START-->"
    end_marker = "<!--LOG_PLACEHOLDER_END-->"
    start_idx = content.find(start_marker) + len(start_marker)
    end_idx = content.find(end_marker)
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    commits_by_type = {
        "F": "Fixes",
        "N": "Additions",
        "U": "Updations",
        "R": "Removal",
        "X": "New Features"
    }
    
    type_entries = {t: [] for t in commits_by_type.keys()}
    for hash, msg, type, files in commit_entries:
        file_entries = [
            f"     {i + 1}. [`{file.strip()}`]({REPO_URL}blob/main/{file.strip()})"
            for i, file in enumerate(files) if file.strip()
        ]
        file_section = "\n".join(file_entries)
        entry = f"""{len(type_entries[type]) + 1}. **{msg}**  
   - *Commit:* [`{hash}`]({REPO_URL}commit/{hash})  
   - *Files:*  
{file_section}
"""
        type_entries[type].append(entry)
    
    changelog_section = [f"### **v{version}** ({current_date})\n"]
    for type, title in commits_by_type.items():
        if type_entries[type]:
            changelog_section.append(f"#### **{title}**\n")
            changelog_section.extend(type_entries[type])
            changelog_section.append("")  
    
    changelog_entry = "\n".join(changelog_section) + "\n---\n"
    new_content = (
        content[:start_idx] + 
        "\n" + changelog_entry + 
        (content[start_idx:end_idx].strip() + "\n" if content[start_idx:end_idx].strip() else "") +
        content[end_idx:]
    )
    
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

def get_unpushed_commits():
    """Get all commits that haven't been pushed yet with their changed files."""
    try:
        remote_branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "@{u}"],
            encoding="utf-8"
        ).strip()
        commits = subprocess.check_output(
            ["git", "log", f"{remote_branch}..HEAD", "--pretty=format:%h|%s"],
            encoding="utf-8"
        ).strip().split('\n')
        commit_data = []
        for commit in commits:
            if commit and not commit.split('|')[1].startswith("Pre-push update:"):
                hash, msg = commit.split('|')
                files = subprocess.check_output(
                    ["git", "show", "--name-only", "--format=", hash],
                    encoding="utf-8"
                ).strip().split('\n')
                commit_data.append((hash, msg, files))
        return commit_data
    except subprocess.CalledProcessError:
        return []

def pre_push():
    """Handle pre-push tasks."""
    if check_lock():
        return

    create_lock()
    try:
        commits = get_unpushed_commits()
        if not commits:
            print("No unpushed commits found.")
            return

        last_commit_msg = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%B"], encoding="utf-8"
        ).strip()
        if last_commit_msg.startswith("Pre-push update:"):
            return

        commit_entries = []
        for hash, msg, files in commits:
            commit_type = get_commit_type_gui(msg)
            if not commit_type:
                print(f"No type selected for commit {hash}. Aborting push.")
                sys.exit(1)
            commit_entries.append((hash, msg, commit_type, files))

        long_hash, short_hash = get_current_commit_hash()
        version_type = determine_version_type(commit_entries)
        version_data = read_version_file()
        new_push_count = version_data.get("PushCount", 0) + 1
        current_date = datetime.now().strftime("%d%m")
        version = f"24.{new_push_count}.{version_type}.{current_date}"
        
        version_data.update({
            "Version": version, "PushCount": new_push_count,
            "LastCommitLong": long_hash, "LastCommitShort": short_hash
        })

        with open(VERSION_FILE, "w", encoding="utf-8") as f:
            json.dump(version_data, f, indent=4)

        update_changelog(commit_entries, version)
        subprocess.run(["git", "add", VERSION_FILE, LOG_FILE])
        subprocess.run(["git", "commit", "-m", f"Pre-push update: Bump version to {version} and update changelog"])
        subprocess.run(["git", "pull", "--rebase"])
    finally:
        remove_lock()

if __name__ == "__main__":
    pre_push()
