from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os
import json

app = Flask(__name__)
CORS(app)

# =========================
# LOAD MODEL
# =========================
model = tf.keras.models.load_model("models/best_currency_model.keras")

# =========================
# LOAD CLASS INDICES
# =========================
with open("class_indices.json") as f:
    class_indices = json.load(f)

class_names = {v: k for k, v in class_indices.items()}

# =========================
# CURRENCY MAPPING
# =========================
CURRENCY_MAPPING = {
    'INR_10': {'currency': 'INR', 'denomination': 10, 'country': 'India'},
    'INR_20': {'currency': 'INR', 'denomination': 20, 'country': 'India'},
    'INR_50': {'currency': 'INR', 'denomination': 50, 'country': 'India'},
    'INR_100': {'currency': 'INR', 'denomination': 100, 'country': 'India'},
    'INR_200': {'currency': 'INR', 'denomination': 200, 'country': 'India'},
    'INR_500': {'currency': 'INR', 'denomination': 500, 'country': 'India'},

    'USD_1': {'currency': 'USD', 'denomination': 1, 'country': 'United States'},
    'USD_2': {'currency': 'USD', 'denomination': 2, 'country': 'United States'},
    'USD_5': {'currency': 'USD', 'denomination': 5, 'country': 'United States'},
    'USD_10': {'currency': 'USD', 'denomination': 10, 'country': 'United States'},
    'USD_50': {'currency': 'USD', 'denomination': 50, 'country': 'United States'},
    'USD_100': {'currency': 'USD', 'denomination': 100, 'country': 'United States'},

    'THAI_20': {'currency': 'THB', 'denomination': 20, 'country': 'Thailand'},
    'THAI_50': {'currency': 'THB', 'denomination': 50, 'country': 'Thailand'},
    'THAI_100': {'currency': 'THB', 'denomination': 100, 'country': 'Thailand'},
    'THAI_500': {'currency': 'THB', 'denomination': 500, 'country': 'Thailand'},
    'THAI_1000': {'currency': 'THB', 'denomination': 1000, 'country': 'Thailand'},
}

# =========================
# PREDICT ROUTE
# =========================
@app.route("/predict", methods=["POST"])
def predict():
    file_path = "temp.jpg"

    try:
        if "image" not in request.files:
            return jsonify({"success": False, "error": "No image uploaded"}), 400

        file = request.files["image"]

        if file.filename == "":
            return jsonify({"success": False, "error": "Empty file"}), 400

        file.save(file_path)

        # Preprocess (same as training)
        img = image.load_img(file_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Prediction
        prediction = model.predict(img_array)
        index = int(np.argmax(prediction))
        confidence = float(np.max(prediction)) * 100

        predicted_class = class_names.get(index, "Unknown")

        print("Class:", predicted_class, "Confidence:", confidence)

        # ✅ Threshold raised to 75%
        if confidence < 75:
            return jsonify({
                "success": False,
                "error": "Low confidence. Please upload a clearer image of the currency note.",
                "confidence": round(confidence, 2),
                "retry": True          # <-- frontend can use this flag to prompt re-upload
            }), 400

        # =========================
        # MAP TO CURRENCY DETAILS
        # =========================
        currency_info = CURRENCY_MAPPING.get(predicted_class)

        if not currency_info:
            return jsonify({
                "success": False,
                "error": f"Unsupported class: {predicted_class}"
            }), 400

        return jsonify({
            "success": True,
            "prediction": predicted_class,
            "currency": currency_info["currency"],
            "denomination": currency_info["denomination"],
            "country": currency_info["country"],
            "confidence": round(confidence, 2)
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# =========================
# HEALTH CHECK
# =========================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": True,
        "supported_currencies": list(CURRENCY_MAPPING.keys())
    })

# =========================
# RUN
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port)