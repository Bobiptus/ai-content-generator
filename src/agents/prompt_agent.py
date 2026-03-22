from typing import Dict, Any, List
import re


class PromptAgent:
    """
    Agente que analiza el contenido del artículo y genera prompts optimizados para imágenes.
    Sin costo de API - usa procesamiento de texto en Python.
    """
    
    # Palabras clave -> conceptos visuales
    VISUAL_MAPPINGS = {
        'tecnologia': ['technology', 'digital', 'modern devices', 'screens'],
        'negocios': ['business', 'professional', 'office', 'growth'],
        'finanzas': ['finance', 'money', 'charts', 'investment'],
        'salud': ['health', 'wellness', 'medical', 'care'],
        'educacion': ['education', 'learning', 'books', 'knowledge'],
        'naturaleza': ['nature', 'outdoors', 'environment', 'earth'],
        'mar': ['ocean', 'sea', 'waves', 'beach', 'water'],
        'vida': ['life', 'living', 'daily life', 'lifestyle'],
        'familia': ['family', 'together', 'loved ones', 'home'],
        'seguro': ['protection', 'security', 'shield', 'safety'],
        'ahorro': ['saving', 'piggy bank', 'coins', 'financial'],
        'futuro': ['future', 'tomorrow', 'forward thinking', 'horizon'],
        'mexico': ['mexican', 'latin america', 'culture'],
        'python': ['code', 'programming', 'computer', 'development'],
        'ia': ['artificial intelligence', 'AI', 'neural networks', 'robotics'],
        'cocina': ['cooking', 'kitchen', 'food', 'culinary'],
        'deportes': ['sports', 'athletic', 'fitness', 'exercise'],
        'musica': ['music', 'musical', 'sound', 'rhythm'],
        'arte': ['art', 'creative', 'painting', 'design'],
        'viaje': ['travel', 'adventure', 'exploration', 'journey']
    }
    
    # Emociones -> estilos visuales
    EMOTION_STYLES = {
        'positivo': ['bright', 'vibrant', 'warm', 'inspiring'],
        'negativo': ['dark', 'serious', 'dramatic'],
        'neutral': ['clean', 'minimalist', 'balanced'],
        'urgente': ['bold', 'dynamic', 'energetic'],
        'calmado': ['peaceful', 'serene', 'soft colors'],
        'profesional': ['corporate', 'clean', 'trustworthy']
    }
    
    def __init__(self):
        self.min_word_importance = 3
    
    def analyze_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analiza el artículo y extrae información para generar prompts de imágenes.
        """
        full_text = self._combine_text(article)
        keywords = self._extract_keywords(full_text)
        emotions = self._detect_emotions(full_text)
        visual_concepts = self._map_to_visuals(keywords)
        
        return {
            'keywords': keywords,
            'emotions': emotions,
            'visual_concepts': visual_concepts,
            'topic': article.get('topic', ''),
            'title': article.get('title', '')
        }
    
    def _combine_text(self, article: Dict[str, Any]) -> str:
        """Combina todo el texto del artículo."""
        parts = []
        
        if article.get('title'):
            parts.append(article['title'])
        if article.get('introduction'):
            parts.append(article['introduction'])
        if article.get('conclusion'):
            parts.append(article['conclusion'])
        if article.get('outline'):
            parts.append(article['outline'])
        
        for section in article.get('sections', []):
            if section.get('title'):
                parts.append(section['title'])
            if section.get('content'):
                parts.append(section['content'])
        
        return ' '.join(parts).lower()
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extrae palabras clave importantes del texto."""
        # Palabras comunes a ignorar
        stopwords = {
            'el', 'la', 'los', 'las', 'de', 'en', 'y', 'a', 'que', 'es',
            'un', 'una', 'por', 'con', 'para', 'se', 'su', 'del', 'al',
            'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este',
            'si', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre',
            'también', 'me', 'hasta', 'hay', 'donde', 'quien', 'desde',
            'todo', 'nos', 'durante', 'todos', 'uno', 'les', 'ni', 'contra',
            'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mi',
            'antes', 'some', 'many', 'most', 'other', 'very', 'just',
            'can', 'will', 'should', 'could', 'would', 'may', 'might',
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
            'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was',
            'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
            'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where',
            'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
            'most', 'other', 'some', 'such', 'no', 'not', 'only', 'same',
            'so', 'than', 'too', 'very', 'just', 'about', 'also'
        }
        
        # Extraer palabras
        words = re.findall(r'\b[a-záéíóúñü]+\b', text)
        
        # Filtrar y contar
        word_count = {}
        for word in words:
            if len(word) > 3 and word not in stopwords:
                word_count[word] = word_count.get(word, 0) + 1
        
        # Ordenar por importancia
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, count in sorted_words[:15]]
    
    def _detect_emotions(self, text: str) -> List[str]:
        """Detecta emociones/tóno del artículo."""
        emotion_indicators = {
            'positivo': ['beneficio', 'mejor', 'importante', 'ayuda', 'bien', 
                        'excelente', 'oportunidad', 'positivo', 'bueno', 'mejorar',
                        'success', 'benefit', 'important', 'good', 'better', 'help'],
            'negativo': ['problema', 'error', 'malo', 'difícil', 'riesgo',
                        'danger', 'problem', 'risk', 'difficult', 'bad'],
            'urgente': ['urgente', 'ahora', 'rápido', 'inmediato',
                       'urgent', 'now', 'quick', 'immediately'],
            'calmado': ['tranquilo', 'paz', 'sereno', 'relajado',
                       'peaceful', 'calm', 'relaxed', 'serene'],
            'profesional': ['profesional', 'experto', 'técnico', 'serio',
                           'professional', 'expert', 'technical', 'serious']
        }
        
        detected = []
        for emotion, indicators in emotion_indicators.items():
            if any(ind in text for ind in indicators):
                detected.append(emotion)
        
        if not detected:
            detected = ['neutral']
        
        return detected
    
    def _map_to_visuals(self, keywords: List[str]) -> List[str]:
        """Convierte palabras clave a conceptos visuales."""
        visuals = []
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            for theme, visual_list in self.VISUAL_MAPPINGS.items():
                if theme in keyword_lower or keyword_lower in theme:
                    visuals.extend(visual_list[:2])
                    break
            else:
                # Si no hay mapping, usar la palabra clave directamente
                visuals.append(keyword)
        
        return list(set(visuals))[:8]
    
    def generate_article_prompt(self, article: Dict[str, Any]) -> str:
        """
        Genera un prompt optimizado para imagen de artículo.
        """
        analysis = self.analyze_article(article)
        
        # Construir prompt
        parts = []
        
        # Tema principal
        topic = analysis['topic']
        parts.append(f"Beautiful illustration about '{topic}'")
        
        # Conceptos visuales
        if analysis['visual_concepts']:
            concepts = ', '.join(analysis['visual_concepts'][:4])
            parts.append(f"Concepts: {concepts}")
        
        # Estilo basado en emociones
        emotions = analysis['emotions']
        if 'profesional' in emotions:
            parts.append("Professional style, clean design")
        elif 'calmado' in emotions:
            parts.append("Peaceful atmosphere, soft colors")
        elif 'urgente' in emotions:
            parts.append("Dynamic, energetic composition")
        else:
            parts.append("Modern minimalist design, high quality")
        
        # Agregar título si está disponible
        title = analysis.get('title', '')
        if title:
            parts.append(f"Related to: '{title}'")
        
        # Restricciones
        parts.append("No text, no people, no faces")
        parts.append("Professional blog cover style")
        
        return '. '.join(parts)
    
    def generate_social_prompt(self, article: Dict[str, Any], platform: str) -> str:
        """
        Genera un prompt optimizado para imagen de redes sociales.
        """
        analysis = self.analyze_article(article)
        
        parts = []
        topic = analysis['topic']
        
        # Tamaño según plataforma
        sizes = {
            'instagram': 'square format, 1:1',
            'twitter': 'landscape format, 16:9',
            'facebook': 'landscape format, 16:9',
            'linkedin': 'landscape format, 16:9'
        }
        
        parts.append(f"Social media post about '{topic}'")
        parts.append(f"Format: {sizes.get(platform, 'square')}")
        
        # Conceptos visuales
        if analysis['visual_concepts']:
            concepts = ', '.join(analysis['visual_concepts'][:3])
            parts.append(f"Elements: {concepts}")
        
        # Estilo
        if analysis['emotions']:
            parts.append("Eye-catching, vibrant colors")
            parts.append("Modern social media aesthetic")
        
        parts.append("No text, no people")
        
        return ', '.join(parts)


def main():
    """Test del PromptAgent"""
    agent = PromptAgent()
    
    test_article = {
        'topic': 'seguros de vida en México',
        'title': 'La Importancia de los Seguros de Vida',
        'introduction': 'Los seguros de vida son fundamentales para proteger a tu familia...',
        'conclusion': 'En conclusión, tener un seguro de vida es una decisión inteligente...',
        'outline': '1. ¿Qué es un seguro de vida?\n2. Beneficios para tu familia\n3. Cómo elegir el mejor'
    }
    
    print("=== Análisis del PromptAgent ===\n")
    
    analysis = agent.analyze_article(test_article)
    print("Keywords:", analysis['keywords'])
    print("Emotions:", analysis['emotions'])
    print("Visuals:", analysis['visual_concepts'])
    
    print("\n--- Prompt para Artículo ---")
    print(agent.generate_article_prompt(test_article))
    
    print("\n--- Prompt para Instagram ---")
    print(agent.generate_social_prompt(test_article, 'instagram'))


if __name__ == "__main__":
    main()
