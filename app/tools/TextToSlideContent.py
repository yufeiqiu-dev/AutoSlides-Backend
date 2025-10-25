import os
import google.generativeai as genai
from dotenv import load_dotenv


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
    """


def generate_slide_content(paper_text: str) -> str:
    """
    Analyzes paper text and generates structured slide content using the Gemini API.
    """
    if not paper_text:
        raise ValueError("Paper text cannot be empty.")

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API Key not found. Please set it in your .env file.")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-pro-latest')
        prompt = build_prompt(paper_text)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error: Could not generate slide content."