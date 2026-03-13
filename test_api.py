"""
Script de diagnóstico para Google Gemini API
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

print("="*70)
print("🔍 DIAGNÓSTICO DE GOOGLE GEMINI API")
print("="*70)

# 1. Verificar que la API key existe
api_key = os.getenv('GOOGLE_API_KEY')
print(f"\n1. ¿Existe GOOGLE_API_KEY en .env? {'✅ SÍ' if api_key else '❌ NO'}")

if api_key:
    print(f"   Primeros 10 caracteres: {api_key[:10]}...")
    print(f"   Longitud total: {len(api_key)} caracteres")
    
    # 2. Configurar la API
    try:
        genai.configure(api_key=api_key)
        print("\n2. ¿Se pudo configurar la API? ✅ SÍ")
    except Exception as e:
        print(f"\n2. ¿Se pudo configurar la API? ❌ NO")
        print(f"   Error: {e}")
        exit(1)
    
    # 3. Listar modelos disponibles
    print("\n3. Listando modelos disponibles...")
    try:
        models = []
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                models.append(model.name)
        
        if models:
            print(f"   ✅ Se encontraron {len(models)} modelos")
            print("\n   Modelos disponibles:")
            for m in models[:5]:  # Mostrar solo los primeros 5
                print(f"   - {m}")
        else:
            print("   ❌ No se encontraron modelos disponibles")
            print("   ⚠️ Posible problema con la API key")
    except Exception as e:
        print(f"   ❌ Error al listar modelos: {e}")
        exit(1)
    
    # 4. Intentar una generación simple
    print("\n4. Probando generación de contenido...")
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-image')
        response = model.generate_content("Di 'hola' en una palabra")
        
        print(f"   ✅ Generación exitosa!")
        print(f"   Respuesta: {response.text}")
        
    except Exception as e:
        error_msg = str(e)
        print(f"   ❌ Error en generación: {error_msg}")
        
        # Diagnóstico específico del error
        if "429" in error_msg:
            print("\n   🔴 DIAGNÓSTICO: Error 429 - Too Many Requests")
            print("   Causas posibles:")
            print("   - Has excedido el límite de 15 requests/minuto")
            print("   - Has excedido el límite de 1,500 requests/día")
            print("   - Solución: Espera 1 hora y vuelve a intentar")
            
        elif "403" in error_msg or "permission" in error_msg.lower():
            print("\n   🔴 DIAGNÓSTICO: Error de permisos")
            print("   Causas posibles:")
            print("   - La API key no tiene permisos habilitados")
            print("   - La API key fue revocada")
            print("   - Solución: Crear una nueva API key")
            
        elif "invalid" in error_msg.lower() or "401" in error_msg:
            print("\n   🔴 DIAGNÓSTICO: API key inválida")
            print("   Causas posibles:")
            print("   - La API key está mal copiada")
            print("   - La API key expiró")
            print("   - Solución: Crear una nueva API key")
            
        elif "404" in error_msg:
            print("\n   🔴 DIAGNÓSTICO: Modelo no encontrado")
            print("   Causas posibles:")
            print("   - El nombre del modelo es incorrecto")
            print("   - El modelo no está disponible en tu región")
            print("   - Solución: Usar otro modelo de la lista")
        
        else:
            print(f"\n   🔴 DIAGNÓSTICO: Error desconocido")
            print(f"   Error completo: {error_msg}")

print("\n" + "="*70)
print("✅ Diagnóstico completado")
print("="*70)