"""
Script principal del sistema de generación de contenido
"""

import os
import sys
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.content_generator import ContentGenerator

def clear_screen():
    """Limpia la pantalla de la terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Imprime el encabezado del programa"""
    print("=" * 60)
    print("🤖 SISTEMA DE GENERACIÓN DE CONTENIDO CON IA")
    print("=" * 60)
    print()

def save_to_file(content, topic):
    """
    Guarda el contenido generado en un archivo
    
    Args:
        content (str): El contenido a guardar
        topic (str): El tema (para el nombre del archivo)
    """
    # Crear nombre de archivo seguro
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_topic = safe_topic.replace(' ', '_')
    
    # Crear nombre con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"outputs/outline_{safe_topic}_{timestamp}.txt"
    
    # Guardar archivo
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"TEMA: {topic}\n")
        f.write(f"FECHA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(content)
    
    return filename

def main():
    """Función principal"""
    clear_screen()
    print_header()
    
    try:
        # Inicializar generador
        print("🔧 Inicializando sistema...")
        generator = ContentGenerator()
        print("✅ Sistema listo\n")
        
        # Solicitar tema al usuario
        print("📝 ¿Sobre qué tema quieres generar un artículo?")
        topic = input("Tema: ").strip()
        
        if not topic:
            print("❌ Debes ingresar un tema")
            return
        
        print(f"\n🤖 Generando outline sobre: '{topic}'")
        print("⏳ Esto tomará unos segundos...\n")
        
        # Generar outline
        outline = generator.generate_article_outline(topic)
        
        # Mostrar resultado
        print("=" * 60)
        print("OUTLINE GENERADO:")
        print("=" * 60)
        print(outline)
        print("=" * 60)
        
        # Guardar en archivo
        filename = save_to_file(outline, topic)
        print(f"\n💾 Guardado en: {filename}")
        
        print("\n✅ ¡Generación completada exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n💡 Verifica que:")
        print("   - Tu GOOGLE_API_KEY esté correcta en .env")
        print("   - Tengas conexión a internet")
        print("   - Las dependencias estén instaladas")

if __name__ == "__main__":
    main()