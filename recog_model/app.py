from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os

app = Flask(__name__)
CORS(app)

# Load model
model = tf.keras.models.load_model("models/best_currency_model.keras")
class_names = sorted(os.listdir("dataset/train"))

print("=" * 50)
print("Model loaded successfully!")
print(f"Classes detected: {class_names}")
print("=" * 50)

# Currency mapping - MATCH YOUR EXACT DATASET FOLDERS
CURRENCY_MAPPING = {
    # Indian Rupee
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
    
    # Thai Baht
    'THAI_20': {'currency': 'THB', 'denomination': 20, 'country': 'Thailand'},
    'THAI_50': {'currency': 'THB', 'denomination': 50, 'country': 'Thailand'},
    'THAI_100': {'currency': 'THB', 'denomination': 100, 'country': 'Thailand'},
    'THAI_500': {'currency': 'THB', 'denomination': 500, 'country': 'Thailand'},
    'THAI_1000': {'currency': 'THB', 'denomination': 1000, 'country': 'Thailand'},
    
    # US Dollar
    
}

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        file = request.files["image"]
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Save temporary file
        file_path = "temp.jpg"
        file.save(file_path)

        # Preprocess image
        img = image.load_img(file_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Make prediction
        prediction = model.predict(img_array)
        index = np.argmax(prediction)
        confidence = float(prediction[0][index]) * 100

        # Get predicted class
        predicted_class = class_names[index]
        
        # DEBUG OUTPUT
        print("=" * 50)
        print(f"Predicted class: {predicted_class}")
        print(f"Confidence: {confidence:.2f}%")
        print("=" * 50)
        
        # ✅ CONFIDENCE THRESHOLD - Reject low confidence predictions
        MIN_CONFIDENCE = 70.0  # You can adjust this (70-85 recommended)
        
        if confidence < MIN_CONFIDENCE:
            # Clean up temp file
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return jsonify({
                'success': False,
                'error': f'Image not recognized as a valid currency note. Please upload a clear image of a currency. (Confidence: {confidence:.1f}%)',
                'confidence': round(confidence, 2)
            }), 400
        
        # Get currency details
        currency_info = CURRENCY_MAPPING.get(predicted_class, {
            'currency': 'Unknown',
            'denomination': 0,
            'country': 'Unknown'
        })
        
        # Clean up temp file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # If currency info is Unknown
        if currency_info['currency'] == 'Unknown':
            supported_currencies = ', '.join([k for k in CURRENCY_MAPPING.keys()])
            return jsonify({
                'success': False,
                'error': f'Currency "{predicted_class}" not supported. This model only recognizes: {supported_currencies}'
            }), 400
        
        # Return successful response
        return jsonify({
            'success': True,
            'prediction': predicted_class,
            'currency': currency_info['currency'],
            'denomination': currency_info['denomination'],
            'country': currency_info['country'],
            'confidence': round(confidence, 2)
        })
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Recognition failed: {str(e)}'
        }), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': True,
        'supported_currencies': list(CURRENCY_MAPPING.keys())
    })

if __name__ == "__main__":
    app.run(debug=True, port=5002)