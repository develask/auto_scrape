# Auto Scrape

Auto Scrape es un proyecto en Python diseñado para automatizar la extracción de datos de sitios web. Proporciona una interfaz sencilla para definir URLs, selectores de contenido y exportar los resultados en formatos JSON o CSV.

## Características

- Configuración basada en archivos de configuración o código Python.
- Soporte para paginación y manejo de errores.
- Exportación de datos a JSON o CSV.

## Ejemplo de uso
```python
from auto_scrape import Scraper

# Crear un scraper para extraer títulos de artículos
config = {
    'start_urls': ['https://example.com/blog'],
    'selectors': {
        'title': 'h2.post-title',
        'date': 'span.post-date'
    }
}
scraper = Scraper(config)
results = scraper.run()

# Guardar resultados en un archivo JSON
scraper.save(results, 'output.json')
print(f"Se han extraído {len(results)} artículos y guardado en output.json")
```
