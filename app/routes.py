from flask import request, jsonify, send_file
from app.tools.pdf_to_slides import pdf_to_slides
from app.tools.pdf_parser import parse_pdf
import io

def register_routes(app):
    """Register all routes for the Flask app."""

    @app.route("/")
    def home():
        return jsonify({"message": "🚀 AutoSlides API is running!"})

    @app.route("/pdf2slides", methods=["POST"])
    def pdf2slides():
        """Handle PDF upload and convert to slides."""
        pdf_file = request.files.get("file")
        if not pdf_file in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        if pdf_file.filename == "":
            return jsonify({"error": "File has no name"}), 400
        if not pdf_file.filename.lower().endswith(".pdf"):
            return jsonify({"error": "Please upload a PDF file"}), 400

        pdf_file = request.files["file"]

        # Process the PDF
        pptx_bytes = pdf_to_slides(pdf_file)  # returns BytesIO buffer or bytes

        # Send back PowerPoint file
        return send_file(
            io.BytesIO(pptx_bytes),
            as_attachment=True,
            download_name="AutoSlides.pptx",
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    @app.route('/test_pdf_parsing', methods=["POST"])
    def test_pdf():
        pdf_file = request.files.get("file")
        if not pdf_file in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        if pdf_file.filename == "":
            return jsonify({"error": "File has no name"}), 400
        if not pdf_file.filename.lower().endswith(".pdf"):
            return jsonify({"error": "Please upload a PDF file"}), 400

        parsed = parse_pdf(pdf_file)
        text = parsed["text"]

        # Return text directly
        return jsonify({"text": text})