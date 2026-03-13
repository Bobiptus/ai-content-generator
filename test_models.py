import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

print("Modelos disponibles:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"- {model.name}")