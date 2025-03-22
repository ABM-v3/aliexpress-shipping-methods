from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to extract shipping methods from AliExpress product page
def extract_shipping_methods(product_url):
    try:
        # Fetch the product page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(product_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract shipping methods
        shipping_methods = []
        shipping_elements = soup.find_all('div', class_='shipping-method')
        for element in shipping_elements:
            shipping_methods.append(element.text.strip())

        return shipping_methods
    except requests.exceptions.RequestException as e:
        print("Error fetching product page:", e)
        return None

# API endpoint
@app.route('/check-shipping', methods=['POST'])
def check_shipping():
    data = request.json
    product_url = data.get('product_url')
    if not product_url:
        return jsonify({'error': 'Product URL is required'}), 400

    # Extract shipping methods
    shipping_methods = extract_shipping_methods(product_url)
    if shipping_methods is not None:
        # Check if "Aliexpress Standard Shipping" is in the list
        supports_standard_shipping = any(
            "Aliexpress Standard Shipping" in method for method in shipping_methods
        )
        return jsonify({
            'supports_standard_shipping': supports_standard_shipping,
            'shipping_methods': shipping_methods
        })
    return jsonify({'error': 'Failed to fetch shipping information'}), 500

# Health check endpoint
@app.route('/')
def health_check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
