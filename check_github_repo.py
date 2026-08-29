import requests

res = requests.get("https://api.github.com/repos/Stable-yogi/sd-forge-krea2/contents")
if res.status_code == 200:
    for item in res.json():
        print(item.get("name"), item.get("download_url"))
