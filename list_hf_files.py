import requests

res = requests.get("https://huggingface.co/api/models/Comfy-Org/Krea-2/tree/main")
if res.status_code == 200:
    for item in res.json():
        print(item.get("path"))
else:
    print("Status:", res.status_code)
    # search other Krea repos
    res2 = requests.get("https://huggingface.co/api/models?search=krea-2")
    if res2.status_code == 200:
        for m in res2.json():
            print("Found repo:", m.get("id"))
