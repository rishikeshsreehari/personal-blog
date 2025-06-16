import subprocess

def run_script(script_path):
    try:
        subprocess.run(['python', script_path], check=True)
        print(f"Successfully ran {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")
        raise

if __name__ == "__main__":
    scripts = [
        'scripts/short_url.py',  # Script will crash if there are conflicting short URLs
        'scripts/count_books.py',
        #'scripts/create_worldmap.py', #Disabled because travel page not yet set
        'scripts/then.py',
        'scripts/fetch_webmentions.py',
        'scripts/send_webmentions.py'
    ]
    
    for script in scripts:
        run_script(script)
