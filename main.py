import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_BOT_TOKEN or not GEMINI_API_KEY:
    logging.error("Missing TELEGRAM_BOT_TOKEN or GEMINI_API_KEY environment variables.")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "models/gemini-2.0-flash-001"
model = genai.GenerativeModel(MODEL_NAME)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Gemini 2.0 Flash powered bot ready to chat!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    logging.info(f"User input: {user_text}")

    try:
        response = model.generate_text(prompt=user_text)
        reply = response.text
        logging.info(f"Gemini 2.0 Flash response: {reply}")
        await update.message.reply_text(reply)
    except Exception as e:
        logging.error(f"Error calling Gemini 2.0 Flash API: {e}")
        await update.message.reply_text("⚠️ Sorry, something went wrong. Please try again later.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Bot running with Gemini 2.0 Flash model...")
    app.run_polling()

if __name__ == "__main__":
    main()
