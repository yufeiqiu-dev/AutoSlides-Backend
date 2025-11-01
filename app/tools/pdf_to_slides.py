from .pdf_parser import parse_pdf
from app.tools.JsonToPPT import json_to_ppt_bytes
from app.tools.TextToSlideContent import generate_slide_content
from app.utils.logger import get_logger
logger = get_logger("PDF to PPTX")
def pdf_to_slides(pdf_file):
    # convert pdf to slides using LLM
    filename = pdf_file.filename
    # step 1: parse pdf into text and images
    parsed = parse_pdf(pdf_file)
    logger.info(f"Successfully parsed pdf {filename}")
    text = parsed["text"]
    image = parsed["image"]
    # step 2: feed LLM with the text and image to generate slide by slide with text and image
    json_data = generate_slide_content(text)
    logger.info(f"Successfully Generated slides content to json for {filename}")
    # step 3: convert the result into ppt
    ppt_bytes = json_to_ppt_bytes(json_data)
    logger.info(f"Successfully generated pptx bytes data for {filename}")
    # return slides
    return ppt_bytes