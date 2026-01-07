import json
import os
import datetime
import subprocess
import uuid

# Configuration
DATA_FILE = "data.json"
DOWNLOADS_DIR = "downloads"
ICONS_DIR = "icons"

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        return False

def get_input(prompt, default=None):
    text = input(f"{prompt} " + (f"[{default}]: " if default else ": "))
    return text.strip() or default

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_app():
    print("\n--- ADD NEW APP ---")
    
    # 1. Get Details
    name = get_input("App Name")
    if not name: return
    
    version = get_input("Version", "1.0")
    category = get_input("Category", "Utility")
    description = get_input("Description")
    
    # 2. File Handling
    print(f"\nEnsure your App file is in the '{DOWNLOADS_DIR}' folder.")
    print(f"Ensure your Icon is in the '{ICONS_DIR}' folder (optional).")
    
    file_name = get_input("Filename (e.g. app.zip)")
    
    # Verify file exists locally
    if not os.path.exists(f"{DOWNLOADS_DIR}/{file_name}"):
        print(f"WARNING: Could not find '{DOWNLOADS_DIR}/{file_name}' locally.")
        print("Make sure you copied it correctly with 'cp'. Continuing anyway...")
    
    icon_name = get_input("Icon Filename (e.g. icon.png)", "")
    
    # 3. Update JSON
    apps = load_data()
    
    new_app = {
        "id": str(uuid.uuid4()),
        "name": name,
        "version": version,
        "category": category,
        "description": description,
        "downloadUrl": f"{DOWNLOADS_DIR}/{file_name}",
        "iconUrl": f"{ICONS_DIR}/{icon_name}" if icon_name else "https://via.placeholder.com/64",
        "date": datetime.datetime.now().isoformat()
    }
    
    apps.append(new_app)
    save_data(apps)
    print("\n[SUCCESS] data.json updated!")
    
    # 4. Git Push
    if get_input("\nPush to GitHub now? (y/n)", "y").lower() == 'y':
        print("\n--- GITHUB SYNC ---")
        run_command("git add .")
        run_command(f'git commit -m "Add app: {name}"')
        print("Pushing... (You may need to enter your PAT password)")
        run_command("git push")

def main():
    if not os.path.exists(DOWNLOADS_DIR): os.makedirs(DOWNLOADS_DIR)
    if not os.path.exists(ICONS_DIR): os.makedirs(ICONS_DIR)
    
    while True:
        print("\n=== VANTAL STORE MANAGER ===")
        print("1. Add New App")
        print("2. Sync/Push Changes")
        print("3. Exit")
        
        choice = input("Select: ")
        
        if choice == '1':
            add_app()
        elif choice == '2':
            run_command("git add .")
            run_command('git commit -m "Manual sync"')
            run_command("git push")
        elif choice == '3':
            break

if __name__ == "__main__":
    main()


