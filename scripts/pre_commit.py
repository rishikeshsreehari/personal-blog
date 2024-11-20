import os
import json
import subprocess
import tkinter as tk
from tkinter import ttk

VERSION_FILE = "data/version.json"

def get_commit_type_gui():
    """Show a GUI window to select commit type."""
    result = {"type": None}
    
    def on_button_click(type_choice):
        result["type"] = type_choice
        root.quit()
        root.destroy()
    
    root = tk.Tk()
    root.title("Select Commit Type")
    
    # Center the window
    window_width = 300
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    label = ttk.Label(root, text="Select the type of commit:", padding=10)
    label.pack()
    
    # Style for buttons
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
    """Get commit type via command line."""
    print("Select commit type:")
    print("F) Fix\nN) New post\nU) Update\nX) Major change")
    choice = input("Your choice: ").upper()
    while choice not in ["F", "N", "U", "X"]:
        print("Invalid choice, please select F, N, U, or X.")
        choice = input("Your choice: ").upper()
    return choice

def get_staged_changes():
    """Get the staged changes message."""
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-status"], text=True
    ).strip()
    return staged.split("\n") if staged else []

def read_version_file():
    """Read the version file and return its data."""
    if not os.path.exists(VERSION_FILE):
        data = {"Version": "24.0.U.0000", "PushCount": 0}
        with open(VERSION_FILE, "w") as f:
            json.dump(data, f, indent=4)
    with open(VERSION_FILE, "r") as f:
        return json.load(f)

def update_version_file(version, push_count):
    """Update the version in the version file."""
    data = {
        "Version": version,
        "PushCount": push_count,
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

    try:
        # Try CLI first
        commit_type = get_commit_type_cli()
    except:
        # If CLI fails, use GUI
        commit_type = get_commit_type_gui()
        if not commit_type:
            print("No commit type selected")
            exit(1)

    # Read current version and push count
    version_data = read_version_file()
    current_push_count = version_data.get("PushCount", 0)
    new_push_count = current_push_count + 1

    # Generate version number
    version = f"24.{new_push_count}.{commit_type}.1911"

    print(f"Setting version to: {version}")

    # Update version.json
    update_version_file(version, new_push_count)
    print(f"Updated version to {version} in {VERSION_FILE}")

    # Stage version.json
    subprocess.run(["git", "add", VERSION_FILE])

if __name__ == "__main__":
    main()
    
    
#Very interesting