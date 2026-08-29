import requests
import re

headers = {"Authorization": "Bearer 8e728b6705b6a2650183d127a74a3644"}
res = requests.get("https://civitai.com/api/v1/articles/32010", headers=headers)
if res.status_code == 200:
    data = res.json()
    content = data.get("content", "")
    urls = re.findall(r'https?://[^\s<>"\']+', content)
    with open("article_links.txt", "w", encoding="utf-8") as f:
        f.write("Article links:\n")
        for u in urls:
            f.write(u + "\n")
        f.write("\nContent preview:\n" + content[:3000])
    print("Article saved")
else:
    print(f"Article fetch status: {res.status_code}")
