# downloader/tiktok.py

import requests

def download_tiktok(url):
    try:
        api = f"https://api.tikmate.app/api/lookup?url={url}"
        res = requests.get(api).json()
        if "video" in res:
            return {"title": "TikTok Video", "url": res["video"]}
        else:
            return {"error": "دانلود انجام نشد یا لینک نامعتبر است."}
    except Exception as e:
        return {"error": str(e)}
