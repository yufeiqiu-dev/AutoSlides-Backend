from .pdf_parser import parse_pdf
from app.tools.JsonToPPT import json_to_ppt_bytes
from app.tools.TextToSlideContent import generate_slide_content
from app.utils.logger import get_logger
logger = get_logger("PDF to PPTX")
def pdf_to_slides(pdf_file):
    """Convert a PDF file into slide deck bytes using the LLM pipeline."""
    filename = getattr(pdf_file, "filename", "unknown")
    logger.info(f"Starting PDF to slides conversion for {filename}")

    try:
        # Step 1: Parse PDF into text and images
        parsed = parse_pdf(pdf_file)
        text = parsed.get("text", "")
        images = parsed.get("image", [])
        logger.info(f"Successfully parsed PDF {filename}: {len(text)} chars, {len(images)} images")

        # Step 2: Generate structured slide content using LLM
        json_data = generate_slide_content(text)
        logger.info(f"Successfully generated slide JSON content for {filename}")

        # Step 3: Convert JSON to PPT bytes
        ppt_bytes = json_to_ppt_bytes(json_data)
        logger.info(f"Successfully generated PPTX bytes for {filename}")

        return ppt_bytes

    except ValueError as e:
        # Custom known errors (e.g., no API key, empty text)
        logger.exception(f"ValueError during conversion for {filename}: {e}")
        raise

    except Exception as e:
        # Catch-all to prevent 500 without trace
        logger.exception(f"Unexpected error processing {filename}: {e}")
        raise ValueError(f"Internal conversion error for {filename}: {e}")
