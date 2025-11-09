from flask import Flask, jsonify, request
from pymongo import MongoClient
import os

app = Flask(__name__)

HOME_MESSAGE = "Hello from Flask DevOps Infra with MongoDB!"
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client["devops_infra"]
col = db["items"]

@app.route("/")
def index():
    return jsonify(message=HOME_MESSAGE)

@app.route("/health")
def health():
    try:
        client.admin.command("ping")
        return jsonify(status="ok")
    except Exception as e:
        return jsonify(status="down", error=str(e)), 500

@app.route("/items", methods=["GET"])
def list_items():
    docs = list(col.find({}, {"_id": 0}))
    return jsonify(items=docs)

@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json(force=True) or {}
    if not data.get("name"):
        return jsonify(error="name is required"), 400
    col.insert_one({"name": data["name"], "value": data.get("value")})
    return jsonify(created=True), 201