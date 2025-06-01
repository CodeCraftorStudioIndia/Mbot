import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# === Configuration from Environment Variables ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# === Validate keys ===
if not TELEGRAM_BOT_TOKEN or not GEMINI_API_KEY:
    print("❌ TELEGRAM_BOT_TOKEN or GEMINI_API_KEY is missing in environment variables.")
    exit()

# === Gemini setup ===
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# === Logging ===
logging.basicConfig(level=logging.INFO)

# === /start command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! I'm your Gemini-powered smart bot. Ask me anything.")

# === Text messages ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    print("Sending to Gemini:", user_input)

    try:
        response = model.generate_content(user_input)
        print("Gemini response:", response.text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        await update.message.reply_text("⚠️ Something went wrong. Try again later.")

# === Main function ===
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
