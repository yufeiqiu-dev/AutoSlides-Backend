# --- Imports ---
from flask import request, jsonify, send_file, abort, g  # <-- MODIFIED (added abort, g)
from app.tools.pdf_to_slides import pdf_to_slides
from app.tools.pdf_parser import parse_pdf
from app.tools.TextToSlideContent import generate_slide_content
from app.utils.logger import get_logger
from app.utils.s3_uploader import upload_ppt_to_s3, generate_presigned_url
import io
from firebase_admin import auth  # <-- NEW
from functools import wraps  # <-- NEW

logger = get_logger("AutoSlides")


# --- NEW: Firebase Authentication Decorator ---
# This helper function checks for a valid Firebase token
def protected_by_firebase(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            logger.warning("Protected route accessed without auth header")
            abort(401, description="Authorization header is missing")

        try:
            # Split "Bearer <token>" and get the token
            token = authorization_header.split("Bearer ")[1]
            # Verify the token with Firebase
            decoded_token = auth.verify_id_token(token)
            # Save user info (like user_id) for this request
            g.user = decoded_token
        except auth.InvalidIdTokenError:
            logger.warning("Invalid Firebase token received")
            abort(401, description="Invalid Firebase token")
        except Exception as e:
            logger.error(f"Error parsing auth header: {e}")
            abort(400, description="Invalid Authorization header")

        # If we get here, the token is valid. Run the endpoint function.
        return f(*args, **kwargs)

    return decorated_function


# --- End of new decorator ---


def register_routes(app):
    """Register all routes for the Flask app."""

    @app.route("/")
    def home():
        logger.info("Home route accessed")
        return jsonify({"message": "🚀 AutoSlides API is running!"})

    @app.route("/pdf2slides", methods=["POST"])
    def pdf2slides():
        logger.info("pdf2slides route accessed")
        """Handle PDF upload and convert to slides."""
        pdf_file = request.files.get("file")
        if not pdf_file or pdf_file.filename == "":
            return jsonify({"error": "No 'file' part in request"}), 400
        if not pdf_file.filename.lower().endswith(".pdf"):
            return jsonify({"error": "Please upload a PDF file"}), 400

        # Process the PDF
        try:
            pptx_bytes = pdf_to_slides(pdf_file)  # returns BytesIO buffer or bytes
            # upload the current generated ppt to s3
            upload_ppt_to_s3(ppt_bytes=pptx_bytes, user_id="test")
            url = generate_presigned_url(key="test.pptx")
            # obtain the presigned url for users to download
            return jsonify({"download_url": url}), 200
        except Exception as e:
            logger.exception("Failed to generate PPTX")
            return jsonify({"error": "Internal Parsing Error"}), 500

    # --- NEW: This is your new, protected endpoint ---
    @app.route("/protected/pdf2slides", methods=["POST"])
    @protected_by_firebase  # <-- This line enables the auth check
    def protected_pdf2slides():
        # 'g.user' is available here thanks to the decorator
        user_uid = g.user.get('uid', 'unknown_user')
        logger.info(f"PROTECTED pdf2slides route accessed by user: {user_uid}")

        """Handle PDF upload and convert to slides (Protected)."""
        pdf_file = request.files.get("file")
        if not pdf_file or pdf_file.filename == "":
            return jsonify({"error": "No 'file' part in request"}), 400
        if not pdf_file.filename.lower().endswith(".pdf"):
            return jsonify({"error": "Please upload a PDF file"}), 400

        # Process the PDF
        try:
            pptx_bytes = pdf_to_slides(pdf_file)

            logger.info(f"Skipping AWS S3 upload for protected route (user: {user_uid})")

            upload_ppt_to_s3(ppt_bytes=pptx_bytes, user_id=user_uid) # <-- COMMENTED OUT
            url = generate_presigned_url(key=f"{user_uid}.pptx")       # <-- COMMENTED OUT

            # Just return a success message instead of the S3 URL
            return jsonify({
                "message": "File processed successfully by protected route",
                "user_uid": user_uid
            }), 200

        except Exception as e:
            logger.exception(f"Failed to generate PPTX for user: {user_uid}")
            return jsonify({"error": "Internal Parsing Error"}), 500