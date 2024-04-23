from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)
CORS(app)

client = MongoClient('localhost', 27017)

db = client.flask_database
todos = db.todos

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/products', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        state = request.args.get('state')
        seller_id = request.args.get('seller_id')

        # Query MongoDB based on state and seller_id
        query = {"state": state, "seller_id": seller_id}
        result = todos.find(query)

        # Convert MongoDB cursor to list of dictionaries
        items_list = list(result)

        # Serialize ObjectId to string using json_util
        return json_util.dumps(items_list)

    else:
        return 'Method not allowed'

if __name__ == '__main__':
    app.run(debug=True)
