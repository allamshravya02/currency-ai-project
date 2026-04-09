from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from conversion import convert_currency
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS to allow frontend requests

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
# SERVE CONVERSION MODULE FRONTEND
# -------------------------------
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def serve_static_files(path):
    return send_from_directory('static', path)

# Catch-all for other files in static folder
@app.route('/<path:path>')
def serve_other_static(path):
    # Don't interfere with /home routes
    if path.startswith('home'):
        return "Not found", 404
    
    # Try to serve from static folder
    try:
        return send_from_directory('static', path)
    except:
        return "Not found", 404

# -------------------------------
# MANUAL CONVERSION API
# -------------------------------
@app.route("/convert/manual", methods=["POST"])
def manual_conversion():
    data = request.json
    result = convert_currency(
        data["from"],
        data["to"],
        float(data["amount"])
    )
    return jsonify(result)

# -------------------------------
# IMAGE-BASED CONVERSION (SIMULATED)
# -------------------------------
@app.route("/convert/image", methods=["POST"])
def image_conversion():
    # Simulated AI output
    recognized_currency = "INR"
    recognized_amount = 500
    target_currency = request.form["to"]
    
    result = convert_currency(
        recognized_currency,
        target_currency,
        recognized_amount
    )
    
    return jsonify({
        "recognized_currency": recognized_currency,
        "recognized_amount": recognized_amount,
        "conversion": result
    })

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)