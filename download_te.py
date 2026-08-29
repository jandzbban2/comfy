import os
import sys
import time
import requests

HF_TE_URL = "https://huggingface.co/Comfy-Org/Krea-2/resolve/main/text_encoders/qwen3vl_4b_fp8_scaled.safetensors"

BASE_SHARED_MODELS = r"C:\Users\kubaz\AppData\Local\Comfy-Desktop\ComfyUI-Shared\models"
TE_DIR = os.path.join(BASE_SHARED_MODELS, "text_encoders")
os.makedirs(TE_DIR, exist_ok=True)

# Save as the exact requested name
primary_filepath = os.path.join(TE_DIR, "qwen3vl-4b-abliterated_fp8_e4m3fn.safetensors")
alias_filepath = os.path.join(TE_DIR, "qwen3vl_4b_fp8_scaled.safetensors")

print(f"Target text encoder destination: {primary_filepath}")

chunk_size = 10 * 1024 * 1024  # 10 MB chunks
max_retries = 25
retry_count = 0

while retry_count < max_retries:
    downloaded = 0
    if os.path.exists(primary_filepath):
        downloaded = os.path.getsize(primary_filepath)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    if downloaded > 0:
        headers["Range"] = f"bytes={downloaded}-"
        print(f"Resuming download from byte {downloaded} ({downloaded / (1024*1024):.1f} MB)...")
    else:
        print(f"Connecting to Hugging Face ({HF_TE_URL})...")

    try:
        response = requests.get(
            HF_TE_URL,
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

        content_range = response.headers.get("Content-Range")
        if content_range:
            total_size = int(content_range.split('/')[-1])
        else:
            total_size = downloaded + int(response.headers.get("content-length", 0))

        mode = "ab" if downloaded > 0 else "wb"
        with open(primary_filepath, mode) as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"Progress: {percent:.1f}% ({downloaded / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB)", flush=True)

        if total_size > 0 and downloaded >= total_size:
            print(f"\n[SUCCESS] Download completed! Total size: {downloaded / (1024*1024):.1f} MB")
            print(f"Saved to: {primary_filepath}")
            
            # Also copy / create alias so standard workflows recognize it immediately
            try:
                import shutil
                if not os.path.exists(alias_filepath):
                    shutil.copyfile(primary_filepath, alias_filepath)
                    print(f"Created alias: {alias_filepath}")
            except Exception as ex:
                print(f"Note: Could not copy alias ({ex})")
            break

    except Exception as e:
        print(f"Network timeout ({e}). Resuming in 4s...")
        retry_count += 1
        time.sleep(4)

if not os.path.exists(primary_filepath) or os.path.getsize(primary_filepath) == 0:
    print("Download failed.")
    sys.exit(1)
