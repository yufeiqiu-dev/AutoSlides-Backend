import os
import google.generativeai as genai
from dotenv import load_dotenv


def generate_slide_content(paper_text: str) -> str:
    """
    Analyzes the text of a paper and generates structured slide content using the Gemini API.

    Args:
        paper_text: A string containing the full text from the paper.

    Returns:
        A string containing the structured slide content, ideally in JSON format.
    """
    # Load the environment variables from the .env file
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("Google API Key not found. Please set it in your .env file.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-pro-latest')

    # Create a detailed prompt for the LLM
    prompt = f"""
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

    try:
        # Send the prompt to the model
        response = model.generate_content(prompt)
        # Return the generated text
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error: Could not generate slide content."


if __name__ == '__main__':
    # A short example paper text for testing
    sample_paper = """
    Retrieval-Augmented Generation (RAG) is a technique for enhancing the accuracy and reliability
    of Large Language Models (LLMs) with facts fetched from external sources. It combines the strengths
    of pre-trained dense retrieval (retriever) and sequence-to-sequence models (generator).
    The retriever finds relevant documents from a knowledge base, and the generator uses this
    information along with the user's prompt to synthesize a comprehensive answer. This approach
    reduces hallucinations and allows for the integration of up-to-date information, making LLMs
    more powerful and trustworthy for real-world applications.
    """

    # Call the function and print the result
    slide_content = generate_slide_content(sample_paper)
    print("--- Generated Slide Content ---")
    print(slide_content)