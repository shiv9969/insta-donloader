import re
import logging
from pyrogram import Client, filters
from bot.downloader import download_instagram_video
from config.settings import API_ID, API_HASH, BOT_TOKEN

# Logging
logging.basicConfig(level=logging.INFO)

# Bot Initialization
app = Client("InstaDownloaderBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Instagram URL Pattern
INSTAGRAM_REGEX = r"(?:https?:\/\/)?(?:www\.)?(instagram\.com\/(?:p|reel|tv|stories)\/[a-zA-Z0-9_-]+)"

@app.on_message(filters.private | filters.group)
async def insta_downloader(client, message):
    text = message.text

    if not text:
        return

    # Check if the message contains an Instagram link
    match = re.search(INSTAGRAM_REGEX, text)
    if not match:
        return  # Ignore non-Instagram links

    insta_url = match.group(0)
    await message.reply_text("🔄 Downloading... Please wait.")

    video_path = download_instagram_video(insta_url)
    if video_path:
        await message.reply_video(video_path, caption="Here is your Instagram video! 📲")
    else:
        await message.reply_text("❌ Failed to download the Instagram video.")

# Run the bot
app.run()
