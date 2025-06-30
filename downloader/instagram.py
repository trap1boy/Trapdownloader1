# downloader/instagram.py

import requests

def download_instagram(url):
    try:
        api = f"https://saveinsta.net/api/instagram?url={url}"
        res = requests.get(api).json()
        if "media" in res and res["media"]:
            return {"title": "Instagram Post", "url": res["media"][0]}
        else:
            return {"error": "لینک معتبر نیست یا دانلود ممکن نیست."}
    except Exception as e:
        return {"error": str(e)}
