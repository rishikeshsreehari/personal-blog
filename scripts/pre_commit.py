import os
import json
import subprocess
import sys
import platform
import tkinter as tk
from tkinter import ttk
from datetime import datetime

VERSION_FILE = "data/version.json"

def is_cli():
    """Check if running in CLI mode"""
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

def get_commit_type_gui():
    """Show a GUI window to select commit type."""
    result = {"type": None}
    
    def on_button_click(type_choice):
        result["type"] = type_choice
        root.quit()
        root.destroy()
    
    root = tk.Tk()
    root.title("Select Commit Type")
    
    # Center the window and bring to front
    window_width = 300
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Make window stay on top
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

def get_staged_changes():
    """Get the staged changes message."""
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-status"], text=True
    ).strip()
    return staged.split("\n") if staged else []

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

def update_version_file(version, push_count):
    """Update the version in the version file."""
    long_hash, short_hash = get_git_hashes()
    data = {
        "Version": version,
        "PushCount": push_count,
        "LastCommitLong": long_hash or "",
        "LastCommitShort": short_hash or ""
    }
    with open(VERSION_FILE, "w") as f:
        json.dump(data, f, indent=4)

def main():
    """Main function to handle pre-commit tasks."""
    # Check if there are staged changes
    staged_changes = get_staged_changes()
    if not staged_changes:
        print("No changes staged for commit.")
        exit(1)

    # Skip if version.json is the only change
    if len(staged_changes) == 1 and VERSION_FILE in staged_changes[0]:
        print("Skipping version update for version.json commit")
        exit(0)

    # Determine whether to use CLI or GUI based on the environment
    if is_cli():
        print("Running in CLI mode.")
        commit_type = get_commit_type_cli()
    else:
        commit_type = get_commit_type_gui()

    if not commit_type:
        print("No commit type selected. Aborting commit.")
        exit(1)

    # Read current version and push count
    version_data = read_version_file()
    current_push_count = version_data.get("PushCount", 0)
    new_push_count = current_push_count + 1

    # Get current date in DDMM format
    current_date = datetime.now().strftime("%d%m")

    # Generate version number
    version = f"24.{new_push_count}.{commit_type}.{current_date}"

    print(f"Setting version to: {version}")

    # Update version.jsonn
    update_version_file(version, new_push_count)
    print(f"Updated version to {version} in {VERSION_FILE}")

    # Stage version.json
    subprocess.run(["git", "add", VERSION_FILE])

if __name__ == "__main__":
    main()