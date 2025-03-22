
WEBHOOK_URL = "https://aliexpress-shipping-methods.vercel.app/webhook"

import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Function to fetch product name from AliExpress link
def fetch_product_name(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        product_name = soup.find("h1", {"class": "product-title-text"}).text.strip()
        return product_name
    except Exception as e:
        print(f"Error fetching product name: {e}")
        return None

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me an AliExpress link, and I'll fetch the product name for you.")

# Message handler for AliExpress links
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "aliexpress.com" in text:
        product_name = fetch_product_name(text)
        if product_name:
            await update.message.reply_text(f"Product Name: {product_name}")
        else:
            await update.message.reply_text("Sorry, I couldn't fetch the product name.")
    else:
        await update.message.reply_text("Please send a valid AliExpress link.")

# Main function to run the bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
