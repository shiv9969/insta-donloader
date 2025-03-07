import os
import re
import logging
import asyncio
import uvicorn
import logging
from fastapi import FastAPI
from pyrogram import Client, filters
from downloader import download_instagram_video
from config.settings import API_ID, API_HASH, BOT_TOKEN

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI server
app = FastAPI()

@app.get("/")
def home():
    return {"status": "Bot is running!"}

# Initialize Telegram bot
bot = Client("InstaDownloaderBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Handle /start command
@bot.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await message.reply_text("👋 Hello! Send me an Instagram link, and I'll download the video for you.")

# Instagram URL Pattern
INSTAGRAM_REGEX = r"(https?:\/\/)?(www\.)?(instagram\.com\/(?:p|reel|tv|stories)\/[a-zA-Z0-9_-]+)"

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@bot.on_message(filters.text & (filters.private | filters.group))
async def insta_downloader(client, message):
    logger.info(f"Received message: {message.text}")  # Debugging log

    text = message.text.strip()
    if not text:
        return

    # Check if the message contains an Instagram link
    match = re.search(INSTAGRAM_REGEX, text)
    if not match:
        logger.info("Ignoring non-Instagram link.")  # Debugging log
        return  # Ignore non-Instagram links

    insta_url = match.group(0)
    await message.reply_text("🔄 Downloading... Please wait.")
    video_path = download_instagram_video(insta_url)

    if video_path:
        await message.reply_video(video_path, caption="@BoB_Files1 📲")
    else:
        await message.reply_text("❌ Failed to download the Instagram video.")

# Function to start both FastAPI and Pyrogram
async def main():
    # Run Pyrogram and FastAPI together
    await bot.start()
    logger.info("Telegram bot started successfully!")

    config = uvicorn.Config(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    server = uvicorn.Server(config)
    await server.serve()

    await bot.stop()

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())

