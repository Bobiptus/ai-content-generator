"""
Script para generar artículos completos
"""

import os
import sys
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.content_generator import ContentGenerator

def clear_screen():
    """Limpia la pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Imprime el encabezado"""
    print("=" * 70)
    print("📰 GENERADOR DE ARTÍCULOS COMPLETOS CON IA")
    print("=" * 70)
    print()

def format_article_markdown(article):
    """
    Formatea el artículo en Markdown
    
    Args:
        article (dict): El artículo generado
        
    Returns:
        str: El artículo en formato Markdown
    """
    markdown = f"""# {article['title']}

**Tema:** {article['topic']}  
**Tono:** {article['tone']}  
**Palabras:** ~{article['word_count']}  
**Fecha:** {datetime.now().strftime('%Y-%m-%d')}

---

## Introducción

{article['introduction']}

---

"""
    
    # Agregar secciones si existen
    for i, section in enumerate(article['sections'], 1):
        markdown += f"## {section['title']}\n\n{section['content']}\n\n---\n\n"
    
    markdown += f"""## Conclusión

{article['conclusion']}

---

*Artículo generado automáticamente con IA*
"""
    
    return markdown

def save_article(article, format='markdown'):
    """
    Guarda el artículo en archivo
    
    Args:
        article (dict): El artículo a guardar
        format (str): Formato del archivo (markdown, txt)
        
    Returns:
        str: Ruta del archivo guardado
    """
    # Crear nombre de archivo seguro
    safe_topic = "".join(c for c in article['topic'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_topic = safe_topic.replace(' ', '_')
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format == 'markdown':
        filename = f"outputs/article_{safe_topic}_{timestamp}.md"
        content = format_article_markdown(article)
    else:
        filename = f"outputs/article_{safe_topic}_{timestamp}.txt"
        content = f"""TÍTULO: {article['title']}
TEMA: {article['topic']}
TONO: {article['tone']}
FECHA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
PALABRAS: ~{article['word_count']}
{"="*70}

INTRODUCCIÓN:
{article['introduction']}

{"="*70}

CONCLUSIÓN:
{article['conclusion']}

{"="*70}
*Artículo generado automáticamente con IA*
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename

def main():
    """Función principal"""
    clear_screen()
    print_header()
    
    try:
        use_research = False
        print("🔧 Inicializando sistema...")
        
        try:
            generator = ContentGenerator(provider="groq", enable_research=True)
            use_research = True
            print("✅ Sistema listo (con búsqueda web)")
        except Exception as e:
            print(f"⚠️ Búsqueda web no disponible: {e}")
            generator = ContentGenerator(provider="groq")
            print("✅ Sistema listo (sin búsqueda web)")
        
        print()
        
        print("📝 Configuración del artículo:")
        print("-" * 70)
        
        topic = input("Tema del artículo: ").strip()
        if not topic:
            print("❌ Debes ingresar un tema")
            return
        
        if use_research:
            print("\n¿Deseas buscar información actualizada en la web?")
            print("  1. Sí (recomendado - información más actualizada)")
            print("  2. No (usar solo conocimiento del modelo)")
            research_choice = input("Elige (1-2) [1]: ").strip() or "1"
            use_research = (research_choice == "1")
        else:
            use_research = False
        
        print("\nTonos disponibles:")
        print("  1. Profesional")
        print("  2. Casual")
        print("  3. Técnico")
        tone_choice = input("Elige el tono (1-3) [1]: ").strip() or "1"
        
        tones = {"1": "profesional", "2": "casual", "3": "técnico"}
        tone = tones.get(tone_choice, "profesional")
        
        research_info = "con investigación web" if use_research else "sin investigación"
        
        print("\n" + "="*70)
        print(f"🤖 Generando artículo completo sobre: '{topic}'")
        print(f"📊 Tono: {tone}")
        print(f"🔍 Modo: {research_info}")
        print("⏳ Esto tomará 30-90 segundos...")
        print("="*70)
        
        article = generator.generate_full_article(topic, tone, use_research=use_research)
        
        # Verificar si hubo error
        if "error" in article:
            print(f"\n❌ {article['error']}")
            return
        
        # Mostrar resultado
        print("\n" + "="*70)
        print("✅ ARTÍCULO GENERADO EXITOSAMENTE")
        print("="*70)
        print(f"\n📊 Estadísticas:")
        print(f"   - Título: {article['title']}")
        print(f"   - Palabras: ~{article['word_count']}")
        print(f"   - Secciones: {len(article['sections'])}")
        
        if article.get('research_data') and article['research_data'].get('sources'):
            sources = article['research_data']['sources']
            print(f"   - Fuentes consultadas: {len(sources)}")
        
        # Guardar artículo
        filename_md = save_article(article, format='markdown')
        filename_txt = save_article(article, format='txt')
        
        print(f"\n💾 Guardado en:")
        print(f"   - Markdown: {filename_md}")
        print(f"   - Texto: {filename_txt}")
        
        # Preguntar si quiere ver el contenido
        view = input("\n¿Quieres ver el artículo completo? (s/n): ").strip().lower()
        if view == 's':
            print("\n" + "="*70)
            print(format_article_markdown(article))
            print("="*70)
        
        print("\n✅ ¡Proceso completado exitosamente!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Proceso cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n💡 Verifica que:")
        print("   - Tu GOOGLE_API_KEY esté correcta en .env")
        print("   - Tengas conexión a internet")
        print("   - No hayas excedido los límites de la API (espera 1 minuto)")

if __name__ == "__main__":
    main()