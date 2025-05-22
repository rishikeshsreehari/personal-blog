#!/usr/bin/env python3
import os
import re
import yaml
import sys
import requests
from datetime import datetime

def parse_frontmatter(file_path):
    """Parse the frontmatter and content from a markdown file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return None, content
    
    frontmatter = yaml.safe_load(match.group(1))
    content_text = match.group(2).strip()
    
    return frontmatter, content_text

def check_length(text, platform):
    """Check if text exceeds platform character limits."""
    limits = {
        'twitter': 280,
        'mastodon': 500,  # This varies by instance but 500 is common
        'bluesky': 300
    }
    
    if len(text) <= limits[platform]:
        return text, False
    
    # If too long, truncate and add a note
    truncated = text[:limits[platform] - 30] + "... [Full post on blog]"
    return truncated, True

def post_to_twitter(text):
    """Post text to Twitter using v2 API with requests."""
    text, was_truncated = check_length(text, 'twitter')
    if was_truncated:
        print("Note: Text was truncated for Twitter")
    
    try:
        # Prepare the OAuth 1.0a authentication
        from requests_oauthlib import OAuth1
        
        auth = OAuth1(
            os.environ['TWITTER_API_KEY'],
            os.environ['TWITTER_API_SECRET'],
            os.environ['TWITTER_ACCESS_TOKEN'],
            os.environ['TWITTER_ACCESS_SECRET']
        )
        
        # Prepare the request to the Twitter v2 API
        url = "https://api.twitter.com/2/tweets"
        payload = {"text": text}
        headers = {"Content-Type": "application/json"}
        
        # Make the request
        response = requests.post(url, json=payload, auth=auth, headers=headers)
        
        # Check if successful
        if response.status_code == 201:
            tweet_data = response.json()
            tweet_id = tweet_data.get('data', {}).get('id')
            print(f"Posted to Twitter: {text[:30]}...")
            return tweet_id
        else:
            print(f"Error posting to Twitter: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error posting to Twitter: {e}")
        return None

def post_to_mastodon(text):
    """Post text to Mastodon using requests."""
    text, was_truncated = check_length(text, 'mastodon')
    if was_truncated:
        print("Note: Text was truncated for Mastodon")
    
    try:
        # Prepare the request to the Mastodon API
        url = f"{os.environ['MASTODON_INSTANCE']}/api/v1/statuses"
        headers = {
            "Authorization": f"Bearer {os.environ['MASTODON_ACCESS_TOKEN']}",
            "Content-Type": "application/json"
        }
        payload = {"status": text}
        
        # Make the request
        response = requests.post(url, json=payload, headers=headers)
        
        # Check if successful
        if response.status_code == 200:
            status_data = response.json()
            status_id = status_data.get('id')
            print(f"Posted to Mastodon: {text[:30]}...")
            return status_id
        else:
            print(f"Error posting to Mastodon: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error posting to Mastodon: {e}")
        return None

def post_to_bluesky(text):
    """Post text to Bluesky using requests."""
    text, was_truncated = check_length(text, 'bluesky')
    if was_truncated:
        print("Note: Text was truncated for Bluesky")
    
    try:
        # First authenticate to get DID and JWT
        auth_url = "https://bsky.social/xrpc/com.atproto.server.createSession"
        auth_data = {
            "identifier": os.environ['BLUESKY_EMAIL'],
            "password": os.environ['BLUESKY_PASSWORD']
        }
        auth_response = requests.post(auth_url, json=auth_data)
        
        if auth_response.status_code != 200:
            print(f"Error authenticating with Bluesky: {auth_response.status_code} - {auth_response.text}")
            return None
        
        auth_result = auth_response.json()
        did = auth_result.get('did')
        jwt = auth_result.get('accessJwt')
        
        # Now create the post
        post_url = "https://bsky.social/xrpc/com.atproto.repo.createRecord"
        post_data = {
            "repo": did,
            "collection": "app.bsky.feed.post",
            "record": {
                "$type": "app.bsky.feed.post",
                "text": text,
                "createdAt": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        post_headers = {
            "Authorization": f"Bearer {jwt}",
            "Content-Type": "application/json"
        }
        
        post_response = requests.post(post_url, json=post_data, headers=post_headers)
        
        if post_response.status_code == 200:
            result = post_response.json()
            print(f"Posted to Bluesky: {text[:30]}...")
            return result.get('uri')
        else:
            print(f"Error posting to Bluesky: {post_response.status_code} - {post_response.text}")
            return None
            
    except Exception as e:
        print(f"Error posting to Bluesky: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python posse.py path/to/micro/post.md")
        return
    
    file_path = sys.argv[1]
    
    # Parse the post file
    frontmatter, content = parse_frontmatter(file_path)
    
    if not frontmatter or 'crosspost' not in frontmatter:
        print("No crosspost settings found in frontmatter.")
        return
    
    # Post to platforms based on frontmatter settings
    if frontmatter['crosspost'].get('twitter', False):
        try:
            post_to_twitter(content)
        except KeyError as e:
            print(f"Twitter credentials not found in environment variables: {e}")
        except Exception as e:
            print(f"Error posting to Twitter: {e}")
    
    if frontmatter['crosspost'].get('mastodon', False):
        try:
            post_to_mastodon(content)
        except KeyError as e:
            print(f"Mastodon credentials not found in environment variables: {e}")
        except Exception as e:
            print(f"Error posting to Mastodon: {e}")
    
    if frontmatter['crosspost'].get('bluesky', False):
        try:
            post_to_bluesky(content)
        except KeyError as e:
            print(f"Bluesky credentials not found in environment variables: {e}")
        except Exception as e:
            print(f"Error posting to Bluesky: {e}")

if __name__ == "__main__":
    main()