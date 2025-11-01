import os, time
import google.generativeai as genai
import json
import re
from dotenv import load_dotenv
from app.utils.logger import get_logger
logger = get_logger("Gemini")

def build_prompt(paper_text: str) -> str:
    """Creates the detailed prompt for the Gemini API."""
    return f"""
    You are an expert presentation creator. 
    Your task is to analyze the following academic paper text and generate 
    content for a slide presentation. The output must be a clean, structured text format like JSON, 
    without any extra explanations.

    The structure should be:
    - A main title for the presentation.
    - A series of slides, each with a header and 3-5 key bullet points.

    Here is the paper text:
    ---
    {paper_text}
    ---

    Generate the presentation content based on this text.
    Return only valid JSON, do not include stuff like '''json. 
    Do not include code fences, explanations, or text before/after. 
    If you cannot produce valid JSON, return {{}}.
    Please respond in **valid JSON** format as shown below:

    {{
    "title": "example title",
    "slides": [
        {{
        "header": "Example Header",
        "bullets": [
            "First point",
            "Second point"
        ]
        }}
    ]
    }}
    
    """
def get_genai_model():
    """Return a configured Gemini model or raise error if key missing."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.exception("Cannot find Gemini API Key")
        raise ValueError("Google API Key not found. Please set it in your .env file.")

    genai.configure(api_key=api_key)
    return genai.GenerativeModel('models/gemini-pro-latest')
def parse_text_to_json(text:str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in response.")
    
    cleaned = match.group(0)
    try:
        data = json.loads(cleaned)
    except Exception as e:
        raise ValueError("JSON cannot be parsed {e}")
    return data
def generate_slide_content(paper_text: str) -> str:
    """
    Analyzes paper text and generates structured slide content using the Gemini API.
    """
    logger.info("Generating slide content using gemini API")
    if not paper_text:
        raise ValueError("Paper text cannot be empty.")

    try:
        start = time.time()
        model = get_genai_model()
        prompt = build_prompt(paper_text)
        response = model.generate_content(prompt)
        elapsed = time.time() - start
        logger.info(f"Response got from LLM in {elapsed:.2f} seconds")
        json_text = response.text
        logger.info("Parsing output into json")
        json = parse_text_to_json(json_text)
        logger.info("LLM output successfully parsed to json")
        logger.debug(json)
        return json
    except Exception as e:
        print(f"An error occurred: {e}")
        raise ValueError(f"Error: {e}")