import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("Google API Key not found. Please set it in your .env file.")

# Configure the Gemini API with your key
genai.configure(api_key=api_key)

print("--- Available Models for Content Generation ---")

# List all models and filter for the ones that can generate content
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(model.name)

print("---------------------------------------------")