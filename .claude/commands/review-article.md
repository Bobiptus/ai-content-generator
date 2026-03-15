# Revisa la calidad de un artículo generado

Este comando analiza un artículo existente y genera un reporte de calidad, similar a una revisión de seguridad.

## Uso

/review-article

## Descripción

El agente de QA analizará:
1. Longitud del contenido
2. Coherencia y estructura
3. Engagement del lector
4. Contenido sensible o inapropiado
5. Originalidad

## Ejemplo de salida

## Reporte de Calidad
Puntuación: 85/100
Estado: ✅ APROBADO

🔴 CRITICAL - Contenido
   Se encontró texto de placeholder
   📝 Recomendación: Reemplaza con contenido original

🟡 MEDIUM - Introducción
   La introducción es muy corta
   📝 Recomendación: Amplía la introducción a al menos 100 palabras
