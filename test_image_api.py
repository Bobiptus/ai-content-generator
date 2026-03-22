import os
import sys
import json
import base64
import urllib.request
import ssl

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
api_token = os.getenv('CLOUDFLARE_API_TOKEN')

print(f"Account ID: {account_id}")
print(f"API Token: {api_token[:10]}..." if api_token else "No token")

if not account_id or not api_token:
    print("ERROR: Faltan credenciales en .env")
    sys.exit(1)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0"

print(f"\nURL: {url}")

prompt = "a cat"
data = json.dumps({"prompt": prompt}).encode('utf-8')

req = urllib.request.Request(
    url,
    data=data,
    headers={
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    },
    method='POST'
)

print(f"\nEnviando request...")
print(f"Prompt: {prompt}")

try:
    with urllib.request.urlopen(req, timeout=120, context=ctx) as response:
        response_data = response.read()
        print(f"\nRespuesta recibida: {len(response_data)} bytes")
        print(f"Primeros 100 bytes: {response_data[:100]}")
        
        # Intentar parsear como JSON
        try:
            result = json.loads(response_data.decode('utf-8'))
            print(f"\nJSON parsed OK")
            print(f"Success: {result.get('success')}")
            if result.get('result'):
                print(f"Tiene imagen: {'image' in result.get('result', {})}")
        except:
            print(f"\nNo es JSON, intentando como imagen directa...")
            with open("test_image.png", 'wb') as f:
                f.write(response_data)
            print("Imagen guardada como test_image.png")
            
except Exception as e:
    print(f"\nERROR: {type(e).__name__}: {e}")
