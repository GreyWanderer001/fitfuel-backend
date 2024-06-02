from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util, ObjectId
import random
import string

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://robertsshalajevs:hwbYyJw4bfO8vnTU@fitfuel.xhemssx.mongodb.net/?retryWrites=true&w=majority&appName=fitfuel")

db = client.fit_fuel
products = db.products
orders = db.orders

def add_products():
    product_data = [
        {"id": "1", "name": "Whey Isolate Protein Powder", "price": 34.99, "manufacturer": "isopure", "type": "protein", "description": "High-quality whey isolate protein powder", "availability": 19, "image": "https://www.dion.lv/userfiles/72faed7fdc6e03323ded569df4d3d046.png"},
        {"id": "2", "name": "Whey Protein", "price": 29.99, "manufacturer": "isopure", "type": "protein", "description": "High-quality whey protein powder", "availability": 10, "image": "https://www.dion.lv/userfiles/40df428a0375d1552576180ac8d3e445.png"},
        {"id": "3", "name": "BCAA", "price": 19.99, "manufacturer": "isopure", "type": "amino_acid", "description": "Branched-chain amino acid supplement", "availability": 15, "image": "https://www.dion.lv/userfiles/5cfdda07ca4f90eb16489f5dc7ef5865.png"},
        {"id": "4", "name": "Creatine Monohydrate", "price": 17.99, "manufacturer": "isopure", "type": "creatine", "description": "Pure creatine monohydrate powder", "availability": 20, "image": "https://www.dion.lv/userfiles/5f6f11d2149960fc05b93b6e38f38270.png"},
        {"id": "5", "name": "Pre-Workout", "price": 34.99, "manufacturer": "muscletech", "type": "pre_workout", "description": "Energy-boosting pre-workout supplement", "availability": 8, "image": "https://www.dion.lv/userfiles/0963e0090276df715726cd408a8893bd.png"},
        {"id": "6", "name": "Mass Gainer", "price": 49.99, "manufacturer": "muscletech", "type": "mass_gainer", "description": "High-calorie mass gainer shake", "availability": 12, "image": "https://www.dion.lv/userfiles/e54215388c561eeb68ce85292eb0a877.png"},
        {"id": "7", "name": "Casein Protein", "price": 32.99, "manufacturer": "muscletech", "type": "protein", "description": "Slow-digesting protein for nighttime", "availability": 18, "image": "https://www.dion.lv/userfiles/062ae81d773f592477bd630790d5b107.png"},
        {"id": "8", "name": "Fish Oil", "price": 14.99, "manufacturer": "muscletech", "type": "supplement", "description": "Omega-3 fish oil softgels", "availability": 25, "image": "https://cdn-icons-png.freepik.com/512/2650/2650572.png?ga=GA1.1.100187492.1714494508"},
        {"id": "9", "name": "Multivitamin", "price": 21.99, "manufacturer": "cellucor", "type": "vitamin", "description": "Comprehensive multivitamin tablets", "availability": 30, "image": "https://www.dion.lv/userfiles/2998213899d85186fc701f28a9106a74.png"},
        {"id": "10", "name": "Glutamine", "price": 23.99, "manufacturer": "cellucor", "type": "amino_acid", "description": "Pure glutamine powder for recovery", "availability": 22, "image": "https://www.dion.lv/userfiles/dc3e5d2e44fab3ab8fbae0a4def13a3f.png"},
        {"id": "11", "name": "Energy Gel", "price": 1.99, "manufacturer": "cellucor", "type": "energy", "description": "Quick energy gel for endurance athletes", "availability": 40, "image": "https://www.dion.lv/userfiles/7dadb2d7fa3275498a9c418d0ae7b7dc.png"},
        {"id": "12", "name": "Beta-Alanine", "price": 23.99, "manufacturer": "cellucor", "type": "amino_acid", "description": "Carnosine-boosting beta-alanine powder", "availability": 17, "image": "https://www.dion.lv/userfiles/b8792fb0e4b737aeaff03e29d856486c.png"},
        {"id": "13", "name": "Electrolyte Drink", "price": 9.99, "manufacturer": "dymatize", "type": "electrolyte", "description": "Refreshing electrolyte sports drink", "availability": 35, "image": "https://electrolit.com/cdn/shop/products/Electrolit-Orange-Front_1800x1800.png.jpg?v=1653397735"},
        {"id": "14", "name": "Vitamin D3", "price": 7.99, "manufacturer": "dymatize", "type": "vitamin", "description": "Vitamin D3 softgel capsules", "availability": 28, "image": "https://www.dion.lv/userfiles/b38bc75d3a1276c0deb039b7bf0436f6.png"},
        {"id": "15", "name": "Testosterone Booster", "price": 39.99, "manufacturer": "dymatize", "type": "testosterone", "description": "Natural testosterone support supplement", "availability": 13, "image": "https://i5.walmartimages.com/seo/Six-Star-Testosterone-Booster-Caplets-386-mg-Rhodiola-Extract-60-Ct-30-Servings_bd19bad2-fff5-428c-8320-db270b624e43.dc4111ffa545b465400a977394ae3cb1.jpeg?odnHeight=2000&odnWidth=2000&odnBg=FFFFFF"},
        {"id": "16", "name": "Weight Loss Supplement", "price": 28.99, "manufacturer": "dymatize", "type": "weight_loss", "description": "Thermogenic fat burner capsules", "availability": 9, "image": "https://m.media-amazon.com/images/I/71Og3+0NCgL._AC_SL1500_.jpg"},
        {"id": "17", "name": "ZMA Supplement", "price": 17.99, "manufacturer": "bulksupplements", "type": "mineral", "description": "Zinc, magnesium, and vitamin B6 supplement", "availability": 20, "image": "https://proteini.lv/8091-large_default/optimum-nutrition-zma-90-caps.jpg"},
        {"id": "18", "name": "Joint Support Supplement", "price": 15.99, "manufacturer": "bulksupplements", "type": "supplement", "description": "Supports joint health and flexibility", "availability": 32, "image": "https://www.nutritjet.com/wp-content/uploads/2021/06/1-6-600x600.jpg"},
        {"id": "19", "name": "Amino Acid Supplement", "price": 22.99, "manufacturer": "bulksupplements", "type": "amino_acid", "description": "Essential amino acids for muscle recovery", "availability": 24, "image": "https://nowfoods.ca/wp-content/uploads/2022/03/NOW80051_01.png"},
        {"id": "20", "name": "Carb Supplement", "price": 11.99, "manufacturer": "bulksupplements", "type": "carbohydrate", "description": "Fast-acting carbohydrate powder", "availability": 26, "image": "https://muscleadd.com/cdn/shop/files/BlueBerry_1800x1800.jpg?v=1696116087"}
    ]

    products.insert_many(product_data)

def add_orders():
    orders_data = [
        {"name": "Robert Shalajev", "email": "roberts.shalajevs@gmail.com", "phone": "+37129930395", "address": "Jana Enzdelina iela", "comment": ""},
        {"name": "Anna Ivanova", "email": "anna.ivanova@example.com", "phone": "+37128830492", "address": "Brivibas iela 12", "comment": "Piegāde pēc 18:00"},
        {"name": "Mikhail Petrov", "email": "mikhail.petrov@example.com", "phone": "+37126759301", "address": "Kalku iela 5", "comment": "Zvanīt stundu pirms piegādes"},
        {"name": "Elena Smirnova", "email": "elena.smirnova@example.com", "phone": "+37129910029", "address": "Terbatas iela 15", "comment": "Bez komentāriem"},
        {"name": "Alexey Kuznetsov", "email": "alexey.kuznetsov@example.com", "phone": "+37129110385", "address": "Stabu iela 23", "comment": "Atstāt pie durvīm"},
        {"name": "Irina Pavlova", "email": "irina.pavlova@example.com", "phone": "+37126485930", "address": "Valnu iela 30", "comment": "Piegāde tikai darba dienās"},
        {"name": "Dmitry Sokolov", "email": "dmitry.sokolov@example.com", "phone": "+37129847461", "address": "Elizabetes iela 19", "comment": "Nezvanīt, rakstīt SMS"},
        {"name": "Olga Romanova", "email": "olga.romanova@example.com", "phone": "+37126593748", "address": "Raina bulvaris 8", "comment": "Vakara piegāde"},
        {"name": "Nikolay Vasiliev", "email": "nikolay.vasiliev@example.com", "phone": "+37129374829", "address": "Krišjāņa Valdemāra iela 11", "comment": "Neatstāt reģistratūrā"},
        {"name": "Tatiana Morozova", "email": "tatiana.morozova@example.com", "phone": "+37129637284", "address": "Krasta iela 44", "comment": "Piegāde no 12:00 līdz 14:00"}
    ]

    orders.insert_many(orders_data)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/order', methods=['GET'])
def get_orders():
    if request.method == 'GET':
        orders_list=list(orders.find())
        return json_util.dumps(orders_list)

@app.route('/products', methods=['GET', 'POST',])
def get_products():

    if request.method == 'GET':
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
    
    elif request.method == 'POST':
            product_data = request.json
            if not product_data.get('id'):
                product_data['id'] = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            products.insert_one(product_data)
            return json_util.dumps(product_data), 201

@app.route('/products/<id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def manage_product_by_id(id):
    if request.method == 'GET':
        query = {"id": id}
        result = products.find_one(query)
        return json_util.dumps(result)

    elif request.method == 'PATCH':
        update_data = request.json
        products.update_one({"id": id}, {"$set": update_data})
        updated_product = products.find_one({"id": id})
        return json_util.dumps(updated_product)

    elif request.method == 'DELETE':
        products.delete_one({"id": id})
        return '', 204

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

    response = {"total_price": round(total_price, 2), "cart_items": cart_items}
    return json_util.dumps(response)

@app.route('/orders', methods=['POST'])
def get_checkout():
    orders_data = request.json
    product_ids = orders_data.get("products", [])

    for product_id in product_ids:
        product = products.find_one({"id": str(product_id)})
        if product and int(product.get("availability", 0)) > 0:
            new_availability = int(product["availability"]) - 1
            products.update_one({"id": str(product_id)}, {"$set": {"availability": new_availability}})

    orders.insert_one(orders_data)
    return json_util.dumps(orders_data)

if __name__ == '__main__':
    # add_products()
    # add_orders()
    app.run(debug=True)
