import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# === CONFIGURATION FROM ENV ===
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# === INIT GEMINI ===
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# === LOGGING ===
logging.basicConfig(level=logging.INFO)

# === TELEGRAM HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your Gemini-powered smart bot. Ask me anything!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        response = model.generate_content(user_input)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Gemini error: {e}")
        await update.message.reply_text("Something went wrong. Try again later.")

# === MAIN FUNCTION ===
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
