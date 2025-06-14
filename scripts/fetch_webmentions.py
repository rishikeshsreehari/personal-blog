import requests
import json
import os
from datetime import datetime

def fetch_webmentions():
    token = "Avvm8D7g2oQiIyTuhULo_g"
    api_url = f"https://webmention.io/api/mentions.jf2?token={token}&per-page=1000"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        
        webmentions = response.json()
        
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        # Save to data/webmentions.json
        with open('data/webmentions.json', 'w') as f:
            json.dump(webmentions, f, indent=2)
        
        print(f"Fetched {len(webmentions.get('children', []))} webmentions")
        
    except requests.RequestException as e:
        print(f"Error fetching webmentions: {e}")
        # Create empty file if fetch fails so build doesn't break
        with open('data/webmentions.json', 'w') as f:
            json.dump({"children": []}, f)

if __name__ == "__main__":
    fetch_webmentions()