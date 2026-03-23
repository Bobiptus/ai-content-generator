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
        'viaje': ['travel', 'adventure', 'exploration', 'journey'],
        'auto': ['car', 'vehicle', 'driving', 'road'],
        'hogar': ['home', 'house', 'family', 'living room'],
        'comida': ['food', 'meal', 'restaurant', 'kitchen'],
        'moda': ['fashion', 'clothing', 'style', 'elegant']
    }
    
    # Categorías de tono visual
    VISUAL_TONES = {
        'SERIO_PROFESIONAL': {
            'keywords': ['seguro', 'dinero', 'finanza', 'legal', 'trabajo', 'banco', 'inversión', 
                        'business', 'finance', 'money', 'legal', 'bank', 'investment', 'profesional',
                        'seguro', 'beneficio', 'patrimonio', 'economía', 'ahorro'],
            'colors': 'dark blue, gray, white, navy blue',
            'style': 'corporate, clean, trustworthy, professional',
            'description': 'professional, clean, trustworthy'
        },
        'CASUAL_DIVERTIDO': {
            'keywords': ['fiesta', 'vacaciones', 'diversión', 'entretenimiento', 'celebración',
                        'party', 'vacation', 'fun', 'entertainment', 'celebration', 'celebrar',
                        'amor', 'feliz', 'disfrutar', 'relax'],
            'colors': 'bright colors, vibrant, saturated, warm',
            'style': 'casual, fun, energetic, friendly',
            'description': 'casual, fun, vibrant colors, energetic'
        },
        'LUJOSO_PREMIUM': {
            'keywords': ['lujo', 'exclusivo', 'premium', 'elegante', 'alta gama',
                        'luxury', 'exclusive', 'premium', 'elegant', 'high-end', 'expensive',
                        'VIP', 'diamante', 'oro', 'exclusive'],
            'colors': 'black, gold, silver, dark purple',
            'style': 'luxury, elegant, premium, sophisticated',
            'description': 'luxury, elegant, premium, sophisticated'
        },
        'INFANTIL_FAMILIAR': {
            'keywords': ['niños', 'educación', 'aprender', 'infantil', 'juguete',
                        'kids', 'children', 'education', 'learning', 'playful',
                        'escuela', 'juego', 'amigo', 'nube', 'estrella'],
            'colors': 'pastel colors, light blue, pink, yellow',
            'style': 'playful, friendly, colorful, childlike',
            'description': 'playful, friendly, colorful, childlike'
        },
        'TECNOLOGICO': {
            'keywords': ['tecnología', 'digital', 'software', 'IA', 'inteligencia', 'código',
                        'technology', 'digital', 'software', 'AI', 'computer', 'code', 'tech',
                        'app', 'internet', 'robot', 'futuro'],
            'colors': 'electric blue, cyan, green neon, purple',
            'style': 'futuristic, modern, sleek, tech-inspired',
            'description': 'futuristic, modern, tech, sleek'
        },
        'NATURAL_ECOLOGICO': {
            'keywords': ['naturaleza', 'ambiente', 'ecología', 'verde', 'animal', 'planta',
                        'nature', 'environment', 'green', 'ecology', 'animal', 'tree',
                        'bosque', 'flor', 'mar', 'playa', 'sol'],
            'colors': 'green, brown, sky blue, natural tones',
            'style': 'organic, natural, fresh, eco-friendly',
            'description': 'organic, natural, fresh, eco-friendly'
        },
        'SALUD_BIENESTAR': {
            'keywords': ['salud', 'bienestar', 'médico', 'ejercicio', 'deporte', 'vida sana',
                        'health', 'wellness', 'medical', 'exercise', 'fitness', 'healthy',
                        'doctor', 'hospital', 'medicina', 'corazón', 'neuro',
                        'neuropsicología', 'autismo', 'diagnóstico', 'cerebro', 'terapia',
                        'tratamiento', 'paciente', 'clínico', 'psychology', 'brain',
                        'mental', 'cognitive', 'developmental', 'infantil',
                        'detección', 'temprana', 'edad', 'niños', 'children', 'pediátrico',
                        'developmental', 'autism', 'early intervention', 'screening'],
            'colors': 'white, light green, blue, teal',
            'style': 'clean, professional, caring, fresh',
            'description': 'clean, fresh, professional, caring'
        },
        'HOGAR_FAMILIAR': {
            'keywords': ['hogar', 'casa', 'domicilio', 'vivienda',
                        'home', 'house', 'living room', 'kitchen',
                        'apartamento', 'interior', 'mueble'],
            'colors': 'warm brown, beige, orange, cream',
            'style': 'warm, cozy, welcoming, domestic',
            'description': 'warm, cozy, welcoming, domestic'
        }
    }
    
    # Prioridad de tonos cuando el artículo es profesional
    # (orden: mayor prioridad primero)
    PROFESIONAL_PRIORITY = [
        'SALUD_BIENESTAR',  # Primero salud
        'SERIO_PROFESIONAL',  # Luego serio general
        'TECNOLOGICO',
        'NATURAL_ECOLOGICO',
        'HOGAR_FAMILIAR',
        'CASUAL_DIVERTIDO',
        'INFANTIL_FAMILIAR',
        'LUJOSO_PREMIUM'
    ]
    
    # Mapeo de tono de artículo a tono visual
    ARTICLE_TONE_TO_VISUAL = {
        'profesional': 'SERIO_PROFESIONAL',
        'casual': 'CASUAL_DIVERTIDO',
        'técnico': 'TECNOLOGICO'
    }
    
    def __init__(self):
        self.min_word_importance = 3
    
    def analyze_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analiza el artículo y extrae información para generar prompts de imágenes.
        """
        full_text = self._combine_text(article)
        keywords = self._extract_keywords(full_text)
        visual_concepts = self._map_to_visuals(keywords)
        
        # Detectar tono visual
        article_tone = article.get('tone', 'profesional')
        visual_tone = self._detect_visual_tone(keywords, article_tone, full_text)
        
        return {
            'keywords': keywords,
            'visual_concepts': visual_concepts,
            'visual_tone': visual_tone,
            'article_tone': article_tone,
            'topic': article.get('topic', ''),
            'title': article.get('title', '')
        }
    
    def _detect_visual_tone(self, keywords: List[str], article_tone: str, text: str) -> str:
        """
        Detecta el tono visual apropiado basado en keywords y tono del artículo.
        """
        # Verificar keywords de temas financieros/negocios (prioridad alta)
        negocio_keywords = self.VISUAL_TONES['SERIO_PROFESIONAL']['keywords']
        negocio_matches = sum(1 for kw in keywords if any(k in kw.lower() for k in negocio_keywords))
        
        if negocio_matches >= 1:
            return 'SERIO_PROFESIONAL'
        
        # Verificar keywords de SALUD_BIENESTAR (temas médicos/serios)
        salud_keywords = self.VISUAL_TONES['SALUD_BIENESTAR']['keywords']
        salud_matches = sum(1 for kw in keywords if any(k in kw.lower() for k in salud_keywords))
        
        if salud_matches >= 1:
            return 'SALUD_BIENESTAR'
        
        # Segundo, prioridad al tono del artículo
        if article_tone in self.ARTICLE_TONE_TO_VISUAL:
            tone_from_article = self.ARTICLE_TONE_TO_VISUAL[article_tone]
            
            tone_config = self.VISUAL_TONES[tone_from_article]
            keywords_match = sum(1 for kw in keywords if any(k in kw.lower() for k in tone_config['keywords']))
            
            if keywords_match >= 1:
                return tone_from_article
        
        # Buscar en keywords del artículo usando prioridad
        for keyword in keywords:
            keyword_lower = keyword.lower()
            for tone_name in self.PROFESIONAL_PRIORITY:
                tone_config = self.VISUAL_TONES[tone_name]
                if any(k in keyword_lower for k in tone_config['keywords']):
                    return tone_name
        
        # Por defecto, usar el tono del artículo
        return self.ARTICLE_TONE_TO_VISUAL.get(article_tone, 'SERIO_PROFESIONAL')
    
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
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
            'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where',
            'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
            'most', 'other', 'some', 'such', 'no', 'not', 'only', 'same',
            'so', 'than', 'too', 'very', 'just', 'about', 'also'
        }
        
        words = re.findall(r'\b[a-záéíóúñü]+\b', text)
        
        word_count = {}
        for word in words:
            if len(word) > 3 and word not in stopwords:
                word_count[word] = word_count.get(word, 0) + 1
        
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, count in sorted_words[:15]]
    
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
                visuals.append(keyword)
        
        return list(set(visuals))[:8]
    
    def _get_tone_style(self, tone_name: str) -> Dict[str, str]:
        """Obtiene la configuración de estilo para un tono visual."""
        return self.VISUAL_TONES.get(tone_name, self.VISUAL_TONES['SERIO_PROFESIONAL'])
    
    def generate_article_prompt(self, article: Dict[str, Any]) -> str:
        """
        Genera un prompt optimizado para imagen de artículo.
        """
        analysis = self.analyze_article(article)
        
        tone_name = analysis['visual_tone']
        tone_style = self._get_tone_style(tone_name)
        
        parts = []
        topic = analysis['topic']
        
        # Tema principal
        parts.append(f"Beautiful {tone_style['description']} illustration about '{topic}'")
        
        # Conceptos visuales
        if analysis['visual_concepts']:
            concepts = ', '.join(analysis['visual_concepts'][:4])
            parts.append(f"Concepts: {concepts}")
        
        # Colores y estilo del tono visual
        parts.append(f"Color palette: {tone_style['colors']}")
        parts.append(f"Style: {tone_style['style']}")
        
        # Título si está disponible
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
        
        tone_name = analysis['visual_tone']
        tone_style = self._get_tone_style(tone_name)
        
        parts = []
        topic = analysis['topic']
        
        # Tamaño según plataforma
        sizes = {
            'instagram': 'square format, 1:1',
            'twitter': 'landscape format, 16:9',
            'facebook': 'landscape format, 16:9',
            'linkedin': 'landscape format, 16:9'
        }
        
        parts.append(f"Beautiful {tone_style['description']} social media post about '{topic}'")
        parts.append(f"Format: {sizes.get(platform, 'square')}")
        
        # Conceptos visuales
        if analysis['visual_concepts']:
            concepts = ', '.join(analysis['visual_concepts'][:3])
            parts.append(f"Elements: {concepts}")
        
        # Estilo visual basado en el tono
        parts.append(f"Color palette: {tone_style['colors']}")
        parts.append(f"Style: {tone_style['style']}")
        
        parts.append("No text, no people")
        
        return ', '.join(parts)


def main():
    """Test del PromptAgent"""
    agent = PromptAgent()
    
    # Test con diferentes tonos
    test_cases = [
        {
            'topic': 'seguros de vida en México',
            'title': 'La Importancia de los Seguros de Vida',
            'tone': 'profesional',
            'introduction': 'Los seguros de vida son fundamentales para proteger a tu familia y asegurar su futuro financiero.',
            'conclusion': 'En conclusion, tener un seguro de vida es una decision inteligente para proteger a tus seres queridos.'
        },
        {
            'topic': 'fiestas de cumpleaños',
            'title': 'Cómo organizar una fiesta increíble',
            'tone': 'casual',
            'introduction': 'Las fiestas de cumpleaños son momentos únicos para celebrar.',
            'conclusion': '¡Celebra siempre con alegría!'
        },
        {
            'topic': 'inteligencia artificial',
            'title': 'El futuro de la IA',
            'tone': 'técnico',
            'introduction': 'La inteligencia artificial está transformando el mundo.',
            'conclusion': 'El futuro está aquí.'
        },
        {
            'topic': 'la importancia de la detección del autismo en la edad temprana con el apoyo de la neuropsicología',
            'title': 'Detección Temprana del Autismo: El Rol de la Neuropsicología',
            'tone': 'profesional',
            'introduction': 'La detección temprana del autismo es fundamental para mejorar los resultados del tratamiento. La neuropsicología juega un papel crucial en identificar señales tempranas en niños.',
            'conclusion': 'La intervención temprana puede hacer una diferencia significativa en el desarrollo del niño.'
        }
    ]
    
    for test in test_cases:
        print(f"\n=== Test: {test['topic']} (tone: {test['tone']}) ===")
        analysis = agent.analyze_article(test)
        print(f"Tono visual: {analysis['visual_tone']}")
        print(f"Keywords: {analysis['keywords'][:5]}")
        
        print("\n--- Social Prompt ---")
        print(agent.generate_social_prompt(test, 'instagram'))


if __name__ == "__main__":
    main()
