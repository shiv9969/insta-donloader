import os
import requests

API_KEY = "4f1de6e816msha09ca385c77233ep1c7c84jsn95dc2cc4ec63"
API_URL = "https://instagram-downloader-scraper-reels-igtv-posts-stories.p.rapidapi.com/"

def download_instagram_video(url):
    headers = {
        "x-rapidapi-host": "instagram-downloader-scraper-reels-igtv-posts-stories.p.rapidapi.com",
        "x-rapidapi-key": API_KEY
    }
    
    response = requests.get(API_URL, headers=headers, params={"url": url})
    
    if response.status_code == 200:
        video_url = response.json().get("video_url")  # Adjust this based on the API response format
        if video_url:
            file_name = "instagram_video.mp4"
            with open(file_name, "wb") as f:
                f.write(requests.get(video_url).content)
            return file_name
    return None

