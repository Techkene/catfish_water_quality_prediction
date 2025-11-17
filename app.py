from flask import Flask, request, jsonify
import joblib
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the model artifacts
try:
    model = joblib.load('water_quality_model.pkl')
    scaler = joblib.load('scaler.pkl')
    model_columns = joblib.load('model_columns.pkl')
    print("Model artifacts loaded successfully.")
except Exception as e:
    print(f"Error loading model artifacts: {e}")
    model = None

@app.route('/')
def home():
    return "Water Quality Prediction API is running. Use /predict to make predictions."

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model is not loaded.'}), 500

    try:
        # Get data from POST request
        data = request.json
        
        # Check if all required columns are present
        missing_cols = [col for col in model_columns if col not in data]
        if missing_cols:
            return jsonify({'error': f'Missing fields: {", ".join(missing_cols)}'}), 400

        # Create input array in the correct order
        input_data = np.array([data[col] for col in model_columns]).reshape(1, -1)
        
        # Scale the input data
        scaled_data = scaler.transform(input_data)
        
        # Make prediction
        prediction = model.predict(scaled_data)
        
        # Return the prediction as JSON
        return jsonify({'water_quality_prediction': int(prediction[0])})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Run the app on host 0.0.0.0 to be accessible from outside the container
    app.run(host='0.0.0.0', port=5000)