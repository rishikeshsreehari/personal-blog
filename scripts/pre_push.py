import os
import json
import subprocess

VERSION_FILE = "data/version.json"


def get_git_commits():
    """Retrieve the list of commits to be pushed."""
    commits = subprocess.check_output(
        ["git", "log", "--oneline", "@{push}..HEAD"], text=True
    ).strip()
    return commits.split("\n") if commits else []


def get_commit_type(commit_message):
    """Prompt for input to categorize each commit."""
    print(f'> "{commit_message}"')
    print("Select type:")
    print("F) Fix\nN) New post\nU) Update\nX) Major change\nI) Ignore")
    choice = input("Your choice: ").upper()
    while choice not in ["F", "N", "U", "X", "I"]:
        print("Invalid choice, please select F, N, U, X, or I.")
        choice = input("Your choice: ").upper()
    return choice


def get_commit_hash_after_stage():
    """Get both full and short hash after staging changes."""
    # Stage all changes first
    subprocess.run(["git", "add", "."])
    # Create a temporary commit to get the hash
    subprocess.run(["git", "commit", "--no-verify", "-m", "Temporary commit for hash"])
    
    full_hash = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip()
    short_hash = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"], text=True
    ).strip()
    
    # Reset the temporary commit but keep changes staged
    subprocess.run(["git", "reset", "--soft", "HEAD^"])
    
    return full_hash, short_hash


def read_version_file():
    """Read the version file and return its data."""
    if not os.path.exists(VERSION_FILE):
        # Initialize version.json if it doesn't exist
        data = {"Version": "24.0.U.0000", "PushCount": 0}
        with open(VERSION_FILE, "w") as f:
            json.dump(data, f, indent=4)
    with open(VERSION_FILE, "r") as f:
        return json.load(f)


def update_version_file(version, push_count):
    """Update the version and push count in the version file."""
    # Stage current changes and get hash
    full_hash, short_hash = get_commit_hash_after_stage()
    
    data = {
        "Version": version,
        "PushCount": push_count,
        "LastCommitHash": full_hash,
        "ShortCommitHash": short_hash
    }
    with open(VERSION_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():
    """Main function to handle pre-push tasks."""
    # Get commits to be pushed
    commits = get_git_commits()
    if not commits:
        print("No commits to push.")
        return

    print(f"Found {len(commits)} commits to push:")
    types = []
    for i, commit in enumerate(commits, 1):
        commit_message = " ".join(commit.split(" ")[1:])  # Get the message part
        print(f"> {i}. \"{commit_message}\"")
        commit_type = get_commit_type(commit_message)
        if commit_type == "I":
            print(f"Ignoring commit: {commit_message}")
            continue  # Skip this commit
        types.append(commit_type)

    if not types:
        print("All commits were ignored. No changes to process.")
        return

    # Determine version type
    unique_types = set(types)
    version_type = "M" if len(unique_types) > 1 else unique_types.pop()

    # Read current version and push count from version.json
    version_data = read_version_file()
    current_push_count = version_data.get("PushCount", 0)
    new_push_count = current_push_count + 1

    # Generate version number
    version = f"24.{new_push_count}.{version_type}.1911"

    print(f"\n{'Multiple change types detected' if version_type == 'M' else ''}")
    print(f"Automatically setting version type to {version_type}")
    print(f"Final version: {version}\n")

    # Update version.json with all information including the hash
    update_version_file(version, new_push_count)
    print(f"Updated version to {version} in {VERSION_FILE}")

    # Commit all changes in a single commit
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "--no-verify", "-m", f"Update version to {version}"])


if __name__ == "__main__":
    main()