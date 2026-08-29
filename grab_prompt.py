import urllib.request
import json
import time
import os

COMFY_URL = "http://127.0.0.1:8188"
OUTPUT_FILE = "workflow_api.json"

def fetch_latest_prompt():
    try:
        req = urllib.request.Request(f"{COMFY_URL}/history")
        with urllib.request.urlopen(req, timeout=5) as response:
            history = json.loads(response.read().decode())
            if not history:
                return None
            # Get the most recent prompt in history
            latest_id = list(history.keys())[-1]
            prompt_data = history[latest_id].get("prompt", {})
            if prompt_data and len(prompt_data) >= 3:
                # ComfyUI history format is: [number, prompt_dict, extra_data, outputs]
                return prompt_data[2] if isinstance(prompt_data, list) and len(prompt_data) > 2 else prompt_data
    except Exception as e:
        print(f"Error connecting to ComfyUI: {e}")
    return None

if __name__ == "__main__":
    print("=== ComfyUI Prompt Auto-Capturer ===")
    print("Checking local ComfyUI history...")
    
    prompt = fetch_latest_prompt()
    if prompt:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(prompt, f, indent=2)
        print(f"[SUCCESS] Captured latest prompt from ComfyUI and saved to: {os.path.abspath(OUTPUT_FILE)}")
    else:
        print("No recent prompt found in history yet.")
        print("Please click 'Queue Prompt' in ComfyUI Desktop, then run this script again!")
