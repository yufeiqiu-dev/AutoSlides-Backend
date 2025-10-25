import pdfplumber
from io import BytesIO
import fitz

def parse_pdf(pdf_file):
    """Parse pdf to text and images"""
    pdf_bytes = pdf_file.read()
    parsed = {}
    text = extract_text(pdf_bytes)
    # extract image once text works
    image = extract_images(pdf_bytes)
    parsed["text"] = text
    parsed["image"] = image
    return parsed
def extract_text(pdf_bytes):
    """Extract text"""
    all_text = []
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)
    return "\n\n".join(all_text)


def extract_images(pdf_bytes):
    """Extract image"""
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