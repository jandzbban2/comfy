import requests

res_te = requests.get("https://huggingface.co/api/models/Comfy-Org/Krea-2/tree/main/text_encoders")
print("Text Encoders:")
for item in res_te.json():
    print(" -", item.get("path"), item.get("size"))

res_vae = requests.get("https://huggingface.co/api/models/Comfy-Org/Krea-2/tree/main/vae")
print("\nVAE:")
for item in res_vae.json():
    print(" -", item.get("path"), item.get("size"))
