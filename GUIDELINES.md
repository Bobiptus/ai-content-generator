# AI Content Automation - Project Guidelines

## Descripción del Proyecto

Sistema de automatización de contenido con IA que genera:
- Artículos completos con investigación web
- Posts para redes sociales (Twitter, LinkedIn, Instagram, Facebook)
- Imágenes para artículos y redes sociales
- Control de calidad automatizado

## Arquitectura de Agentes

```
┌─────────────────────────────────────────────────────────────┐
│                     ORQUESTADOR PRINCIPAL                    │
│                    (generate_article.py)                      │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ResearchAgent  │   │Orchestrator   │   │ SocialMedia   │
│ (Búsqueda web)│   │ (Artículos)  │   │ Agent         │
└───────────────┘   └───────────────┘   └───────────────┘
                              │                     │
                              ▼                     ▼
                    ┌───────────────┐   ┌───────────────┐
                    │ QA Agent      │   │ ImageAgent    │
                    │ (Calidad)    │   │ (Imágenes)    │
                    └───────────────┘   └───────────────┘
                                             │
                                             ▼
                                    ┌───────────────┐
                                    │ PromptAgent   │
                                    │ (Prompts)     │
                                    └───────────────┘
```

## Agentes Disponibles

### 1. ResearchAgent (`src/agents/research_agent.py`)
**Propósito:** Búsqueda web automática
- Busca información actualizada con Tavily API
- Cache de 24 horas
- Extrae fuentes relevantes
- **Costo:** Tavily (1000 búsquedas/mes gratis)

### 2. OrchestratorAgent (`src/agents/orchestrator.py`)
**Propósito:** Generación de artículos
- Coordina la generación de contenido
- Genera outline, introducción, secciones, conclusión
- Usa Groq API (Llama 3.3 70B)
- **Costo:** Groq (gratuito con límites)

### 3. ContentQAAgent (`src/agents/qa_agent.py`)
**Propósito:** Control de calidad
- Analiza longitud del contenido
- Detecta texto placeholder
- Verifica coherencia
- Detecta contenido sensible
- **Costo:** Ninguno (procesamiento local)

### 4. ContentSecurityAgent (`src/agents/qa_agent.py`)
**Propósito:** Seguridad del contenido
- Detecta temas sensibles
- Escanea datos personales
- Alertas de contenido restringido
- **Costo:** Ninguno (procesamiento local)

### 5. SocialMediaAgent (`src/agents/social_media_agent.py`)
**Propósito:** Generación de posts sociales
- Genera contenido para Twitter, LinkedIn, Instagram, Facebook
- Adapta el tono a cada plataforma
- Incluye hashtags y call-to-action
- **Costo:** Groq API (incluido en Orchestrator)

### 6. ImageAgent (`src/agents/image_agent.py`)
**Propósito:** Generación de imágenes
- Usa Cloudflare Workers AI (Stable Diffusion XL)
- Genera imágenes para artículos
- Genera imágenes para redes sociales
- **Costo:** Cloudflare (10,000 neuronas/día = ~10-20 imágenes)

### 7. PromptAgent (`src/agents/prompt_agent.py`)
**Propósito:** Optimización de prompts
- Analiza el contenido del artículo
- Genera prompts específicos para imágenes
- Extrae palabras clave y conceptos visuales
- **Costo:** Ninguno (procesamiento local)

## Flujo de Ejecución

```
1. Usuario ejecuta generate_article.py
        │
        ▼
2. ResearchAgent (opcional)
   - Busca en Tavily si --research
   - Guarda en cache 24h
        │
        ▼
3. OrchestratorAgent
   - Genera outline
   - Genera introducción
   - Genera conclusión
        │
        ▼
4. QA Agent
   - Verifica calidad
   - Detecta problemas
        │
        ▼
5. SocialMediaAgent
   - Genera posts para 4 plataformas
        │
        ▼
6. PromptAgent + ImageAgent
   - Analiza artículo para prompts
   - QA de prompts
   - Genera imágenes (artículo + 4 redes sociales)
        │
        ▼
7. Guarda archivos en outputs/
```

## Archivos del Proyecto

```
ai-content-generator/
├── generate_article.py       # Script principal
├── main.py                    # Script alternativo (outline básico)
├── requirements.txt           # Dependencias
├── .env.example               # Plantilla de configuración
├── .gitignore                 # Archivos ignorados
├── src/
│   ├── agents/
│   │   ├── orchestrator.py       # Orquestador de artículos
│   │   ├── research_agent.py     # Búsqueda web
│   │   ├── qa_agent.py          # QA y seguridad
│   │   ├── social_media_agent.py # Posts sociales
│   │   ├── image_agent.py        # Generación de imágenes
│   │   └── prompt_agent.py       # Optimización de prompts
│   └── services/
│       └── cache_service.py      # Cache de búsquedas
└── outputs/                     # Archivos generados
```

## APIs Requeridas

| API | Proveedor | Costo | Uso |
|-----|-----------|-------|-----|
| GROQ_API_KEY | Groq | Gratis (límites) | LLM principal |
| TAVILY_API_KEY | Tavily | 1000/mes gratis | Búsqueda web |
| CLOUDFLARE_ACCOUNT_ID | Cloudflare | Gratis | Imágenes |
| CLOUDFLARE_API_TOKEN | Cloudflare | Gratis | Imágenes |

## Próximos Pasos (Pendientes)

| # | Funcionalidad | Prioridad | Notas |
|---|---------------|-----------|-------|
| 1 | Imágenes con texto | ALTA | Para publicidad en redes sociales |
| 2 | Interfaz gráfica | MEDIA | Python GUI / Web / Móvil |
| 3 | VideoAgent | BAJA | Generación de videos cortos |
| 4 | GitHub Actions avanzado | MEDIA | Automatización CI/CD |

## Cómo Trabajar con Este Proyecto

### Setup Inicial
```bash
git clone <repo>
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Editar .env con API keys
```

### Ejecutar
```bash
python generate_article.py
# O con argumentos:
python generate_article.py --topic "tu tema" --tone profesional --research
```

### Agregar Nuevo Agente
1. Crear archivo en `src/agents/`
2. Implementar clase con método principal
3. Importar en `generate_article.py`
4. Agregar al flujo de ejecución

## Notas Importantes

- El `.env` NO se sube a git (contiene API keys)
- El `venv` NO se sube a git
- Los `outputs/` NO se suben a git
- Cada usuario debe crear su propio `.env`

## Contacto / Soporte

Para continuar con otro agente o sesión:
1. Leer GUIDELINES.md para contexto
2. Leer README.md para setup
3. Revisar código en `src/agents/`
4. Continuar desde el último commit en git
