import requests

# Check Stable Yogi files or search HF for qwen3vl-4b-abliterated
res = requests.get("https://huggingface.co/api/models?search=qwen3vl-4b-abliterated")
print("Search qwen3vl-4b-abliterated:")
for m in res.json():
    print(" -", m.get("id"))

res2 = requests.get("https://huggingface.co/api/models?search=abliterated")
print("\nSearch abliterated (Krea/Qwen):")
for m in res2.json()[:15]:
    if "qwen" in m.get("id").lower() or "krea" in m.get("id").lower():
        print(" -", m.get("id"))
