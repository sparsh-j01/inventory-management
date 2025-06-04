from flask import Flask, request, jsonify
from flask_cors import CORS
from linked_list import Inventory
from order_queue import OrderQueue
import csv
from io import StringIO

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8000"}})  # Allow frontend origin

inventory = Inventory()
orders = OrderQueue()

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory.get_all())

@app.route("/inventory", methods=["POST"])
def add_inventory():
    data = request.get_json()
    try:
        # Validate product_id
        if "product_id" not in data:
            return jsonify({"message": "Product ID is required"}), 400
        try:
            product_id = int(data["product_id"])
            if product_id <= 0:
                return jsonify({"message": "Product ID must be a positive number"}), 400
        except ValueError:
            return jsonify({"message": "Product ID must be a valid number"}), 400

        # Validate name
        if "name" not in data:
            return jsonify({"message": "Product name is required"}), 400
        name = data["name"].strip()
        if not name:
            return jsonify({"message": "Product name cannot be empty"}), 400

        # Validate quantity
        if "quantity" not in data:
            return jsonify({"message": "Quantity is required"}), 400
        try:
            quantity = int(data["quantity"])
            if quantity < 0:
                return jsonify({"message": "Quantity cannot be negative"}), 400
        except ValueError:
            return jsonify({"message": "Quantity must be a valid number"}), 400

        # Check if product ID already exists
        existing_product = inventory.search_by_id(product_id)
        if existing_product:
            return jsonify({"message": f"Product with ID {product_id} already exists"}), 400

        inventory.add_product(product_id, name, quantity)
        return jsonify({"message": "Product added to Woxsen Mega Mart inventory"}), 201
    except Exception as e:
        return jsonify({"message": f"Unexpected error: {str(e)}"}), 500

@app.route("/inventory/bulk", methods=["POST"])
def add_bulk_inventory():
    if 'file' not in request.files:
        return jsonify({"message": "No file provided"}), 400
    file = request.files['file']
    if not (file.filename.endswith('.csv') or file.filename.endswith('.txt')):
        return jsonify({"message": "File must be a CSV or TXT"}), 400
    try:
        stream = StringIO(file.stream.read().decode("UTF-8"))
        if file.filename.endswith('.csv'):
            csv_reader = csv.DictReader(stream)
            for row in csv_reader:
                try:
                    product_id = int(row['product_id'])
                    name = row['name']
                    quantity = int(row['quantity'])
                    inventory.add_product(product_id, name, quantity)
                except (KeyError, ValueError):
                    return jsonify({"message": "Invalid CSV format"}), 400
        else:  # .txt file
            lines = stream.getvalue().strip().split('\n')
            for line in lines:
                try:
                    product_id, name, quantity = line.strip().split(',')
                    product_id = int(product_id)
                    quantity = int(quantity)
                    inventory.add_product(product_id, name.strip(), quantity)
                except (ValueError, IndexError):
                    return jsonify({"message": "Invalid TXT format. Use: product_id,name,quantity"}), 400
        return jsonify({"message": "Bulk products added to Woxsen Mega Mart inventory"}), 201
    except Exception as e:
        return jsonify({"message": f"Error processing file: {str(e)}"}), 500

@app.route("/inventory/<int:product_id>", methods=["DELETE"])
def delete_inventory(product_id):
    success = inventory.remove_product(product_id)
    return jsonify({"message": "Product removed from Woxsen Mega Mart inventory" if success else "Product not found in Woxsen Mega Mart inventory"}), 200 if success else 404

@app.route("/inventory/sort", methods=["POST"])
def sort_inventory():
    inventory.sort_by_quantity()
    return jsonify({"message": "Woxsen Mega Mart inventory sorted by quantity"}), 200

@app.route("/inventory/search/<int:product_id>", methods=["GET"])
def search_inventory(product_id):
    product = inventory.search_by_id(product_id)
    if product:
        return jsonify({
            "product_id": product.product_id,
            "name": product.name,
            "quantity": product.quantity
        }), 200
    else:
        return jsonify({"message": "Product not found in Woxsen Mega Mart inventory"}), 404

@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(orders.get_all())

@app.route("/orders", methods=["POST"])
def add_order():
    data = request.get_json()
    try:
        order_id = int(data["order_id"])
        orders.add_order(order_id)
        return jsonify({"message": "Order added to Woxsen Mega Mart queue"}), 201
    except (KeyError, ValueError):
        return jsonify({"message": "Invalid order ID"}), 400

@app.route("/orders/process", methods=["POST"])
def process_order():
    order = orders.process_order()
    if order:
        return jsonify({"message": f"Order {order} processed in Woxsen Mega Mart"}), 200
    return jsonify({"message": "No orders in Woxsen Mega Mart queue"}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)