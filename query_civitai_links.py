import requests
import json
import re

headers = {"Authorization": "Bearer 8e728b6705b6a2650183d127a74a3644"}
res = requests.get("https://civitai.com/api/v1/models/2741166", headers=headers)
if res.status_code == 200:
    data = res.json()
    desc = data.get("description", "")
    urls = re.findall(r'https?://[^\s<>"\']+', desc)
    with open("civitai_links.txt", "w", encoding="utf-8") as f:
        f.write("Model description links:\n")
        for u in urls:
            f.write(u + "\n")
        f.write("\nModel Versions:\n")
        for v in data.get("modelVersions", []):
            f.write(f"Version: {v.get('name')} (ID: {v.get('id')})\n")
            f.write(f"Description: {v.get('description')}\n")
            vurls = re.findall(r'https?://[^\s<>"\']+', str(v))
            for vu in vurls:
                f.write("  " + vu + "\n")
    print("Links written to civitai_links.txt")
