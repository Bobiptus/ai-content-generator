import os
import sys
import time
import json
import urllib.request
import ssl
from typing import Optional, Dict, Any
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


class ImageAgent:
    """
    Agente para generar imágenes usando Cloudflare Workers AI
    Gratis: 10,000 neuronas/día (~10-20 imágenes)
    """
    
    def __init__(self, output_dir: str = "outputs/images", max_retries: int = 3):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE
        self.max_retries = max_retries
        
        self.account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
        self.api_token = os.getenv('CLOUDFLARE_API_TOKEN')
        
        if not self.account_id or not self.api_token:
            print("[WARN] Cloudflare credentials not found. Images disabled.")
            self.account_id = None
            self.api_token = None
        
        # Cargar PromptAgent y QA
        try:
            from agents.prompt_agent import PromptAgent
            from agents.qa_agent import ContentSecurityAgent
            self.prompt_agent = PromptAgent()
            self.qa_agent = ContentSecurityAgent()
        except ImportError:
            self.prompt_agent = None
            self.qa_agent = None
    
    def generate(self, prompt: str, width: int = 1024, height: int = 1024) -> Dict[str, Any]:
        """
        Genera una imagen usando Cloudflare Workers AI (Stable Diffusion XL)
        """
        if not self.account_id or not self.api_token:
            return {'success': False, 'error': 'Cloudflare credentials not configured', 'prompt': prompt}
        
        if len(prompt) > 500:
            prompt = prompt[:500]
        
        for attempt in range(self.max_retries):
            try:
                url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0"
                
                safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_prompt = safe_prompt.replace(' ', '_')
                filename = f"image_{safe_prompt}_{int(time.time())}.png"
                filepath = self.output_dir / filename
                
                print(f"  [Image] Generando: {prompt[:50]}...")
                
                data = json.dumps({"prompt": prompt}).encode('utf-8')
                req = urllib.request.Request(
                    url,
                    data=data,
                    headers={
                        'Authorization': f'Bearer {self.api_token}',
                        'Content-Type': 'application/json'
                    },
                    method='POST'
                )
                
                with urllib.request.urlopen(req, timeout=120, context=self.ctx) as response:
                    image_data = response.read()
                
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                
                return {
                    'success': True,
                    'filepath': str(filepath),
                    'url': url,
                    'prompt': prompt,
                    'size': f"{width}x{height}"
                }
                    
            except Exception as e:
                error_msg = str(e)
                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 5
                    print(f"  [Image] Error, esperando {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                return {
                    'success': False,
                    'error': error_msg,
                    'prompt': prompt
                }
        
        return {'success': False, 'error': 'Max retries exceeded', 'prompt': prompt}
    
    def generate_for_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera imagen para un artículo basándose en su contenido.
        Usa PromptAgent para crear prompt y QA para verificarlo.
        """
        # Generar prompt con PromptAgent
        if self.prompt_agent:
            prompt = self.prompt_agent.generate_article_prompt(article)
            print(f"  [QA] Prompt generado por PromptAgent")
        else:
            topic = article.get('topic', '')
            title = article.get('title', '')
            prompt = f"A beautiful and professional blog article cover about '{topic}'. Title: '{title}'. Modern style, clean design, high quality, no text, no people"
        
        # Revisar prompt con QA
        if self.qa_agent:
            from agents.qa_agent import QAReport
            qa_report = QAReport()
            
            # Revisar el prompt
            if hasattr(self.qa_agent, 'review_image_prompt'):
                qa_report = self.qa_agent.review_image_prompt(prompt, article.get('topic', ''))
                
                if qa_report.findings:
                    print(f"  [QA] Hallazgos: {len(qa_report.findings)}")
                    for f in qa_report.findings:
                        print(f"     - {f['severity'].upper()}: {f['message']}")
                    
                    # Optimizar prompt basándose en hallazgos
                    if hasattr(self.qa_agent, 'optimize_prompt'):
                        prompt = self.qa_agent.optimize_prompt(prompt, qa_report)
                        print(f"  [QA] Prompt optimizado")
                else:
                    print(f"  [QA] Prompt aprobado")
        
        return self.generate(prompt=prompt, width=1024, height=1024)
    
    def generate_social_post(self, article: Dict[str, Any], platform: str = "instagram") -> Dict[str, Any]:
        """
        Genera imagen para post de redes sociales.
        Usa PromptAgent para crear prompt y QA para verificarlo.
        """
        sizes = {
            'instagram': (1080, 1080),
            'twitter': (1200, 675),
            'facebook': (1200, 630),
            'linkedin': (1200, 627)
        }
        
        width, height = sizes.get(platform, (1080, 1080))
        
        # Generar prompt
        if self.prompt_agent:
            prompt = self.prompt_agent.generate_social_prompt(article, platform)
        else:
            topic = article.get('topic', '')
            prompt = f"Social media post image about '{topic}'. Platform: {platform}. Eye-catching, modern design, vibrant colors, professional look, no text"
        
        # Revisar con QA
        if self.qa_agent:
            from agents.qa_agent import QAReport
            qa_report = QAReport()
            topic = article.get('topic', '')
            
            if hasattr(self.qa_agent, 'review_image_prompt'):
                qa_report = self.qa_agent.review_image_prompt(prompt, topic)
                
                if qa_report.findings:
                    for f in qa_report.findings:
                        print(f"     - {f['severity'].upper()}: {f['message']}")
                    
                    if hasattr(self.qa_agent, 'optimize_prompt'):
                        prompt = self.qa_agent.optimize_prompt(prompt, qa_report, topic)
                        print(f"     [QA] Prompt corregido")
        
        return self.generate(prompt=prompt, width=width, height=height)


def main():
    from agents.prompt_agent import PromptAgent
    
    agent = ImageAgent()
    print("Testing ImageAgent con PromptAgent...")
    
    test_article = {
        'topic': 'seguros de vida en México',
        'title': 'La Importancia de los Seguros de Vida para las Familias Mexicanas',
        'introduction': 'Los seguros de vida son fundamentales para proteger a tu familia...',
        'conclusion': 'En conclusión, tener un seguro de vida es una decisión inteligente...'
    }
    
    result = agent.generate_for_article(test_article)
    
    if result['success']:
        print(f"SUCCESS: {result['filepath']}")
        print(f"Prompt usado: {result['prompt']}")
    else:
        print(f"FAILED: {result.get('error')}")


if __name__ == "__main__":
    main()
