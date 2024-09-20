from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# In-memory storage for user carts
carts = {}

# URL for Product Service
PRODUCT_SERVICE_URL = 'https://products-f1gy.onrender.com/products'  

@app.route('/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    return jsonify(carts.get(user_id, {}))

@app.route('/cart/<user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    if user_id not in carts:
        carts[user_id] = {}
    product = requests.get(f"{PRODUCT_SERVICE_URL}/{product_id}").json()
    if product:
        carts[user_id][product_id] = carts[user_id].get(product_id, 0) + 1
        return jsonify(carts[user_id]), 201
    return ('', 404)

@app.route('/cart/<user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    if user_id in carts and product_id in carts[user_id]:
        del carts[user_id][product_id]
    return jsonify(carts.get(user_id, {})), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
