import os
import hashlib
from datetime import datetime
import re

# Define paths
now_page = "content/now.md"
archive_dir = "content/now-archive"
current_page = os.path.join(archive_dir, "current.md")
archive_page = "content/then.md"
hash_file = os.path.join(archive_dir, "now_hash.txt")

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

def calculate_hash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def get_content_without_frontmatter_and_shortcodes(content):
    # Remove frontmatter
    content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
    
    # Remove shortcodes
    content = re.sub(r'{{<.*?>}}', '', content)
    content = re.sub(r'{{% .*?%}}', '', content)
    
    return content.strip()

def update_archive_content(content, date_str):
    frontmatter = f"""---
title: "What I'm Doing Now"
url: "/now-{date_str}"
summary: single
type: page
disable_comments: true
ShowReadingTime: false
dataDir: "data"
index: false
hideFromRSS: true
---

This is an archive of the Now page on {date_str}

"""
    return frontmatter + content

def prepend_to_then_md(archive_url):
    date_str = archive_url.split('-', 1)[1]  # Extract date from archive_url
    new_entry = f"[{date_str}](/{archive_url})\n\n"
    if os.path.exists(archive_page):
        existing_content = read_file(archive_page)
        parts = existing_content.split('### Archives\n', 1)
        if len(parts) == 2:
            prelude, archives = parts
            updated_content = f"{prelude}### Archives\n{new_entry}{archives}"
        else:
            updated_content = f"{existing_content}\n{new_entry}"
    else:
        updated_content = f'''Idea stolen from [Matthew Smith](https://matthewsmith.website/then)

This is an archive of all of my "Now" pages. This is mostly for myself—as I suspect it'll be nice to reflect on down the road—but you may very well find it interesting too!

### Archives
{new_entry}'''
    write_file(archive_page, updated_content)

def add_draft_frontmatter(content):
    frontmatter = """---
draft: true
---

"""
    return frontmatter + content

def get_unique_archive_filename(base_filename):
    counter = 1
    new_filename = base_filename
    while os.path.exists(new_filename):
        name, ext = os.path.splitext(base_filename)
        new_filename = f"{name}-{counter}{ext}"
        counter += 1
    return new_filename

# Ensure necessary directories exist
os.makedirs(archive_dir, exist_ok=True)

# Read the current now.md content
now_content = read_file(now_page)
now_content_clean = get_content_without_frontmatter_and_shortcodes(now_content)

# Calculate the hash of the cleaned current content
current_hash = calculate_hash(now_content_clean)

# Read the stored hash
stored_hash = read_file(hash_file).strip() if os.path.exists(hash_file) else ""

# Check if the content has changed
if current_hash != stored_hash:
    date_str = datetime.now().strftime("%Y-%m-%d")
    archive_file = None  # Initialize archive_file
    
    # If current.md exists, archive it
    if os.path.exists(current_page):
        archived_content = read_file(current_page)
        archived_content_clean = get_content_without_frontmatter_and_shortcodes(archived_content)
        base_archive_file_name = f"now-{date_str}.md"
        base_archive_file = os.path.join(archive_dir, base_archive_file_name)
        archive_file = get_unique_archive_filename(base_archive_file)
        archived_content = update_archive_content(archived_content_clean, date_str)
        write_file(archive_file, archived_content)
        
        # Update the URL in the archived content to match the potentially new filename
        archive_url = os.path.splitext(os.path.basename(archive_file))[0]
        archived_content = archived_content.replace(f'url: "/now-{date_str}"', f'url: "/{archive_url}"')
        write_file(archive_file, archived_content)
        
        prepend_to_then_md(archive_url)
    
    # Create/update current.md with new content and draft frontmatter
    current_content_with_draft = add_draft_frontmatter(now_content_clean)
    write_file(current_page, current_content_with_draft)
    
    # Update the hash file
    write_file(hash_file, current_hash)
    
    if archive_file:
        print(f"Archived previous 'Now' page to {archive_file}, updated 'current.md', and updated 'then.md'")
    else:
        print("Updated 'current.md' and 'then.md'. No previous version to archive.")
else:
    print("No changes detected in 'now.md'. No update required.")