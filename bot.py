import os
import re
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.utils.executor import start_webhook
from flask import Flask, request
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = "https://aliexpress-shipping-methods.vercel.app/webhook"

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
app = Flask(__name__)

# Function to fetch product name from AliExpress
def fetch_product_name(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("title").text.strip()
        return title.replace("| AliExpress", "")
    return "Couldn't fetch product details. Make sure the link is correct."

# Handle messages with AliExpress links
@dp.message_handler(regexp=r"https?://(?:www\.)?aliexpress\..+")
async def get_product_name(message: types.Message):
    url = re.search(r"https?://[^\s]+", message.text).group()
    product_name = fetch_product_name(url)
    await message.reply(f"Product Name: {product_name}")

# Handle start/help commands
@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("Send me an AliExpress link, and I'll fetch the product name for you!")

# Webhook route for Telegram
@app.route("/webhook", methods=["POST"])
async def webhook():
    update = Update(**request.json)
    await dp.process_update(update)
    return "OK", 200

# Set webhook on startup
async def set_webhook():
    await bot.set_webhook(WEBHOOK_URL)

# Run Flask server
if __name__ == "__main__":
    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
