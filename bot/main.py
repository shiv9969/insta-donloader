import re
import logging
import threading
import uvicorn
from fastapi import FastAPI
from pyrogram import Client, filters
from downloader import download_instagram_video
from config.settings import API_ID, API_HASH, BOT_TOKEN

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Initialization
app = Client("InstaDownloaderBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# FastAPI for health check
api = FastAPI()

@api.get("/")
async def root():
    return {"message": "Bot is running"}

# Instagram URL Pattern
INSTAGRAM_REGEX = r"(?:https?:\/\/)?(?:www\.)?(instagram\.com\/(?:p|reel|tv|stories)\/[a-zA-Z0-9_-]+)"

@app.on_message(filters.text & (filters.private | filters.group))
async def insta_downloader(client, message):
    logger.info(f"Received message: {message.text}")

    text = message.text.strip()
    if not text:
        return

    # Check if the message contains an Instagram link
    match = re.search(INSTAGRAM_REGEX, text)
    if not match:
        logger.info("Ignoring non-Instagram link.")
        return  # Ignore non-Instagram links

    insta_url = match.group(0)
    await message.reply_text("🔄 Downloading... Please wait.")

    video_path = download_instagram_video(insta_url)
    if video_path:
        await message.reply_video(video_path, caption="@BoB_Files1 📲")
    else:
        await message.reply_text("❌ Failed to download the Instagram video.")

# Start both the bot and web server
def start_bot():
    app.run()

threading.Thread(target=start_bot).start()

uvicorn.run(api, host="0.0.0.0", port=10000)
