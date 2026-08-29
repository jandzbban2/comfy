import requests
import json

# Check huggingface files with exact search
res = requests.get("https://huggingface.co/api/models?search=abliterated&filter=text-generation")
print("HF models:")
for m in res.json()[:20]:
    print(m.get("id"))
