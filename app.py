from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = '7668277092:AAHduqzgcBig3eVJOHpgThyXqhCrXAL1N8Q'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'

# Function to extract product name from AliExpress product page
def extract_product_info(product_url):
    try:
        # Fetch the product page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print("Fetching product page:", product_url)  # Log the product URL
        response = requests.get(product_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product name
        product_name_element = soup.find('h1', class_='product-title-text')
        if product_name_element:
            product_name = product_name_element.text.strip()
            print("Product Name Found:", product_name)  # Log the product name
            return product_name
        else:
            print("Product Name Not Found")  # Log if product name is not found
            return None
    except requests.exceptions.RequestException as e:
        print("Error fetching product page:", e)  # Log request errors
        return None
    except Exception as e:
        print("Unexpected error:", e)  # Log unexpected errors
        return None

# Function to send a message to the user
def send_message(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text,
    }
    response = requests.post(f'{TELEGRAM_API_URL}/sendMessage', json=payload)
    return response.json()

# Telegram webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        chat_id = data['message']['chat']['id']
        text = data['message']['text']

        if text == '/start':
            send_message(chat_id, 'Welcome! Send me an AliExpress product link, and I will fetch the product name.')
        elif 'aliexpress.com' in text:
            product_name = extract_product_info(text)
            if product_name:
                send_message(chat_id, f'📦 Product Name: {product_name}')
            else:
                send_message(chat_id, '⚠️ Failed to fetch product information. Please try again later.')
        else:
            send_message(chat_id, 'Please send an AliExpress product link.')

        return jsonify({'status': 'ok'})
    except Exception as e:
        print("Error in webhook:", e)  # Log unexpected errors
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Health check endpoint
@app.route('/')
def health_check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
