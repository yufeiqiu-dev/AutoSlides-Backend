# app.py
from flask import Flask, request, send_file, jsonify
from app.tools.pdf_to_slides import pdf_to_slides

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/pdf2slides', method=["POST"])
def pdf_to_slides():
    """Receive PDF, parse it, summarize, and return PowerPoint."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files["file"]


    slides = pdf_to_slides(pdf_file)

    # send file to user
    return send_file(
        slides,
        as_attachment=True,
        download_name="AutoSlide.pptx",
        mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

if __name__ == '__main__':
    app.run(debug=True) # debug=True enables debug mode for development