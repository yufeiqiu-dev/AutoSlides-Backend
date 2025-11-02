from flask import Flask
from app.routes import register_routes

import os                         
from dotenv import load_dotenv     
import firebase_admin           
from firebase_admin import credentials 
from .utils.logger import get_logger

logger = get_logger("APP Start")
# --- ADD THIS BLOCK ---
# Load secrets from .env file (AWS_KEYS, FIREBASE_KEY_PATH)
load_dotenv()
# Initialize Firebase Admin SDK
firebase_key_path = os.getenv("FIREBASE_KEY_PATH")
if not firebase_key_path:
    logger.info("Firebase credentials key path not found. Protected route cannot be used")
else:
    try:
        cred = credentials.Certificate(firebase_key_path)
        firebase_admin.initialize_app(cred)
        logger.info("Firebase Admin SDK initialized successfully.")
    except Exception as e:
        # This is also critical
        logger.info(f"Failed to initialize Firebase Admin SDK: {e}")
        raise RuntimeError(f"Failed to initialize Firebase Admin SDK: {e}")
# --- END OF BLOCK ---

def create_app():
    app = Flask(__name__)
    register_routes(app)
    return app

# Flask entry point
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)