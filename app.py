from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to extract product name from AliExpress product page
def extract_product_info(product_url):
    try:
        # Fetch the product page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(product_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product name
        product_name = soup.find('h1', class_='product-title-text').text.strip()

        # Log the product name for debugging
        print("Product Name:", product_name)
        return {
            'product_name': product_name
        }
    except requests.exceptions.RequestException as e:
        print("Error fetching product page:", e)
        return None
    except Exception as e:
        print("Unexpected error:", e)
        return None

# API endpoint
@app.route('/check-product', methods=['POST'])
def check_product():
    try:
        data = request.json
        product_url = data.get('product_url')
        if not product_url:
            return jsonify({'error': 'Product URL is required'}), 400

        # Extract product info
        product_info = extract_product_info(product_url)
        if product_info:
            return jsonify({
                'product_name': product_info['product_name']
            })
        return jsonify({'error': 'Failed to fetch product information'}), 500
    except Exception as e:
        print("Unexpected error in /check-product:", e)
        return jsonify({'error': 'Internal server error'}), 500

# Health check endpoint
@app.route('/')
def health_check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
