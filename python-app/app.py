import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:mysecurepassword2@new36-release-monflask:27017/mydatabase?authSource=admin")
client = MongoClient(MONGO_URI)
db = client.mydatabase
collection = db.mycollection

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app.json_encoder = JSONEncoder

@app.route('/')
def home():
    return "Hello, Flask is running!"

@app.route('/add', methods=['POST'])
def add_document():
    try:
        data = request.json
        result = collection.insert_one(data)
        return jsonify({'message': 'Document added!', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/documents', methods=['GET'])
def get_documents():
    try:
        documents = collection.find()
        doc_list = [{**doc, "_id": str(doc["_id"])} for doc in documents]
        return jsonify(doc_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

