import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📥 Send /video <URL> to download video\n🎵 Send /audio <URL> to download audio"
    )

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
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            ext = info.get('ext', 'mp4')
            file_path = f"video.{ext}"

        with open(file_path, 'rb') as video_file:
            await update.message.reply_video(video=video_file, caption="✅ Video downloaded!")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    finally:
        for ext in ['mp4', 'mkv', 'webm']:
            if os.path.exists(f"video.{ext}"):
                os.remove(f"video.{ext}")

async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Please provide an audio URL.")
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
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open("audio.mp3", 'rb') as audio_file:
            await update.message.reply_audio(audio=audio_file, caption="✅ Audio downloaded!")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    finally:
        if os.path.exists("audio.mp3"):
            os.remove("audio.mp3")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("video", download_video))
    app.add_handler(CommandHandler("audio", download_audio))
    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
