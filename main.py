import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp

# Load Telegram bot token from environment
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📥 Welcome! Send /video <URL> to download video\n🎵 Send /audio <URL> to download audio"
    )

# Download video
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Please provide a video URL.")
        return
    url = context.args[0]
    await update.message.reply_text("🔄 Downloading video...")

    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'video.%(ext)s',
            'merge_output_format': 'mp4',
            'cookiefile': 'cookies.txt',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            ext = info.get('ext', 'mp4')
            file_path = f"video.{ext}"

        with open(file_path, 'rb') as video_file:
            await update.message.reply_video(video=video_file, caption="✅ Video downloaded!")

    except Exception as e:
        if "Sign in to confirm you’re not a bot" in str(e):
            await update.message.reply_text("❌ This video requires login. Bot cannot access it.")
        else:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    finally:
        for ext in ['mp4', 'mkv', 'webm']:
            file_path = f"video.{ext}"
            if os.path.exists(file_path):
                os.remove(file_path)

# Download audio
async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Please provide a video URL.")
        return
    url = context.args[0]
    await update.message.reply_text("🔄 Downloading audio...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'cookiefile': 'cookies.txt',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open("audio.mp3", 'rb') as audio_file:
            await update.message.reply_audio(audio=audio_file, caption="✅ Audio downloaded!")

    except Exception as e:
        if "Sign in to confirm you’re not a bot" in str(e):
            await update.message.reply_text("❌ This audio requires login. Bot cannot access it.")
        else:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    finally:
        if os.path.exists("audio.mp3"):
            os.remove("audio.mp3")

# Run the bot
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("video", download_video))
    app.add_handler(CommandHandler("audio", download_audio))
    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
