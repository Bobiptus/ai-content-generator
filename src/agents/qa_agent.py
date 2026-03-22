import os
import sys
from typing import Dict, List, Any
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from dotenv import load_dotenv
load_dotenv()


class QAReport:
    """Reporte de Quality Assurance"""
    
    def __init__(self):
        self.findings: List[Dict[str, str]] = []
        self.score: int = 100
        self.passed: bool = True
    
    def add_finding(self, severity: str, category: str, message: str, recommendation: str = ""):
        severities = {
            'critical': 25,
            'high': 15,
            'medium': 10,
            'low': 5,
            'info': 0
        }
        
        self.findings.append({
            'severity': severity,
            'category': category,
            'message': message,
            'recommendation': recommendation
        })
        
        self.score -= severities.get(severity, 0)
        self.passed = self.score >= 70
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'score': max(0, self.score),
            'passed': self.passed,
            'findings': self.findings,
            'timestamp': datetime.now().isoformat()
        }
    
    def to_markdown(self) -> str:
        lines = [f"## Reporte de Calidad", f"Puntuación: {max(0, self.score)}/100", f"Estado: {'✅ APROBADO' if self.passed else '❌ REPROBADO'}", ""]
        
        if not self.findings:
            lines.append("✅ No se encontraron problemas")
            return "\n".join(lines)
        
        severity_order = ['critical', 'high', 'medium', 'low', 'info']
        sorted_findings = sorted(self.findings, key=lambda x: severity_order.index(x['severity']))
        
        for f in sorted_findings:
            emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🔵', 'info': 'ℹ️'}.get(f['severity'], '•')
            lines.append(f"{emoji} **{f['severity'].upper()}** - {f['category']}")
            lines.append(f"   {f['message']}")
            if f['recommendation']:
                lines.append(f"   📝 Recomendación: {f['recommendation']}")
            lines.append("")
        
        return "\n".join(lines)


class ContentQAAgent:
    """Agente de Quality Assurance para revisar contenido generado"""
    
    def __init__(self):
        self.provider = "groq"
        self.client = None
        self._setup()
    
    def _setup(self):
        try:
            from groq import Groq
            api_key = os.getenv('GROQ_API_KEY')
            if api_key:
                self.client = Groq(api_key=api_key)
        except:
            pass
    
    def analyze_article(self, article: Dict[str, Any]) -> QAReport:
        """Analiza un artículo y genera un reporte de calidad"""
        report = QAReport()
        
        title = article.get('title', '')
        introduction = article.get('introduction', '')
        conclusion = article.get('conclusion', '')
        content = f"{introduction} {conclusion}"
        
        if len(title) < 10:
            report.add_finding(
                'high', 
                'Título', 
                'El título es demasiado corto',
                'Usa un título más descriptivo de al menos 10 caracteres'
            )
        
        if len(title) > 100:
            report.add_finding(
                'medium',
                'Título',
                'El título es demasiado largo',
                'Reduce el título a menos de 100 caracteres'
            )
        
        if len(introduction) < 100:
            report.add_finding(
                'medium',
                'Introducción',
                'La introducción es muy corta',
                'Amplía la introducción a al menos 100 palabras'
            )
        
        if len(conclusion) < 50:
            report.add_finding(
                'low',
                'Conclusión',
                'La conclusión podría ser más sustancial',
                'Amplía la conclusión con un llamado a la acción'
            )
        
        words = content.split()
        if len(words) < 200:
            report.add_finding(
                'high',
                'Extensión',
                'El artículo es muy corto',
                'El artículo debería tener al menos 200 palabras'
            )
        
        forbidden = ['Lorem ipsum', 'texto de ejemplo', 'placeholder']
        for phrase in forbidden:
            if phrase.lower() in content.lower():
                report.add_finding(
                    'critical',
                    'Contenido',
                    f'Se encontró texto de relleno: "{phrase}"',
                    'Reemplaza con contenido original'
                )
        
        if '?' not in introduction and '!' not in introduction:
            report.add_finding(
                'info',
                'Engagement',
                'La introducción podría ser más dinámica',
                'Considera añadir preguntas o exclamaciones'
            )
        
        return report
    
    def deep_analysis(self, article: Dict[str, Any]) -> QAReport:
        """Análisis profundo usando IA - similar al security review de Anthropic"""
        report = self.analyze_article(article)
        
        if not self.client:
            return report
        
        try:
            from groq import Groq
            
            topic = article.get('topic', '')
            title = article.get('title', '')
            intro = article.get('introduction', '')[:500]
            conclusion = article.get('conclusion', '')[:500]
            
            prompt = f"""Analiza este artículo y encuentra problemas de calidad:

Tema: {topic}
Título: {title}
Introducción: {intro}
Conclusión: {conclusion}

Evalúa:
1. Coherencia - ¿El contenido tiene sentido?
2. Relevancia - ¿Está relacionado con el tema?
3. Originalidad - ¿Parece contenido único o genérico?
4. Engagement - ¿Captura la atención?

Responde en JSON:
{{
  "problemas": [
    {{"severity": "high|medium|low", "tipo": "coherencia|relevancia|originalidad|engagement", "descripcion": "...", "recomendacion": "..."}}
  ]
}}"""

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            
            import json
            import re
            
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                for problem in data.get('problemas', []):
                    report.add_finding(
                        problem.get('severity', 'low'),
                        problem.get('tipo', 'calidad').title(),
                        problem.get('descripcion', ''),
                        problem.get('recomendacion', '')
                    )
        
        except Exception as e:
            report.add_finding('info', 'Análisis IA', f'No se pudo completar análisis profundo: {str(e)}', '')
        
        return report


class ContentSecurityAgent:
    """Agente de seguridad para detectar contenido sensible/inapropiado"""
    
    FORBIDDEN_TOPICS = [
        '武器制作', 'bombas', 'drogas', 'violencia',
    ]
    
    SENSITIVE_PATTERNS = [
        (r'\b\d{16}\b', 'Número de tarjeta de crédito'),
        (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'Email'),
        (r'\b\d{3}-\d{2}-\d{4}\b', 'Número de Seguro Social'),
    ]
    
    def __init__(self):
        pass
    
    def scan_article(self, article: Dict[str, Any]) -> QAReport:
        """Escanea el artículo buscando contenido sensible"""
        report = QAReport()
        
        full_content = f"{article.get('title', '')} {article.get('introduction', '')} {article.get('conclusion', '')}"
        
        for topic in self.FORBIDDEN_TOPICS:
            if topic.lower() in full_content.lower():
                report.add_finding(
                    'critical',
                    'Contenido Restringido',
                    f'Se detectó tema potencialmente sensible: {topic}',
                    'Revisa manualmente este contenido'
                )
        
        for pattern, description in self.SENSITIVE_PATTERNS:
            import re
            if re.search(pattern, full_content):
                report.add_finding(
                    'high',
                    'Datos Personales',
                    f'Se detectó {description}',
                    'Asegúrate de que el contenido no exponga datos reales'
                )
        
        return report
    
    def review_image_prompt(self, prompt: str, context: str = "") -> QAReport:
        """
        Revisa un prompt de imagen antes de enviarlo a Cloudflare.
        Sin costo de API - usa reglas predefinidas.
        """
        report = QAReport()
        prompt_lower = prompt.lower()
        
        # Verificar longitud
        if len(prompt) < 20:
            report.add_finding('high', 'Longitud', 'Prompt muy corto', 'Agrega más contexto')
        elif len(prompt) > 400:
            report.add_finding('medium', 'Longitud', 'Prompt muy largo', 'Cloudflare puede truncarlo')
        
        # Verificar que tenga descripción visual
        visual_words = ['image', 'photo', 'picture', 'illustration', 'design', 'cover', 'beautiful', 'modern', 'professional']
        if not any(word in prompt_lower for word in visual_words):
            report.add_finding('medium', 'Contenido', 'Falta descripción visual', 'Agrega palabras como: beautiful, illustration, design')
        
        # Verificar que no tenga texto (la imagen no puede generar texto)
        text_indicators = ['write the', 'write in', 'text in image', 'add text', 'letter in', 'put text', 'include text']
        problematic_phrases = ['write the title', 'write text', 'add the word', 'letter in image', 'text in the image', 'put words']
        
        has_problem = any(ind in prompt_lower for ind in problematic_phrases)
        
        # Excluir "no text" y "without text"
        if 'no text' in prompt_lower or 'without text' in prompt_lower:
            has_problem = False
        
        if has_problem:
            report.add_finding('high', 'Texto', 'El prompt menciona texto', 'Las imágenes no pueden generar texto legible. Elimina referencias a texto en la imagen')
        
        # Verificar que no tenga instrucciones conflictivas
        if 'no ' in prompt_lower and 'but' in prompt_lower:
            report.add_finding('low', 'Estilo', 'Instrucciones conflictivas', 'Simplifica las instrucciones')
        
        # Si hay contexto del artículo, verificar relevancia
        if context:
            context_words = set(context.lower().split())
            prompt_words = set(prompt_lower.split())
            overlap = context_words & prompt_words
            if len(overlap) < 2:
                report.add_finding('medium', 'Relevancia', 'El prompt no parece relacionado con el artículo', 'Asegúrate de que el prompt refleje el tema del artículo')
        
        return report
    
    def optimize_prompt(self, prompt: str, report: QAReport, topic: str = "") -> str:
        """
        Optimiza un prompt basándose en los hallazgos del QA.
        """
        optimized = prompt
        
        # Si el prompt es muy corto, agregar contexto adicional
        if len(prompt) < 50:
            optimized = f"Beautiful professional image. {optimized}. High quality, modern style"
        
        # Si falta descripción visual, agregar palabras clave
        visual_words = ['beautiful', 'professional', 'high quality', 'modern']
        if not any(word in optimized.lower() for word in visual_words):
            optimized = f"{optimized}. Professional design, high quality"
        
        # Asegurar que no tenga referencias a texto
        text_phrases = ['write the', 'write in', 'text in', 'letter in', 'caption in', 'add text']
        for phrase in text_phrases:
            optimized = optimized.replace(phrase, '')
        
        # Si hay hallazgo de relevancia, agregar el tema del artículo
        relevance_issue = any(f['category'] == 'Relevancia' for f in report.findings)
        if relevance_issue and topic:
            # El prompt debe incluir claramente el tema del artículo
            optimized = f"Social media post about '{topic}'. Professional image, high quality, modern design, vibrant colors, no text"
        
        return optimized.strip()
