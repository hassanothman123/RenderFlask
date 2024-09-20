import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory cart storage
carts = {}

PRODUCT_SERVICE_URL = 'https://products-f1gy.onrender.com'  # Change to your Product Service URL on deployment

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart = carts.get(user_id, {})
    return jsonify(cart), 200

@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    if user_id not in carts:
        carts[user_id] = {}
    quantity = request.json.get('quantity', 1)

    # Retrieve product details from Product Service
    product_response = requests.get(f'{PRODUCT_SERVICE_URL}/{product_id}')
    if product_response.status_code != 200:
        return jsonify({'error': 'Product not found'}), 404

    product = product_response.json()
    carts[user_id][product_id] = {
        'name': product['name'],
        'quantity': quantity,
        'total_price': product['price'] * quantity
    }
    return jsonify(carts[user_id]), 201

@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    if user_id in carts and product_id in carts[user_id]:
        del carts[user_id][product_id]
        return jsonify(carts[user_id]), 200
    return jsonify({'error': 'Product not in cart'}), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)
