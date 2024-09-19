import yaml
import json
import subprocess
import os

def get_commit_hash():
    # Check if the environment variable is set
    commit_hash = os.getenv('GIT_COMMIT_HASH')
    if commit_hash:
        return commit_hash

    # Fallback to git command if not running in CI
    try:
        commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('utf-8')
        return commit_hash
    except subprocess.CalledProcessError:
        print("Error: Could not retrieve Git commit hash.")
        return None

def read_version_from_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            version_number = config.get('params', {}).get('version', None)
            return version_number
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None
    except yaml.YAMLError as exc:
        print(f"Error reading YAML file: {exc}")
        return None

def update_version_file(version_number):
    commit_hash = get_commit_hash()
    if not commit_hash:
        print("Error: Cannot update version file without commit hash.")
        return

    version_data = {
        "Version": version_number,
        "Commit": commit_hash
    }

    # Write version data to version.json file
    with open('data/version.json', 'w') as version_file:
        json.dump(version_data, version_file, indent=4)

    print("Version file updated successfully.")

if __name__ == "__main__":
    # Read the version number from config.yml
    version_number = read_version_from_config('config.yml')
    
    if version_number:
        # Update the version file
        update_version_file(version_number)
