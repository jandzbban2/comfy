import os
import sys
import requests

VAE_URL = "https://huggingface.co/Comfy-Org/Krea-2/resolve/main/vae/qwen_image_vae.safetensors"

BASE_SHARED_MODELS = r"C:\Users\kubaz\AppData\Local\Comfy-Desktop\ComfyUI-Shared\models"
VAE_DIR = os.path.join(BASE_SHARED_MODELS, "vae")
os.makedirs(VAE_DIR, exist_ok=True)

target_filepath = os.path.join(VAE_DIR, "qwen_image_vae.safetensors")
print(f"Downloading VAE to: {target_filepath}")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(VAE_URL, headers=headers, stream=True, allow_redirects=True, timeout=30)

if response.status_code != 200:
    print(f"Failed to initiate download. Status code: {response.status_code}")
    sys.exit(1)

total_size = int(response.headers.get("content-length", 0))
downloaded = 0
chunk_size = 5 * 1024 * 1024  # 5 MB chunks

with open(target_filepath, "wb") as f:
    for chunk in response.iter_content(chunk_size=chunk_size):
        if chunk:
            f.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                print(f"Progress: {percent:.1f}% ({downloaded / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB)", flush=True)

print(f"\n[SUCCESS] VAE downloaded successfully: {target_filepath}")
