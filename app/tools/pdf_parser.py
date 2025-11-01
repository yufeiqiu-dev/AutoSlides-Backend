import pdfplumber
from io import BytesIO
import fitz
from app.utils.logger import get_logger
import time
logger = get_logger("PDF Parser")
def parse_pdf(pdf_file):
    """Parse pdf to text and images"""
    print("DEBUG - pdf_file is:", type(pdf_file))
    if not pdf_file:
        raise FileNotFoundError("PDF File Doesn't exist!")
    pdf_bytes = pdf_file.read()

    if not pdf_bytes:
        raise ValueError("Empty PDF content")
    logger.info(f"--- Parsing {pdf_file.filename} ---")
    parsed = {}
    start = time.time()
    text = extract_text(pdf_bytes)
    # extract image once text works
    image = extract_images(pdf_bytes)
    elapsed = time.time() - start
    logger.info(f"PDF parsing completed in {elapsed:.2f} seconds")
    parsed["text"] = text
    parsed["image"] = image
    return parsed
def extract_text(pdf_bytes):
    """Extract text"""
    logger.info("Extracting text...")
    all_text = []
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)
    return "\n\n".join(all_text)


def extract_images(pdf_bytes):
    """Extract image"""
    logger.info("Extracting image")
    images = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page_index, page in enumerate(doc):
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_img = doc.extract_image(xref)
                image_bytes = base_img["image"]
                ext = base_img["ext"]
                images.append({
                    "page": page_index + 1,
                    "ext": ext,
                    "bytes": image_bytes
                })
    return images