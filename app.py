from flask import Flask, jsonify, request
from flask_cors import CORS
import openfoodfacts

app = Flask(__name__)
CORS(app)


# Create the OpenFoodFacts client
food_api = openfoodfacts.API(
    user_agent="InventoryManager/1.0"
)


# Temporary inventory for Charon Fresh Market
inventory = [
    {
        "id": 1,
        "product_name": "Kenyan Premium Macadamia Milk",
        "brands": "NutriHarvest",
        "barcode": "0619202500018",
        "price": 450.00,
        "stock": 32,
        "ingredients_text": "Macadamia nuts, filtered water, natural sweetener"
    },
    {
        "id": 2,
        "product_name": "Creamy Honey Peanut Spread",
        "brands": "Golden Spoon",
        "barcode": "0619202500025",
        "price": 380.00,
        "stock": 24,
        "ingredients_text": "Roasted peanuts, natural honey, sea salt"
    },
    {
        "id": 3,
        "product_name": "Whole Grain Breakfast Loaf",
        "brands": "Daily Harvest",
        "barcode": "0619202500032",
        "price": 250.00,
        "stock": 18,
        "ingredients_text": "Whole wheat flour, oats, yeast, sunflower seeds"
    },
    {
        "id": 4,
        "product_name": "Natural Tropical Mango Juice",
        "brands": "TropiFresh",
        "barcode": "0619202500049",
        "price": 180.00,
        "stock": 45,
        "ingredients_text": "Mango juice, water, natural fruit extract"
    },
    {
        "id": 5,
        "product_name": "Organic Crunchy Granola",
        "brands": "Nature Basket",
        "barcode": "0619202500056",
        "price": 520.00,
        "stock": 20,
        "ingredients_text": "Rolled oats, almonds, raisins, honey"
    }
]




@app.route("/", methods=["GET"])
def index():
    main = "<h1>Home</h1>"
    return main

# All Products
@app.route("/inventory", methods=["GET"])
def all():
    return jsonify(inventory), 200

# One product
@app.route("/inventory/<int:id>", methods=["GET"])
def one(id):
    item = next((i for i in inventory if i["id"]==id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200

# Create a Product

@app.route("/inventory", methods=["POST"])
def create():
    product = request.get_json()

    if not product:
        return jsonify({"error": "Please provide product details"}), 400

    required = ["product_name", "price", "stock"]
    missing = [key for key in required if key not in product]

    if missing:
        return jsonify({
            "message": f"Missing required fields: {', '.join(missing)}"
        }), 400

    new_id = max([i["id"] for i in inventory], default=0) + 1

    new_product = {
        "id": new_id,
        "product_name": product["product_name"],
        "brands": product.get("brands", ""),
        "barcode": product.get("barcode", ""),
        "price": product["price"],
        "stock": product["stock"],
        "ingredients_text": product.get("ingredients_text", "")
    }

    inventory.append(new_product)

    return jsonify({
        "message": "Product added successfully",
        "product": new_product
    }), 201

# Update a product

# Update a product
@app.route("/inventory/<int:id>", methods=["PATCH"])
def update(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Please provide product details"}), 400

    product = next((i for i in inventory if i["id"] == id), None)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    if "product_name" in data:
        product["product_name"] = data["product_name"]

    if "brands" in data:
        product["brands"] = data["brands"]

    if "barcode" in data:
        product["barcode"] = data["barcode"]

    if "price" in data:
        product["price"] = data["price"]

    if "stock" in data:
        product["stock"] = data["stock"]

    if "ingredients_text" in data:
        product["ingredients_text"] = data["ingredients_text"]

    return jsonify({
        "message": f"Product '{product['product_name']}' updated successfully",
        "product": product
    }), 200

# delete a product
@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete(id):
    global inventory

    item = next((i for i in inventory if i["id"] == id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    product_name = item["product_name"]

    inventory = [i for i in inventory if i["id"] != id]

    return jsonify({
        "message": f"Product '{product_name}' deleted successfully"
    }), 200


    









if __name__ == "__main__":
    app.run(debug=True, port=5000)