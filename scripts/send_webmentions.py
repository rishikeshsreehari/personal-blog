import os
import json
import re
import requests
from pathlib import Path
import frontmatter
from urllib.parse import urlparse
from datetime import datetime

# Folders to process for webmentions
WEBMENTION_FOLDERS = [
    'content/blog',
    'content/journal', 
    'content/meet',
    'content/til'
]

# Domains to exclude from webmention sending
EXCLUDED_DOMAINS = {
    'google.com',
    'wikipedia.org', 'en.wikipedia.org',
    'geni.us',
    'youtube.com', 'youtu.be',
    'amazon.com', 'amazon.in',
    'github.com',
    'twitter.com', 'x.com',
    'facebook.com',
    'instagram.com',
    'linkedin.com',
    'reddit.com',
    'strava.com',  
    'web.archive.org',  
    'emojikeyboard.org',  
    'metmuseum.org',  
    'news.ycombinator.com',  
    'substack.com',
    'letterboxd.com',
    'porkbun.com',
    'cloudflare.com',
    'pages.cloudflare.com',
    'code.visualstudio.com',
    'obsidian.md',
    'htmx.org',
    'gohugo.io',
    'zerodha.com'
}

# Status codes that should be retried (temporary failures)
RETRYABLE_STATUSES = {
    'network_error',
    'http_429',  # Rate limit
    'http_500', 'http_502', 'http_503', 'http_504',  # Server errors
    'timeout',
    'connection_error',
    'unknown_error'
}

# Status codes that should NOT be retried (permanent failures)
PERMANENT_FAILURE_STATUSES = {
    'not_supported',
    'no_webmention_endpoint',
    'invalid_target',
    'forbidden',
    'http_404',
    'http_410',
    'no_link_found'# Does not recheck cases where link was not found at source
}

def load_sent_webmentions():
    """Load previously sent webmentions tracking file"""
    try:
        with open('data/sent-webmentions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_sent_webmentions(sent_data):
    """Save sent webmentions tracking file"""
    os.makedirs('data', exist_ok=True)
    with open('data/sent-webmentions.json', 'w') as f:
        json.dump(sent_data, f, indent=2)

def is_domain_excluded(url):
    """Check if a domain should be excluded from webmention sending"""
    try:
        domain = urlparse(url).netloc.lower()
        # Remove www. prefix for comparison
        if domain.startswith('www.'):
            domain = domain[4:]
        
        return domain in EXCLUDED_DOMAINS
    except:
        return False

def extract_links_from_content(content):
    """Extract external links from markdown content"""
    # Find markdown links: [text](url)
    md_links = re.findall(r'\[.*?\]\((https?://[^\)]+)\)', content)
    # Find HTML links: href="url"
    html_links = re.findall(r'href=["\']https?://([^"\']+)["\']', content)
    
    all_links = md_links + ['https://' + link for link in html_links if not link.startswith('//')]
    
    # Filter out your own domain and excluded domains
    external_links = []
    for link in all_links:
        try:
            domain = urlparse(link).netloc.lower()
            # Remove www. prefix for comparison
            if domain.startswith('www.'):
                clean_domain = domain[4:]
            else:
                clean_domain = domain
                
            # Check exclusions using the clean domain
            if (domain and 
                domain != "rishikeshs.com" and 
                clean_domain not in EXCLUDED_DOMAINS and
                domain not in EXCLUDED_DOMAINS):
                
                # Fix broken URLs that Hugo generates (double ? issue)
                # Replace ?parameter?utm_source with ?parameter&utm_source
                fixed_link = re.sub(r'\?([^?]+)\?utm_source=', r'?\1&utm_source=', link)
                
                # If no utm_source exists, add it properly
                if 'utm_source=rishikeshs.com' not in fixed_link:
                    if '?' in fixed_link:
                        fixed_link = f"{fixed_link}&utm_source=rishikeshs.com"
                    else:
                        fixed_link = f"{fixed_link}?utm_source=rishikeshs.com"
                
                external_links.append(fixed_link)
                
        except Exception as e:
            print(f"Error processing link {link}: {e}")
            continue
    
    return list(set(external_links))

def get_post_url(post_path, post_metadata, base_url):
    """Generate the correct URL for a post"""
    
    # First check if there's a custom URL in frontmatter
    if 'url' in post_metadata:
        url = post_metadata['url']
        # Ensure it starts with base_url
        if url.startswith('/'):
            return f"{base_url}{url}"
        elif url.startswith('http'):
            return url
        else:
            return f"{base_url}/{url}/"
    
    # Then check if there's a slug in frontmatter
    if 'slug' in post_metadata:
        return f"{base_url}/{post_metadata['slug']}/"
    
    # For index.md files, use the parent directory name
    if post_path.name == 'index.md':
        slug = post_path.parent.name
    else:
        slug = post_path.stem
    
    return f"{base_url}/{slug}/"

def get_tracking_key(post_path, post_metadata):
    """Generate a unique tracking key for this post"""
    
    # First check if there's a custom URL in frontmatter
    if 'url' in post_metadata:
        url = post_metadata['url']
        # Extract the path part and clean it up for use as a key
        if url.startswith('/'):
            return url.strip('/').replace('/', '-')
        elif url.startswith('http'):
            path = urlparse(url).path
            return path.strip('/').replace('/', '-')
        else:
            return url.replace('/', '-')
    
    # Then check if there's a slug in frontmatter
    if 'slug' in post_metadata:
        return post_metadata['slug']
    
    # For index.md files, use the parent directory name
    if post_path.name == 'index.md':
        return post_path.parent.name
    else:
        return post_path.stem

def should_skip_webmention(tracking_data, target_url):
    """Check if we should skip sending webmention based on previous attempts"""
    if not tracking_data:
        return False
    
    # Skip if already successful
    if target_url in tracking_data.get('successful', []):
        return True
    
    # Check failed attempts
    failed_attempts = tracking_data.get('failed', [])
    for failed in failed_attempts:
        if failed['url'] == target_url:
            status = failed.get('status', 'unknown_error')
            
            # Skip only permanent failures
            if status in PERMANENT_FAILURE_STATUSES:
                print(f"    Skipping {target_url} - permanent failure: {status}")
                return True
            
            # For retryable statuses, check if we should retry based on time
            if status in RETRYABLE_STATUSES:
                last_attempt = failed.get('last_attempt')
                if last_attempt:
                    try:
                        last_time = datetime.fromisoformat(last_attempt.replace('Z', '+00:00'))
                        hours_since = (datetime.now(last_time.tzinfo) - last_time).total_seconds() / 3600
                        
                        # Retry after 24 hours for retryable failures
                        if hours_since < 24:
                            print(f"    Skipping {target_url} - retrying too soon ({hours_since:.1f}h ago)")
                            return True
                        else:
                            print(f"    Will retry {target_url} - last attempt {hours_since:.1f}h ago")
                            return False
                    except:
                        # If we can't parse the time, allow retry
                        return False
    
    return False

def save_webmention_result(sent_webmentions, tracking_key, target_url, success, status=None, error=None):
    """Save webmention result with status tracking"""
    if tracking_key not in sent_webmentions:
        sent_webmentions[tracking_key] = {"successful": [], "failed": []}
    
    if success:
        # Add to successful list if not already there
        if target_url not in sent_webmentions[tracking_key]["successful"]:
            sent_webmentions[tracking_key]["successful"].append(target_url)
        
        # Remove from failed list if it was there
        sent_webmentions[tracking_key]["failed"] = [
            f for f in sent_webmentions[tracking_key].get("failed", []) 
            if f['url'] != target_url
        ]
    else:
        # Add to failed list with details
        failed_entry = {
            "url": target_url,
            "status": status or "unknown_error",
            "error": error,
            "last_attempt": datetime.utcnow().isoformat() + "Z"
        }
        
        # Remove any existing failed entry for this URL
        sent_webmentions[tracking_key]["failed"] = [
            f for f in sent_webmentions[tracking_key].get("failed", []) 
            if f['url'] != target_url
        ]
        
        # Add the new failed entry
        sent_webmentions[tracking_key]["failed"].append(failed_entry)

def send_webmention(source_url, target_url, dry_run=True):
    """Send a webmention using Telegraph"""
    if dry_run:
        print(f"DRY RUN: Would send webmention {source_url} -> {target_url}")
        return True, "queued", None
    
    token = os.environ.get('TELEGRAPH_TOKEN')
    if not token:
        print("Error: TELEGRAPH_TOKEN environment variable not set")
        return False, "no_token", "TELEGRAPH_TOKEN environment variable not set"
    
    endpoint = "https://telegraph.p3k.io/webmention"
    data = {
        'token': token,
        'source': source_url,
        'target': target_url
    }
    
    try:
        response = requests.post(endpoint, data=data, timeout=30)
        
        # Telegraph returns 201 for successful queueing
        success = response.status_code == 201
        
        if success:
            result = response.json()
            status = result.get('status', 'queued')
            print(f"Webmention queued: {source_url} -> {target_url}")
            print(f"  Status: {status}")
            if 'location' in result:
                print(f"  Track at: {result['location']}")
            return True, status, None
        else:
            try:
                error_info = response.json()
                error_status = error_info.get('error', 'unknown_error')
                error_description = error_info.get('error_description', 'no description')
                
                print(f"Webmention failed ({response.status_code}): {source_url} -> {target_url}")
                print(f"  Error: {error_status}")
                print(f"  Description: {error_description}")
                
                return False, error_status, error_description
            except:
                print(f"Webmention failed ({response.status_code}): {source_url} -> {target_url}")
                print(f"  Response: {response.text}")
                return False, f"http_{response.status_code}", response.text
        
    except requests.Timeout:
        print(f"Webmention timeout: {source_url} -> {target_url}")
        return False, "timeout", "Request timed out"
    except requests.ConnectionError as e:
        print(f"Connection error sending webmention: {e}")
        return False, "connection_error", str(e)
    except requests.RequestException as e:
        print(f"Error sending webmention: {e}")
        return False, "network_error", str(e)

def process_webmentions(dry_run=True):
    """Process posts in specified folders and send webmentions for new links"""
    sent_webmentions = load_sent_webmentions()
    base_url = "https://rishikeshs.com"
    
    # Find all markdown files in specified folders
    all_posts = []
    for folder in WEBMENTION_FOLDERS:
        folder_path = Path(folder)
        if folder_path.exists():
            posts = list(folder_path.rglob('*.md'))
            all_posts.extend(posts)
            print(f"Found {len(posts)} files in {folder}")
        else:
            print(f"Folder not found: {folder}")
    
    print(f"\nTotal: {len(all_posts)} markdown files to process")
    print(f"Retryable statuses: {', '.join(sorted(RETRYABLE_STATUSES))}")
    print(f"Permanent failure statuses: {', '.join(sorted(PERMANENT_FAILURE_STATUSES))}")
    
    total_links = 0
    total_sent = 0
    total_skipped = 0
    total_retries = 0
    
    for post_path in all_posts:
        try:
            # Parse frontmatter and content
            with open(post_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            # Skip drafts
            if post.metadata.get('draft', False):
                print(f"Skipping draft: {post_path}")
                continue
            
            # Get correct URL and tracking key for this post
            post_url = get_post_url(post_path, post.metadata, base_url)
            tracking_key = get_tracking_key(post_path, post.metadata)
            
            print(f"\nProcessing: {post_path}")
            print(f"Post URL: {post_url}")
            print(f"Tracking key: {tracking_key}")
            
            # Extract links from content (WITH UTM parameters)
            links = extract_links_from_content(post.content)
            total_links += len(links)
            
            print(f"Found {len(links)} webmention-worthy external links")
            
            if links:
                for link in links[:3]:  # Show first 3 links
                    print(f"  - {link}")
                if len(links) > 3:
                    print(f"  ... and {len(links) - 3} more")
            
            # Get tracking data for this post
            tracking_data = sent_webmentions.get(tracking_key, {})
            
            # Filter out links we should skip
            new_links = []
            skipped_count = 0
            retry_count = 0
            
            for link in links:
                if should_skip_webmention(tracking_data, link):
                    skipped_count += 1
                    total_skipped += 1
                else:
                    new_links.append(link)
                    # Check if this is a retry
                    failed_attempts = tracking_data.get('failed', [])
                    for failed in failed_attempts:
                        if failed['url'] == link and failed.get('status') in RETRYABLE_STATUSES:
                            retry_count += 1
                            total_retries += 1
                            break
            
            print(f"Skipped: {skipped_count}, New: {len(new_links) - retry_count}, Retries: {retry_count}")
            
            # Send webmentions for new links
            for link in new_links:
                success, status, error = send_webmention(post_url, link, dry_run)
                
                if not dry_run:
                    save_webmention_result(sent_webmentions, tracking_key, link, success, status, error)
                
                if success:
                    total_sent += 1
        
        except Exception as e:
            print(f"Error processing {post_path}: {e}")
            continue
    
    # Save updated tracking
    if not dry_run:
        save_sent_webmentions(sent_webmentions)
        print(f"\nUpdated sent-webmentions.json")
    
    print(f"\nSummary:")
    print(f"  Found {total_links} webmention-worthy links")
    print(f"  Sent {total_sent} new webmentions")
    print(f"  Retried {total_retries} previously failed webmentions")
    print(f"  Skipped {total_skipped} (already processed or permanent failures)")

if __name__ == "__main__":
    # Run in dry-run mode by default
    process_webmentions(dry_run=False)