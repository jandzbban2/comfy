import requests

res = requests.get("https://api.github.com/repos/Stable-yogi/sd-forge-krea2/contents/scripts")
if res.status_code == 200:
    for item in res.json():
        print(item.get("name"), item.get("download_url"))
        if "download" in item.get("name").lower() or "ui" in item.get("name").lower():
            # fetch code
            code_res = requests.get(item.get("download_url"))
            with open("forge_krea_script.py", "w", encoding="utf-8") as f:
                f.write(code_res.text)
            print("Saved", item.get("name"))
