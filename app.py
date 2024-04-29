from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://robertsshalajevs:hwbYyJw4bfO8vnTU@fitfuel.xhemssx.mongodb.net/?retryWrites=true&w=majority&appName=fitfuel")

db = client.fit_fuel
products = db.products
orders = db.orders

def add_products():
    product_data = [
        {"id": "2", "name": "Whey Protein", "price": 29.99, "manufacturer": "Optimum Nutrition", "type": "Protein", "description": "High-quality whey protein powder", "availability": 10, "image": ""},
        {"id": "3", "name": "BCAA", "price": 19.99, "manufacturer": "MusclePharm", "type": "Amino Acid", "description": "Branched-chain amino acid supplement", "availability": 15, "image": ""},
        {"id": "4", "name": "Creatine Monohydrate", "price": 17.99, "manufacturer": "MuscleTech", "type": "Creatine", "description": "Pure creatine monohydrate powder", "availability": 20, "image": ""},
        {"id": "5", "name": "Pre-Workout", "price": 34.99, "manufacturer": "Cellucor", "type": "Pre-Workout", "description": "Energy-boosting pre-workout supplement", "availability": 8, "image": ""},
        {"id": "6", "name": "Mass Gainer", "price": 49.99, "manufacturer": "Dymatize", "type": "Mass Gainer", "description": "High-calorie mass gainer shake", "availability": 12, "image": ""},
        {"id": "7", "name": "Casein Protein", "price": 32.99, "manufacturer": "MusclePharm", "type": "Protein", "description": "Slow-digesting protein for nighttime", "availability": 18, "image": ""},
        {"id": "8", "name": "Fish Oil", "price": 14.99, "manufacturer": "NOW Foods", "type": "Supplement", "description": "Omega-3 fish oil softgels", "availability": 25, "image": ""},
        {"id": "9", "name": "Multivitamin", "price": 21.99, "manufacturer": "Optimum Nutrition", "type": "Vitamin", "description": "Comprehensive multivitamin tablets", "availability": 30, "image": ""},
        {"id": "10", "name": "Glutamine", "price": 23.99, "manufacturer": "BulkSupplements.com", "type": "Amino Acid", "description": "Pure glutamine powder for recovery", "availability": 22, "image": ""},
        {"id": "11", "name": "Energy Gel", "price": 1.99, "manufacturer": "GU Energy Labs", "type": "Energy", "description": "Quick energy gel for endurance athletes", "availability": 40, "image": ""},
        {"id": "12", "name": "Beta-Alanine", "price": 23.99, "manufacturer": "BulkSupplements.com", "type": "Amino Acid", "description": "Carnosine-boosting beta-alanine powder", "availability": 17, "image": ""},
        {"id": "13", "name": "Electrolyte Drink", "price": 9.99, "manufacturer": "Gatorade", "type": "Electrolyte", "description": "Refreshing electrolyte sports drink", "availability": 35, "image": ""},
        {"id": "14", "name": "Vitamin D3", "price": 7.99, "manufacturer": "Nature Made", "type": "Vitamin", "description": "Vitamin D3 softgel capsules", "availability": 28, "image": ""},
        {"id": "15", "name": "Testosterone Booster", "price": 39.99, "manufacturer": "TestoFuel", "type": "Testosterone", "description": "Natural testosterone support supplement", "availability": 13, "image": ""},
        {"id": "16", "name": "Weight Loss Supplement", "price": 28.99, "manufacturer": "Transparent Labs", "type": "Weight Loss", "description": "Thermogenic fat burner capsules", "availability": 9, "image": ""},
        {"id": "17", "name": "ZMA Supplement", "price": 17.99, "manufacturer": "MET-Rx", "type": "Mineral", "description": "Zinc, magnesium, and vitamin B6 supplement", "availability": 20, "image": ""},
        {"id": "18", "name": "Joint Support Supplement", "price": 15.99, "manufacturer": "Doctor's Best", "type": "Supplement", "description": "Supports joint health and flexibility", "availability": 32, "image": ""},
        {"id": "19", "name": "Amino Acid Supplement", "price": 22.99, "manufacturer": "MuscleTech", "type": "Amino Acid", "description": "Essential amino acids for muscle recovery", "availability": 24, "image": ""},
        {"id": "20", "name": "Carb Supplement", "price": 11.99, "manufacturer": "NOW Sports", "type": "Carbohydrate", "description": "Fast-acting carbohydrate powder", "availability": 26, "image": ""},
        {"id": "21", "name": "Whey Isolate Protein Powder", "price": 34.99, "manufacturer": "Isopure", "type": "Protein", "description": "High-quality whey isolate protein powder", "availability": 19, "image": ""}
    ]
    
    products.insert_many(product_data)

def add_orders():
    orders_data = [
        {"test" : "test"}
    ]

    orders.insert_many(orders_data)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/products', methods=['GET'])
def get_products():
    query = {}

    product_types = request.args.getlist('type')
    manufacturer = request.args.get('manufacturer')
    max_price = request.args.get('price')

    if product_types:
        query["type"] = {"$in": product_types}

    if manufacturer:
        query["manufacturer"] = manufacturer

    if max_price:
        query["price"] = {"$lte": float(max_price)}

    result = products.find(query)

    items_list = list(result)

    return json_util.dumps(items_list)

@app.route('/products/<id>', methods=['GET'])
def get_product_by_id(id):
    query = {"id": id}
    result = products.find_one(query)
    return json_util.dumps(result)

@app.route('/cart', methods=['POST'])
def get_cart():
    data = request.json
    product_ids = data.get("products", [])
    total_price = 0
    cart_items = []

    for product_id in product_ids:
        query = {"id": str(product_id)}
        product = products.find_one(query)
        if product:
            total_price += product["price"]
            cart_items.append(product)

    response = {"total_price": total_price, "cart_items": cart_items}
    return json_util.dumps(response)


if __name__ == '__main__':
    # add_products()
    # add_orders()
    app.run(debug=True)
