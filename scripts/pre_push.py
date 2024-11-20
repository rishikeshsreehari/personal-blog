import os
import json
import subprocess
import sys

# File paths
PUSH_COUNT_FILE = "push.txt"
VERSION_FILE = "data/version.json"

def is_interactive():
    """Check if the script is running in an interactive shell."""
    return sys.stdin.isatty()

def read_push_number():
    """Read the current push number from the push count file."""
    if not os.path.exists(PUSH_COUNT_FILE):
        with open(PUSH_COUNT_FILE, "w") as f:
            f.write("0")
    with open(PUSH_COUNT_FILE, "r") as f:
        return int(f.read().strip())

def increment_push_number(current_push):
    """Increment and save the push number."""
    new_push = current_push + 1
    with open(PUSH_COUNT_FILE, "w") as f:
        f.write(str(new_push))
    return new_push

def get_git_commits():
    """Retrieve the list of commits to be pushed."""
    commits = subprocess.check_output(["git", "log", "--oneline", "@{push}..HEAD"], text=True).strip()
    return commits.split("\n") if commits else []

def get_commit_type(commit_message):
    """Prompt for input or use default type when non-interactive."""
    print(f'> "{commit_message}"')
    if not is_interactive():
        print("Non-interactive mode detected. Defaulting to 'Update'.")
        return "U"  # Default to Update
    print("Select type:")
    print("F) Fix\nN) New post\nU) Update\nX) Major change")
    choice = input("Your choice: ").upper()
    while choice not in ["F", "N", "U", "X"]:
        print("Invalid choice, please select F, N, U, or X.")
        choice = input("Your choice: ").upper()
    return choice

def update_version_file(version):
    """Update the version file with the new version number."""
    if not os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "w") as f:
            json.dump({"Version": version, "Commit": ""}, f, indent=4)
    with open(VERSION_FILE, "r") as f:
        data = json.load(f)
    current_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    data["Version"] = version
    data["Commit"] = current_commit
    with open(VERSION_FILE, "w") as f:
        json.dump(data, f, indent=4)

def main():
    """Main function to handle pre-push logic."""
    # Get all commits
    commits = get_git_commits()
    if not commits:
        print("No commits to push.")
        return

    print(f"Found {len(commits)} commits to push:")
    types = []
    for i, commit in enumerate(commits, 1):
        commit_message = " ".join(commit.split(" ")[1:])  # Get the message part
        print(f"> {i}. \"{commit_message}\"")
        types.append(get_commit_type(commit_message))

    # Determine version type
    unique_types = set(types)
    version_type = "M" if len(unique_types) > 1 else unique_types.pop()

    # Generate the new version number
    current_push = read_push_number()
    push_number = increment_push_number(current_push)
    version = f"24.{push_number}.{version_type}.{os.path.basename(VERSION_FILE)[:4]}"

    print(f"\n{'Multiple change types detected' if version_type == 'M' else ''}")
    print(f"Automatically setting version type to {version_type}")
    print(f"Final version: {version}\n")

    # Update version file
    update_version_file(version)

    # Log actions
    print(f"Updating version to {version}")
    print(f"Push incremented to {push_number}")

if __name__ == "__main__":
    main()
