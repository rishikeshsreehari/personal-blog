import os
import hashlib
from datetime import datetime

# Define paths
now_page = "content/now.md"
archive_dir = "content/then"
archive_page = "content/then.md"
hash_file = "content/then/now_hash.txt"

# Function to read file content
def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

# Function to write file content
def write_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

# Function to get content below the front matter
def get_content_below_front_matter(content):
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content  # Invalid front matter format
    return parts[2]

# Function to calculate hash of content
def calculate_hash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

# Function to update the front matter and content of the archived page
def update_archive_content(content, date_str, archive_file_name):
    # Split the front matter and the body
    parts = content.split('---', 2)
    front_matter = parts[1]
    body = parts[2]

    # Update the URL and add index: false in the front matter
    front_matter_lines = front_matter.strip().split('\n')
    new_front_matter = []
    url_added = False
    index_added = False
    for line in front_matter_lines:
        if line.startswith('url:'):
            new_front_matter.append(f'url: "/{archive_file_name[:-3]}"')  # Remove the .md extension
            url_added = True
        else:
            new_front_matter.append(line)
        if line.startswith('index:'):
            index_added = True
    if not url_added:
        new_front_matter.append(f'url: "/{archive_file_name[:-3]}"')
    if not index_added:
        new_front_matter.append('index: false')
    new_front_matter = '\n'.join(new_front_matter)

    # Add archive notice
    archive_notice = f"This is an archive of the Now page on {date_str}\n\n"

    # Remove the section ### Now in Numbers and {{< now_tiles >}}
    if '### Now in Numbers' in body:
        body = body.replace('### Now in Numbers\n', '')
    body = body.replace('{{< now_tiles >}}', '')

    # Combine the updated front matter and body
    new_content = f"---\n{new_front_matter}\n---\n\n{archive_notice}{body}"

    return new_content

# Function to prepend to then.md
def prepend_to_then_md(date_str, archive_file_name):
    url = f"/{archive_file_name[:-3]}"  # Remove the .md extension
    new_entry = f"[{date_str}]({url})\n\n"

    # Read the existing content
    if os.path.exists(archive_page):
        existing_content = read_file(archive_page)
        # Find the position to insert the new entry
        parts = existing_content.split('### Archives\n', 1)
        if len(parts) == 2:
            prelude = parts[0]
            archives = parts[1]
            updated_content = f"{prelude}### Archives\n{new_entry}{archives}"
        else:
            updated_content = f"{existing_content}\n{new_entry}"
    else:
        # If the file doesn't exist, create it with the new entry
        updated_content = f"Idea stolen from [Matthew Smith](https://matthewsmith.website/then)\n\nThis is an archive of all of my “Now” pages. This is mostly for myself—as I suspect it’ll be nice to reflect on down the road—but you may very well find it interesting too!\n\n### Archives\n{new_entry}"

    # Write the updated content back to the file
    write_file(archive_page, updated_content)

# Ensure the archive directory and hash file directory exist
if not os.path.exists(archive_dir):
    os.makedirs(archive_dir)
hash_file_dir = os.path.dirname(hash_file)
if not os.path.exists(hash_file_dir):
    os.makedirs(hash_file_dir)

# Read the current now.md content and extract content below the front matter
now_content = read_file(now_page)
now_content_below_front_matter = get_content_below_front_matter(now_content)

# Calculate the hash of the current content below the front matter
current_hash = calculate_hash(now_content_below_front_matter)

# Read the stored hash
if os.path.exists(hash_file):
    stored_hash = read_file(hash_file).strip()
else:
    stored_hash = ""

# Check if the content has changed
if current_hash != stored_hash:
    # Get the current date
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Define the new archive filename
    archive_file_name = f"now-{date_str}.md"
    archive_file = os.path.join(archive_dir, archive_file_name)

    # Update the content for the archive
    updated_content = update_archive_content(now_content, date_str, archive_file_name)

    # Write the updated content to the archive file
    write_file(archive_file, updated_content)

    # Prepend the new entry to the then.md file
    prepend_to_then_md(date_str, archive_file_name)

    # Update the hash file with the new hash
    write_file(hash_file, current_hash)

    print(f"Archived current 'Now' page to {archive_file} and updated 'then.md'")

else:
    print("No changes detected in 'now.md'. No update required.")
