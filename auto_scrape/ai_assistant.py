"""
Asistente de IA para generar código de scraping.
"""

import openai
from typing import Optional


class AIAssistant:
    """Asistente de IA para generar código de scraping."""
    
    def generate_scraping_code(self, prompt: str) -> str:
        """
        Generar código de scraping usando IA.
        
        Args:
            prompt: Descripción de lo que se quiere hacer
            
        Returns:
            Código Python generado
        """
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """Eres un experto en web scraping con Python. 
                        Genera código limpio, eficiente y que siga las mejores prácticas.
                        Incluye siempre manejo de errores y respeta los robots.txt y rate limits."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            # Fallback: generar código básico si falla la IA
            print(f"Error generando código con IA: {e}")
    