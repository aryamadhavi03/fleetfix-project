from flask import Flask, request, jsonify
import joblib  # For loading ML models
import numpy as np
import pandas as pd  # For DataFrame handling
import google.generativeai as genai  # Gemini AI
import os  # For environment variables
from dotenv import load_dotenv  # Load .env file
from flask_cors import CORS  # ✅ Import CORS
from flask_bcrypt import Bcrypt  # ✅ Import Bcrypt for password hashing
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity  # ✅ Import JWT for authentication
from config import users_collection  # Import MongoDB collections from config

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ Allow all origins

# Import blueprints after app initialization
from api.vehicle_routes import vehicle_bp
from api.garage_routes import garage_bp
from api.report_routes import report_bp

# Register blueprints
app.register_blueprint(vehicle_bp, url_prefix='/api')
app.register_blueprint(garage_bp, url_prefix='/api')
app.register_blueprint(report_bp, url_prefix='/api')

# Flask Security Configs
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your_secret_key")  # Change in production
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Load trained ML models safely
try:
    classifier = joblib.load("fclassifier.pkl")  # Classification model
    regressor = joblib.load("fregressor.pkl")  # Regression model
    scaler = joblib.load("fscaler.pkl")  # Feature scaler
except FileNotFoundError as e:
    raise FileNotFoundError(f"🚨 Model file missing: {e}")

# Get API Key securely
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("🚨 ERROR: Gemini API Key is missing! Check your .env file.")

# Configure Gemini AI API
genai.configure(api_key=api_key)

# Function to generate maintenance explanation using Gemini AI
def generate_explanation(features, maintenance_status):
    prompt = f"""
    🚗 Vehicle Maintenance Prediction Report



    ▼ Vehicle Input Parameters:
    - Age: {features[0]} years (0–18)
    - Odometer Reading: {features[1]} km
    - Current Payload: {features[2]} tons (Max: 50)
    - Fuel Consumption Rate (FCR): {features[3]} L/100km
    - Mileage: {features[4]} km/l
    - Engine Temperature: {features[5]}°C
    - Oil Pressure: {features[6]} psi
    - Tyre Pressure (Front): {features[7]} psi
    - Tyre Pressure (Rear): {features[8]} psi
    - ABS Status: {'ON' if features[9] == 1 else 'OFF'}
    - Average Speed: {features[10]} km/h
    - Coolant Temperature: {features[11]}°C
    - Battery Status: {'Healthy' if features[12] == 1 else 'Unhealthy'}
    - RPM: {features[13]}
    - Time Since Last Maintenance: {features[14]} days
    - Maintenance History: {features[15]}
    - Service History Count: {features[16]}
    - Weather: {features[17]}
    - Road Type: {features[18]}

    ▼ Prediction Result:
    - Maintenance Required: {'Yes' if maintenance_status == 1 else 'No'}

    Please provide a concise and structured explanation of the vehicle's condition and maintenance recommendation in the following format:

    -----------------------------------------
    🔍 1. Vehicle Condition Analysis:
    - Provide a brief but clear analysis of the vehicle's current performance and reliability based on the input parameters.

    🛠 2. Identified Maintenance Issues:
    - List any issues or early warning signs detected through the sensor and usage data.

    ✅ 3. Recommended Maintenance Actions:
    - Suggest what type of service or maintenance is needed and the priority level.

    📊 4. Technical Breakdown:
    - Present a technical health score of the vehicle in percentage form (e.g., "Vehicle Health: 74%").

    ⚠️ 5. Urgency of Maintenance:
    - Estimate a maintenance urgency score (0 to 100%) based on severity and risk.
    - If Maintenance is "No", the urgency should be <15%.
    - If Maintenance is "Yes", urgency should be between 60% and 100%.
    -----------------------------------------

    ⚠️ Note: Ensure that the language is simple and clear enough for both technical and non-technical users.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)

        return response.text if hasattr(response, "text") else "No explanation generated."
    except Exception as e:
        return f"Error generating explanation: {str(e)}"


# Home route
@app.route("/")
def home():
    return "🚀 Flask API is running with ML models and Gemini AI!"

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if "features" not in data:
            return jsonify({"error": "Missing 'features' in request data"}), 400
        
        features = np.array(data["features"]).reshape(1, -1)
        print("🚨 Raw Input Features:", data["features"])

        # Scale features
        features_scaled = scaler.transform(features)
        print("📊 Scaled Features:", features_scaled)

        # Make predictions
        maintenance_status = classifier.predict(features_scaled)[0]
        maintenance_percentage = regressor.predict(features_scaled)[0]

        # Generate Gemini explanation
        explanation = generate_explanation(features[0].tolist(), maintenance_status)

        return jsonify({
            "Maintenance_Need": bool(maintenance_status),
            "Need_Percentage": float(maintenance_percentage),
            "explanation": explanation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔹 User Registration Route
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    name = data.get("name")
    password = bcrypt.generate_password_hash(data.get("password")).decode("utf-8")

    if users_collection.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 400

    users_collection.insert_one({"email": email, "name": name, "password": password})
    return jsonify({"message": "User registered successfully"}), 201

# 🔹 User Login Route
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = users_collection.find_one({"email": data.get("email")})

    if user and bcrypt.check_password_hash(user["password"], data.get("password")):
        access_token = create_access_token(identity=user["email"])
        return jsonify({"access_token": access_token, "name": user["name"]}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# 🔹 Protected Route (For Authenticated Users)
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello {current_user}, you are authorized!"}), 200

# Run Flask app securely
if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode)
