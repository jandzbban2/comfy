import json
import base64
import time
import os
import requests

# ==========================================
# CONFIGURATION
# ==========================================
_CONFIG = {}
if os.path.exists("runpod_config.json"):
    try:
        with open("runpod_config.json", "r", encoding="utf-8") as _f:
            _CONFIG = json.load(_f)
    except Exception:
        pass

RUNPOD_API_KEY = os.environ.get("RUNPOD_API_KEY") or _CONFIG.get("RUNPOD_API_KEY", "YOUR_RUNPOD_API_KEY_HERE")
ENDPOINT_ID = os.environ.get("ENDPOINT_ID") or _CONFIG.get("ENDPOINT_ID", "YOUR_ENDPOINT_ID_HERE")
WORKFLOW_FILE = "workflow_api.json"
OUTPUT_IMAGE_NAME = "generated_output.png"

# Base URL for RunPod Serverless
BASE_URL = f"https://api.runpod.ai/v2/{ENDPOINT_ID}"
HEADERS = {
    "Authorization": f"Bearer {RUNPOD_API_KEY}",
    "Content-Type": "application/json"
}

def load_workflow():
    if not os.path.exists(WORKFLOW_FILE):
        print(f"Error: {WORKFLOW_FILE} not found. Please place your exported API workflow in this folder.")
        return None
    with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def run_sync(workflow_data):
    """Executes workflow synchronously (blocks until image is generated)."""
    print("Sending synchronous request to RunPod...")
    url = f"{BASE_URL}/runsync"
    payload = {"input": {"workflow": workflow_data}}
    
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code != 200:
        print(f"HTTP Error {response.status_code}: {response.text}")
        return None
    return response.json()

def run_async_with_polling(workflow_data):
    """Executes workflow asynchronously and polls status until complete."""
    print("Submitting async job to RunPod...")
    url = f"{BASE_URL}/run"
    payload = {"input": {"workflow": workflow_data}}
    
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code != 200:
        print(f"HTTP Error {response.status_code}: {response.text}")
        return None
    
    job = response.json()
    job_id = job.get("id")
    print(f"Job submitted! Job ID: {job_id}")
    
    # Poll status
    status_url = f"{BASE_URL}/status/{job_id}"
    while True:
        status_res = requests.get(status_url, headers=HEADERS).json()
        status = status_res.get("status")
        print(f"Current Status: {status}")
        
        if status == "COMPLETED":
            return status_res
        elif status in ["FAILED", "CANCELLED"]:
            print(f"Job ended with status: {status}")
            print(status_res)
            return None
        
        time.sleep(3)

def save_output_image(result):
    if not result or "output" not in result:
        print("No output found in response.")
        return

    output_data = result["output"]
    images = output_data.get("images", [])
    
    if not images:
        print("No images returned in response.")
        return

    for idx, img_info in enumerate(images):
        file_name = f"output_{idx + 1}_{OUTPUT_IMAGE_NAME}"
        if img_info.get("type") == "base64":
            img_bytes = base64.b64decode(img_info["image"])
            with open(file_name, "wb") as f:
                f.write(img_bytes)
            print(f"Successfully saved image to: {os.path.abspath(file_name)}")
        elif "download_url" in img_info or "image" in img_info:
            img_url = img_info.get("download_url") or img_info.get("image")
            img_data = requests.get(img_url).content
            with open(file_name, "wb") as f:
                f.write(img_data)
            print(f"Successfully downloaded and saved image to: {os.path.abspath(file_name)}")

if __name__ == "__main__":
    print("=== RunPod ComfyUI Serverless Client ===")
    
    if RUNPOD_API_KEY == "YOUR_RUNPOD_API_KEY_HERE" or ENDPOINT_ID == "YOUR_ENDPOINT_ID_HERE":
        print("Please edit 'test_runpod.py' and fill in your RUNPOD_API_KEY and ENDPOINT_ID.")
        exit(1)
        
    workflow = load_workflow()
    if workflow:
        # Example: Modify seed or positive prompt dynamically before sending
        # workflow["6"]["inputs"]["text"] = "A magnificent fantasy castle on a mountain peak, digital art, 8k"
        
        res = run_async_with_polling(workflow)
        if res:
            save_output_image(res)
