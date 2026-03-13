from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')

if not api_key:
    print("❌ No se encontró GROQ_API_KEY en .env")
    exit(1)

print(f"✅ API Key encontrada (primeros 10 chars): {api_key[:10]}...")

try:
    client = Groq(api_key=api_key)
    
    print("🤖 Enviando request de prueba...")
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": "Di 'hola' en una palabra"
            }
        ],
        max_tokens=10
    )
    
    print(f"✅ Respuesta recibida: {response.choices[0].message.content}")
    print("\n🎉 ¡Groq funciona perfectamente!")
    
except Exception as e:
    print(f"❌ Error: {e}")