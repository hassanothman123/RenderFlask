from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample product data
products = [
    {"id": 1, "name": "Banana", "price": 0.3, "quantity": 150},
    {"id": 2, "name": "Apple", "price": 0.5, "quantity": 100},
]

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    return jsonify(product) if product else ('', 404)

@app.route('/products', methods=['POST'])
def add_product():
    new_product = request.get_json()
    products.append(new_product)
    return jsonify(new_product), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
