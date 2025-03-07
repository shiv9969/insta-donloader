import os
import requests

def download_instagram_video(url):
    api_url = f"https://api.example.com/instagram?url={url}"  # Replace with a working API

    response = requests.get(api_url)
    if response.status_code == 200:
        video_url = response.json().get("video_url")
        if video_url:
            file_name = "instagram_video.mp4"
            with open(file_name, "wb") as f:
                f.write(requests.get(video_url).content)
            return file_name
    return None
