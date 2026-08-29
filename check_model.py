import os
import requests
import json

CIVITAI_URL = "https://civitai.com/api/v1/model-versions/3258954"
# Also test civitai.red or direct download URL
DOWNLOAD_URL = "https://civitai.red/api/download/models/3258954?fileId=3142504"
TOKEN = "8e728b6705b6a2650183d127a74a3644"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

print("Checking model version metadata...")
try:
    res = requests.get(f"https://civitai.com/api/v1/model-versions/3258954", headers=headers, timeout=10)
    if res.status_code == 200:
        data = res.json()
        print(f"Model Name: {data.get('model', {}).get('name')}")
        print(f"Model Type: {data.get('model', {}).get('type')}")
        print(f"Base Model: {data.get('baseModel')}")
        print(f"Files: {[f.get('name') for f in data.get('files', [])]}")
    else:
        print(f"Civitai API status: {res.status_code}")
except Exception as e:
    print(f"Error querying API: {e}")
