from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory product storage
products = {}

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products), 200

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({'error': 'Product not found'}), 404

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    product_id = len(products) + 1
    products[product_id] = {
        'name': data['name'],
        'price': data['price'],
        'quantity': data['quantity']
    }
    return jsonify({'id': product_id}), 201

if __name__ == '__main__':
    app.run(debug=True)
