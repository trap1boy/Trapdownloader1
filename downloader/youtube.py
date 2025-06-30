# downloader/youtube.py

import requests

def download_youtube(url):
    try:
        api_url = f"https://api.vidcdn.top/youtube/video?url={url}"
        res = requests.get(api_url).json()
        if "download" in res:
            return {"title": res.get("title"), "url": res["download"]}
        else:
            return {"error": "دانلود ممکن نیست یا لینک نادرست است."}
    except Exception as e:
        return {"error": str(e)}
