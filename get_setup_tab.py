import requests

res = requests.get("https://raw.githubusercontent.com/Stable-yogi/sd-forge-krea2/main/scripts/krea2_setup_tab.py")
if res.status_code == 200:
    with open("krea2_setup_tab.py", "w", encoding="utf-8") as f:
        f.write(res.text)
    print("Fetched krea2_setup_tab.py successfully")
