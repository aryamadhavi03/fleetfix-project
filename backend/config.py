from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# MongoDB Atlas Connection
client = MongoClient(
    os.getenv("MONGO_URI"),
    serverSelectionTimeoutMS=5000,  # Set timeout for server selection
    connectTimeoutMS=10000,  # Set timeout for initial connection
    socketTimeoutMS=None,  # Set no timeout for operations
    connect=True,  # Make sure we connect immediately
    retryWrites=True,  # Enable retryable writes
    directConnection=False,  # Allow for DNS SRV resolution
    appName="vehicle_maintenance"  # Set application name for monitoring
)
db = client["vehicle_maintenance"]

# Collections
users_collection = db["users"]
vehicles_collection = db["vehicles"]
prediction_history_collection = db["prediction_history"]
garages_collection = db["garages"]