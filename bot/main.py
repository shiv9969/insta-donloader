import re
import logging
from pyrogram import Client, filters
from downloader import download_instagram_video
from config.settings import API_ID, API_HASH, BOT_TOKEN

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Initialization
app = Client("InstaDownloaderBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Instagram URL Pattern
INSTAGRAM_REGEX = r"(https?:\/\/)?(www\.)?(instagram\.com\/(?:p|reel|tv|stories)\/[a-zA-Z0-9_-]+)"

@app.on_message(filters.text & (filters.private | filters.group))
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

# Run the bot
app.run()
