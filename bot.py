import os
import re
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = f"https://aliexpress-shipping-methods.vercel.app/webhook"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
app = Flask(__name__)

def fetch_product_name(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("title").text.strip()
        return title.replace("| AliExpress", "")
    return "Couldn't fetch product details. Make sure the link is correct."

@dp.message_handler(regexp=r"https?://(?:www\.)?aliexpress\..+")
async def get_product_name(message: Message):
    url = re.search(r"https?://[^\s]+", message.text).group()
    product_name = fetch_product_name(url)
    await message.reply(f"Product Name: {product_name}")

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: Message):
    await message.reply("Send me an AliExpress link, and I'll fetch the product name for you!")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = types.Update(**request.json)
    dp.process_update(update)
    return "OK", 200

async def set_webhook():
    await bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    import asyncio
    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
