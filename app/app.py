from flask import Flask
from app.routes import register_routes

import os                          # <-- ADD THIS
from dotenv import load_dotenv     # <-- ADD THIS
import firebase_admin              # <-- ADD THIS
from firebase_admin import credentials # <-- ADD THIS

# --- ADD THIS BLOCK ---
# Load secrets from .env file (AWS_KEYS, FIREBASE_KEY_PATH)
load_dotenv()
print("Loaded .env file")

# Initialize Firebase Admin SDK
firebase_key_path = os.getenv("FIREBASE_KEY_PATH")
if not firebase_key_path:
    # This is a critical error, so we'll stop the app
    raise RuntimeError("FIREBASE_KEY_PATH not found in .env file. App cannot start.")
else:
    try:
        cred = credentials.Certificate(firebase_key_path)
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully.")
    except Exception as e:
        # This is also critical
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