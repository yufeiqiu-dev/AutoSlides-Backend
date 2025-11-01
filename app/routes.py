from flask import request, jsonify, send_file
from app.tools.pdf_to_slides import pdf_to_slides
from app.tools.pdf_parser import parse_pdf
from app.tools.TextToSlideContent import generate_slide_content
from app.utils.logger import get_logger
import io

logger = get_logger("AutoSlides")
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
        if pdf_file.filename == "":
            return jsonify({"error": "File has no name"}), 400
        if not pdf_file.filename.lower().endswith(".pdf"):
            return jsonify({"error": "Please upload a PDF file"}), 400

        pdf_file = request.files["file"]

        # Process the PDF
        try:
            pptx_bytes = pdf_to_slides(pdf_file)  # returns BytesIO buffer or bytes
            pptx_bytes.seek(0) # ensure pointer at start
        except Exception as e:
            logger.exception("Failed to generate PPTX")
            return jsonify({"error": "Internal Parsing Error"}), 500

        # Send back PowerPoint file
        return send_file(
            pptx_bytes,
            as_attachment=True,
            download_name="AutoSlides.pptx",
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )