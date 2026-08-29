import requests

res = requests.get("https://huggingface.co/api/models?search=qwen3vl")
if res.status_code == 200:
    for m in res.json():
        print(m.get("id"))

print("--- Searching qwen3-vl ---")
res2 = requests.get("https://huggingface.co/api/models?search=qwen3-vl")
if res2.status_code == 200:
    for m in res2.json()[:10]:
        print(m.get("id"))
