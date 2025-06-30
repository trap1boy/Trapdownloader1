# downloader/pinterest.py

import requests

def download_pinterest(url):
    try:
        api_url = "https://pinterestvideodownloader.com/api/widget"
        res = requests.post(api_url, data={"url": url})
        if "download_url" in res.text:
            # Parse لینک دانلود از HTML
            download_link = res.text.split('href="')[1].split('"')[0]
            return {"title": "Pinterest Download", "url": download_link}
        else:
            return {"error": "لینک معتبر یا قابل دانلود نیست."}
    except Exception as e:
        return {"error": str(e)}
