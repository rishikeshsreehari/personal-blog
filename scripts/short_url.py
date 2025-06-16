import os
import yaml
import hashlib
import glob
import frontmatter
from pathlib import Path

def generate_short_code(url, length=6):
    """Generate consistent short code from URL hash"""
    hash_obj = hashlib.md5(url.encode())
    hash_hex = hash_obj.hexdigest()
    return hash_hex[:length]

def get_hugo_content(content_dir="content"):
    """Extract ALL content and their short URLs from Hugo content directory"""
    content_items = []
    
    if not os.path.exists(content_dir):
        print(f"Warning: Content directory {content_dir} not found")
        return content_items
    
    # Find all markdown files in all subdirectories
    for md_file in glob.glob(f"{content_dir}/**/*.md", recursive=True):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                
                # Skip if is draft
                if post.metadata.get('draft', False):
                    continue
                
                # Generate URL based on Hugo's default URL structure
                relative_path = Path(md_file).relative_to(content_dir)
                content_url = generate_hugo_url(relative_path, post.metadata)
                
                # Skip if no valid URL could be generated
                if not content_url:
                    continue
                
                # Check if custom shorturl exists in front matter
                custom_short = post.metadata.get('shorturl')
                
                # Determine content type from directory structure
                content_type = get_content_type(relative_path)
                
                content_items.append({
                    'content_url': content_url,
                    'custom_shorturl': custom_short,
                    'title': post.metadata.get('title', 'Untitled'),
                    'content_type': content_type,
                    'file_path': md_file
                })
                
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
    
    print(f"Found {len(content_items)} content items to process")
    return content_items

def generate_hugo_url(relative_path, metadata):
   """Generate Hugo URL based on file structure and front matter"""
   
   # FIRST: Check if there's a custom URL in front matter
   if 'url' in metadata:
       url = metadata['url']
       # Ensure it starts and ends with /
       if not url.startswith('/'):
           url = '/' + url
       if not url.endswith('/'):
           url = url + '/'
       return url
   
   # SECOND: Check if there's a slug in front matter
   if 'slug' in metadata:
       slug = metadata['slug']
       # For slugs, we still need to consider the directory structure
       if len(relative_path.parts) == 1:
           # Top-level file with slug
           return f"/{slug}/"
       else:
           # File in subdirectory with slug
           parent_dirs = '/'.join(relative_path.parts[:-1])
           return f"/{parent_dirs}/{slug}/"
   
   # Handle special files
   if relative_path.name in ['_index.md']:
       # _index.md files are section pages
       if len(relative_path.parts) == 1:
           # content/_index.md -> /
           return "/"
       else:
           # content/blog/_index.md -> /blog/
           return f"/{'/'.join(relative_path.parts[:-1])}/"
   
   # Handle index.md files (leaf bundles)
   if relative_path.name == 'index.md':
       # content/posts/my-post/index.md -> /posts/my-post/
       return f"/{'/'.join(relative_path.parts[:-1])}/"
   
   # Handle regular markdown files
   # content/posts/my-post.md -> /posts/my-post/
   # content/about.md -> /about/
   path_without_ext = relative_path.with_suffix('')
   return f"/{path_without_ext}/"


def get_content_type(relative_path):
    """Determine content type from file path"""
    parts = relative_path.parts
    
    if len(parts) == 1:
        return "page"  # Top-level pages like about.md
    
    return parts[0]  # posts, blog, docs, etc.

def load_existing_shorturls(data_file="data/shorturl.yaml"):
    """Load existing short URLs"""
    if not os.path.exists(data_file):
        print("No existing shorturl.yaml found, creating new one")
        return {}
    
    try:
        with open(data_file, 'r') as f:
            existing = yaml.safe_load(f) or []
        
        # Convert list to dict for easy lookup
        existing_dict = {item['content_url']: item for item in existing}
        print(f"Loaded {len(existing_dict)} existing short URLs")
        return existing_dict
    except Exception as e:
        print(f"Error loading existing shorturl.yaml: {e}")
        return {}

def update_shorturls(content_dir="content", data_file="data/shorturl.yaml"):
    """Main function to update short URLs with conflict detection"""
    
    content_items = get_hugo_content(content_dir)
    existing_shorturls = load_existing_shorturls(data_file)
    
    # First pass: detect all custom shorturl conflicts
    custom_short_map = {}
    conflicts = []
    
    for item in content_items:
        custom_short = item['custom_shorturl']
        if custom_short:
            if custom_short in custom_short_map:
                # Found a conflict!
                existing_conflict = next((c for c in conflicts if c['short_url'] == custom_short), None)
                if existing_conflict:
                    existing_conflict['files'].append(item)
                else:
                    conflicts.append({
                        'short_url': custom_short,
                        'files': [custom_short_map[custom_short], item]
                    })
            else:
                custom_short_map[custom_short] = item
    
    # If conflicts found, report and exit gracefully
    if conflicts:
        print(f"\n❌ CONFLICT DETECTED: {len(conflicts)} duplicate custom short URL(s) found!")
        print("\n🚨 The following short URLs are used multiple times:")
        
        for conflict in conflicts:
            short_url = conflict['short_url']
            files = conflict['files']
            print(f"\n   Short URL: /{short_url}")
            for file_info in files:
                print(f"     - '{file_info['title']}' ({file_info['content_url']})")
                print(f"       File: {file_info['file_path']}")
        
        print(f"\n💡 To fix this:")
        print(f"   1. Choose unique shorturl values in your front matter")
        print(f"   2. Or remove 'shorturl: {conflicts[0]['short_url']}' from one of the conflicting files")
        print(f"   3. Then run the build again")
        
        print(f"\n🛑 Build stopped. Please resolve conflicts before continuing.")
        
        # Return False to indicate failure - don't continue processing
        return False
    
    # Second pass: check for conflicts with existing auto-generated URLs
    auto_generated_conflicts = []
    for item in content_items:
        custom_short = item['custom_shorturl']
        content_url = item['content_url']
        
        if custom_short:
            # Check if custom short URL conflicts with existing auto-generated ones
            for existing_url, existing_data in existing_shorturls.items():
                if (existing_data['short_url'] == f"/{custom_short}" and 
                    existing_url != content_url and 
                    not existing_data.get('custom', False)):
                    
                    auto_generated_conflicts.append({
                        'short_url': custom_short,
                        'new_item': item,
                        'existing_item': existing_data
                    })
    
    # Report auto-generated conflicts
    if auto_generated_conflicts:
        print(f"\n⚠️  WARNING: {len(auto_generated_conflicts)} custom short URL(s) conflict with existing auto-generated ones:")
        
        for conflict in auto_generated_conflicts:
            short_url = conflict['short_url']
            new_item = conflict['new_item']
            existing_item = conflict['existing_item']
            
            print(f"\n   Short URL: /{short_url}")
            print(f"     NEW (custom): '{new_item['title']}' ({new_item['content_url']})")
            print(f"     EXISTING (auto): ({existing_item['content_url']})")
        
        print(f"\n💡 These conflicts will be resolved by:")
        print(f"   - Keeping your new custom short URLs")
        print(f"   - Auto-generating new short URLs for the existing content")
        
        user_input = input(f"\nContinue? (y/N): ").strip().lower()
        if user_input not in ['y', 'yes']:
            print("🛑 Build cancelled by user.")
            return False
    
    # Third pass: Process all items (no conflicts at this point)
    updated_shorturls = []
    changes_made = False
    used_short_urls = set()
    
    # Group by content type for better organization
    by_type = {}
    for item in content_items:
        content_type = item['content_type']
        if content_type not in by_type:
            by_type[content_type] = []
        by_type[content_type].append(item)
    
    print(f"\nProcessing content by type:")
    for content_type, items in by_type.items():
        print(f"  {content_type}: {len(items)} items")
    
    for item in content_items:
        content_url = item['content_url']
        custom_short = item['custom_shorturl']
        title = item['title']
        content_type = item['content_type']
        
        # Check if this content already has a short URL
        if content_url in existing_shorturls:
            existing_entry = existing_shorturls[content_url]
            
            # If custom shorturl changed in front matter, update it
            if custom_short and existing_entry['short_url'] != f"/{custom_short}":
                short_url = f"/{custom_short}"
                changes_made = True
                print(f"Updated custom short URL for [{content_type}] '{title}': /{custom_short}")
            elif not custom_short and existing_entry.get('custom', False):
                # Custom shorturl was removed from front matter
                short_url = f"/{generate_short_code(content_url)}"
                changes_made = True
                print(f"Reverted to auto-generated short URL for [{content_type}] '{title}': {short_url}")
            else:
                # No change needed
                short_url = existing_entry['short_url']
        else:
            # New content - create short URL
            changes_made = True
            if custom_short:
                short_url = f"/{custom_short}"
                print(f"New [{content_type}] with custom short URL '{title}': /{custom_short}")
            else:
                short_url = f"/{generate_short_code(content_url)}"
                print(f"New [{content_type}] with auto-generated short URL '{title}': {short_url}")
        
        # Handle conflicts with used URLs (should only be auto-generated at this point)
        if short_url in used_short_urls:
            if custom_short:
                # This shouldn't happen anymore due to our pre-checks
                print(f"ERROR: Unexpected custom short URL conflict: {short_url}")
                return False
            else:
                # Generate new code for auto-generated URLs
                counter = 1
                original_short = short_url
                while short_url in used_short_urls:
                    short_url = f"/{generate_short_code(content_url + str(counter))}"
                    counter += 1
                print(f"Resolved auto-generated duplicate: {original_short} -> {short_url} for [{content_type}] '{title}'")
                changes_made = True
        
        used_short_urls.add(short_url)
        
        updated_shorturls.append({
            'content_url': content_url,
            'short_url': short_url,
            'custom': bool(custom_short),
            'title': title,
            'content_type': content_type
        })
    
    # Sort by content type, then by URL for consistent output
    updated_shorturls.sort(key=lambda x: (x['content_type'], x['content_url']))
    
    # Only write if changes were made
    if changes_made:
        # Ensure data directory exists
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        
        with open(data_file, 'w') as f:
            yaml.dump(updated_shorturls, f, default_flow_style=False, sort_keys=False)
        
        print(f"✅ Updated shorturl.yaml with {len(updated_shorturls)} entries")
        return True
    else:
        print("ℹ️  No changes needed for short URLs")
        return True  # Changed from None to True for consistency

def print_summary(data_file="data/shorturl.yaml"):
    """Print a summary of current short URLs"""
    if not os.path.exists(data_file):
        print("No shorturl.yaml file found")
        return
    
    with open(data_file, 'r') as f:
        shorturls = yaml.safe_load(f) or []
    
    # Group by content type
    by_type = {}
    custom_count = 0
    
    for item in shorturls:
        content_type = item.get('content_type', 'unknown')
        if content_type not in by_type:
            by_type[content_type] = []
        by_type[content_type].append(item)
        
        if item.get('custom', False):
            custom_count += 1
    
    auto_count = len(shorturls) - custom_count
    
    print(f"\n📊 Short URL Summary:")
    print(f"   Total: {len(shorturls)}")
    print(f"   Custom: {custom_count}")
    print(f"   Auto-generated: {auto_count}")
    
    print(f"\n📁 By Content Type:")
    for content_type, items in sorted(by_type.items()):
        custom_in_type = sum(1 for item in items if item.get('custom', False))
        print(f"   {content_type}: {len(items)} total ({custom_in_type} custom)")
    
    # Show examples if not too many
    if len(shorturls) <= 15:
        print(f"\n📝 All Short URLs:")
        current_type = None
        for item in shorturls:
            if item['content_type'] != current_type:
                current_type = item['content_type']
                print(f"\n  [{current_type.upper()}]")
            
            custom_flag = " (custom)" if item.get('custom', False) else ""
            print(f"    {item['short_url']} -> {item['content_url']}{custom_flag}")

if __name__ == "__main__":
    # You can customize these paths
    CONTENT_DIR = "content"
    DATA_FILE = "data/shorturl.yaml"
    
    print("🔗 Generating short URLs for ALL Hugo content...")
    
    try:
        result = update_shorturls(CONTENT_DIR, DATA_FILE)
        
        if result is False:
            # Conflicts detected - don't show summary
            print(f"\n❌ Short URL generation failed due to conflicts.")
            print(f"📋 Current data preserved at {DATA_FILE}")
            exit(1)
        elif result is True:
            # Success (either changes made or no changes needed)
            print_summary(DATA_FILE)
            print(f"\n✅ shorturl.yaml processing completed at {DATA_FILE}")
        else:
            # This shouldn't happen now
            print(f"⚠️ Unexpected result: {result}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)