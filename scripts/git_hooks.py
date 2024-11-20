import os
import json
import subprocess
import sys
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from pathlib import Path

VERSION_FILE = "data/version.json"
LOCK_FILE = ".git/pre-commit.lock"

# Utility Functions
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

def get_current_commit_hash():
    """Get the current commit hash."""
    try:
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

def get_commit_type_gui():
    """Show a GUI window to select commit type."""
    result = {"type": None}

    def on_button_click(type_choice):
        result["type"] = type_choice
        root.quit()
        root.destroy()

    root = tk.Tk()
    root.title("Select Commit Type")

    window_width = 300
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    root.attributes('-topmost', True)

    label = ttk.Label(root, text="Select the type of commit:", padding=10)
    label.pack()

    style = ttk.Style()
    style.configure('Custom.TButton', padding=5)

    buttons = [
        ("Fix", "F"),
        ("New Post", "N"),
        ("Update", "U"),
        ("Major Change", "X")
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

# Main Functions
def pre_commit():
    """Handle pre-commit tasks."""
    # Avoid re-execution during amendments
    if check_lock():
        return

    # Create a lock to prevent recursive invocation
    create_lock()

    try:
        # Check for staged changes
        staged_changes = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"], text=True
        ).strip().splitlines()
        if not staged_changes:
            print("No changes staged for commit.")
            sys.exit(1)

        # Get commit type via GUI
        commit_type = get_commit_type_gui()
        if not commit_type:
            print("No commit type selected. Aborting commit.")
            sys.exit(1)

        # Read and update version
        version_data = read_version_file()
        current_push_count = version_data.get("PushCount", 0)
        new_push_count = current_push_count + 1
        current_date = datetime.now().strftime("%d%m")
        version = f"24.{new_push_count}.{commit_type}.{current_date}"

        version_data["Version"] = version
        version_data["PushCount"] = new_push_count
        version_data["LastCommitLong"] = "TBD"
        version_data["LastCommitShort"] = "TBD"

        with open(VERSION_FILE, "w") as f:
            json.dump(version_data, f, indent=4)

        # Stage changes and commit
        subprocess.run(["git", "add", "-u"])
        subprocess.run(["git", "commit", "-m", f"Bump version to {version}"])
    finally:
        # Remove lock after execution
        remove_lock()

def post_commit():
    """Handle post-commit tasks."""
    # Avoid re-execution due to amendments
    if check_lock():
        return

    try:
        # Create a lock to prevent recursive invocation
        create_lock()

        # Get current commit hash
        long_hash, short_hash = get_current_commit_hash()
        if not long_hash or not short_hash:
            print("Could not retrieve current commit hash.")
            return

        # Update version.json with commit hash
        version_data = read_version_file()
        version_data["LastCommitLong"] = long_hash
        version_data["LastCommitShort"] = short_hash

        with open(VERSION_FILE, "w") as f:
            json.dump(version_data, f, indent=4)

        # Stage and amend commit
        subprocess.run(["git", "add", VERSION_FILE])
        subprocess.run(["git", "commit", "--amend", "--no-edit", "--no-verify"])
    finally:
        # Remove lock after executionn
        remove_lock()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "post-commit":
        post_commit()
    else:
        pre_commit()
