from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["education_portal"]
collection = db["currencies"]

# -------------------------------
# SERVE HOMEPAGE FILES
# -------------------------------
@app.route('/home')
@app.route('/home/')
def home_index():
    homepage_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Homepage')
    return send_from_directory(homepage_path, 'index.html')

@app.route('/home/<path:filename>')
def serve_homepage(filename):
    homepage_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Homepage')
    return send_from_directory(homepage_path, filename)

# -------------------------------
# SERVE EDUCATION PORTAL FRONTEND
# -------------------------------
@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route('/static/<path:path>')
def serve_static_files(path):
    return send_from_directory('static', path)

# Catch-all for other files in static folder
@app.route('/<path:path>')
def serve_other_static(path):
    # Don't interfere with /home or /education routes
    if path.startswith('home') or path.startswith('education'):
        return "Not found", 404
    
    # Try to serve from static folder
    try:
        return send_from_directory('static', path)
    except:
        return "Not found", 404

# -------------------------------
# EDUCATION API
# -------------------------------
@app.route("/education", methods=["GET"])
def get_currency_info():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    result = collection.find_one({
        "$or": [
            {"iso_code": query.upper()},
            {"currency_name": {"$regex": query, "$options": "i"}},
            {"country": {"$regex": query, "$options": "i"}}
        ]
    }, {"_id": 0})
    
    if not result:
        return jsonify({"message": "Currency not found"}), 404
    
    return jsonify(result), 200



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)