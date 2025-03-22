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

        # Log the shipping methods for debugging
        print("Shipping Methods:", shipping_methods)
        return shipping_methods
    except requests.exceptions.RequestException as e:
        print("Error fetching product page:", e)
        return None
