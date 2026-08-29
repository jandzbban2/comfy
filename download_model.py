import os
import re
import sys
import time
import requests

DOWNLOAD_URL = "https://civitai.red/api/download/models/3258954?fileId=3142504"
TOKEN = "8e728b6705b6a2650183d127a74a3644"

BASE_SHARED_MODELS = r"C:\Users\kubaz\AppData\Local\Comfy-Desktop\ComfyUI-Shared\models"
CHECKPOINTS_DIR = os.path.join(BASE_SHARED_MODELS, "checkpoints")
LORAS_DIR = os.path.join(BASE_SHARED_MODELS, "loras")

os.makedirs(CHECKPOINTS_DIR, exist_ok=True)
os.makedirs(LORAS_DIR, exist_ok=True)

filename = "museByStableYogi_v35Int8Extended.safetensors"
target_dir = CHECKPOINTS_DIR
target_filepath = os.path.join(target_dir, filename)

print(f"Target destination: {target_filepath}")

url_with_token = f"{DOWNLOAD_URL}&token={TOKEN}" if "?" in DOWNLOAD_URL else f"{DOWNLOAD_URL}?token={TOKEN}"

chunk_size = 10 * 1024 * 1024  # 10 MB chunks
max_retries = 25
retry_count = 0

while retry_count < max_retries:
    downloaded = 0
    if os.path.exists(target_filepath):
        downloaded = os.path.getsize(target_filepath)
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    if downloaded > 0:
        headers["Range"] = f"bytes={downloaded}-"
        print(f"Resuming download from byte {downloaded} ({downloaded / (1024*1024):.1f} MB)...")
    else:
        print("Starting fresh download...")

    try:
        response = requests.get(
            url_with_token,
            headers=headers,
            stream=True,
            allow_redirects=True,
            timeout=45
        )

        if response.status_code == 416:
            print("Range not satisfiable — file might already be complete!")
            break
        elif response.status_code not in (200, 206):
            print(f"Server returned HTTP {response.status_code}. Retrying in 5s...")
            time.sleep(5)
            retry_count += 1
            continue

        # Get total size
        content_range = response.headers.get("Content-Range")
        if content_range:
            total_size = int(content_range.split('/')[-1])
        else:
            total_size = downloaded + int(response.headers.get("content-length", 0))

        mode = "ab" if downloaded > 0 else "wb"
        with open(target_filepath, mode) as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"Progress: {percent:.1f}% ({downloaded / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB)", flush=True)
                    else:
                        print(f"Downloaded: {downloaded / (1024*1024):.1f} MB", flush=True)

        if total_size > 0 and downloaded >= total_size:
            print(f"\n[SUCCESS] Download completed! Total size: {downloaded / (1024*1024):.1f} MB")
            print(f"Model location: {target_filepath}")
            break

    except (requests.exceptions.RequestException, Exception) as e:
        print(f"Network glitch/timeout ({e}). Resuming in 4 seconds...")
        retry_count += 1
        time.sleep(4)

if not os.path.exists(target_filepath) or os.path.getsize(target_filepath) == 0:
    print("Download failed after maximum retries.")
    sys.exit(1)
