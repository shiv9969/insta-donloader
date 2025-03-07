import os
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

# Initialize FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"status": "Bot is running!"}

# Initialize Telegram bot
bot = Client("InstaDownloaderBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Instagram URL Pattern
INSTAGRAM_REGEX = r"(https?:\/\/)?(www\.)?(instagram\.com\/(?:p|reel|tv|stories)\/[a-zA-Z0-9_-]+)"

@bot.on_message(filters.text & (filters.private | filters.group))
async def insta_downloader(client, message):
    try:
        text = message.text.strip()
        if not text:
            return  # Ignore empty messages

        # Check if the message contains an Instagram link
        match = re.search(INSTAGRAM_REGEX, text)
        if not match:
            return  # Ignore non-Instagram links

        insta_url = match.group(0)
        await message.reply_text("🔄 Downloading... Please wait.")

        video_path = download_instagram_video(insta_url)

        if video_path:
            await message.reply_video(video_path, caption="@BoB_Files1 📲")
        else:
            await message.reply_text("❌ Failed to download the Instagram video. Please try again later.")

    except Exception as e:
        logger.error(f"Error: {e}")
        await message.reply_text("⚠️ An error occurred. Please try again later.")

# Function to start the bot
def start_bot():
    bot.run()

# Start the bot in a separate thread
threading.Thread(target=start_bot).start()

# Run FastAPI server on Render's required port
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
