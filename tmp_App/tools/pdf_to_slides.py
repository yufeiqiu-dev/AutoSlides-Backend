from .pdf_parser import parse_pdf
def pdf_to_slides(pdf_file):
    # convert pdf to slides using LLM
    
    # step 1: parse pdf into text and images
    parsed = parse_pdf(pdf_file)
    text = parsed["text"]

    image = parsed["image"]
    # step 2: feed LLM with the text and image to generate slide by slide with text and image

    # step 3: convert the result into ppt

    # return slides