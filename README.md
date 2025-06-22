# Auto Scrape

Auto Scrape es un proyecto en Python diseñado para automatizar la extracción de datos de sitios web. Proporciona una interfaz sencilla para definir URLs, selectores de contenido y exportar los resultados en formatos JSON o CSV.

## Características

- Configuración basada en archivos de configuración o código Python.
- Soporte para paginación y manejo de errores.
- Exportación de datos a JSON o CSV.
- Generación de scripts de scraping para uso personalizado.

## Ejemplo de uso
```python
from auto_scrape import ScriptGenerator

config = {
    'start_urls': ['https://example.com/'],
    'description': """
Extract the information from each competition.
The output format must follow the following scheme:
[
    {
        'name': 'Cometition name',
        'date': 'race date',
        'results': [
            {'name': 'Name', 'position': Number, 'time': '00:01:30'},
            {'name': 'Name 2', 'position': Number, 'time': '00:01:30'},
        ]
    }
]
"""
}
generator = ScriptGenerator(config)
script_path = generator.generate('scrape_blog.py')
print(f"Script generado en {script_path}")

# Ejecutar el script para extraer datos y guardarlos en JSON
# python scrape_blog.py --output output.json
```
