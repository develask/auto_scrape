# Sandbox Docker con Playwright

Este sandbox proporciona un entorno Docker aislado con Playwright y otras herramientas de scraping preinstaladas. Permite ejecutar código de scraping de forma segura y reproducible.

## Características

- 🎭 **Playwright** preinstalado con navegadores Chromium, Firefox y WebKit
- 🐍 **Python 3.11** con bibliotecas populares de scraping
- 💾 **Persistencia de datos** entre sesiones
- 🔧 **Tres modos de operación**: interactivo, scripts y Jupyter
- 🛡️ **Entorno aislado** con Docker
- 📚 **Bibliotecas incluidas**: requests, BeautifulSoup, Selenium, pandas, etc.

## Instalación

1. Asegúrate de tener Docker instalado
2. Navega al directorio del sandbox:
   ```bash
   cd sandbox/
   ```

## Modos de uso

### 1. Modo Interactivo (IPython)

Inicia un intérprete Python interactivo con todas las bibliotecas disponibles:

```bash
python sandbox.py interactive
```

Ejemplo de uso dentro del intérprete:
```python
from playwright.sync_api import sync_playwright

# Crear un scraper básico
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    print(page.title())
    browser.close()
```

### 2. Ejecutar Scripts

Coloca tus scripts Python en el directorio `user_scripts/` y ejecútalos:

```bash
python sandbox.py script mi_scraper.py
```

### 3. Jupyter Notebook

Inicia un servidor Jupyter para desarrollo interactivo:

```bash
python sandbox.py jupyter
```

Luego visita `http://localhost:8888` en tu navegador.

## Comandos disponibles

- `python sandbox.py interactive` - Modo interactivo con IPython
- `python sandbox.py script <nombre>` - Ejecutar script específico
- `python sandbox.py jupyter [--port 8888]` - Jupyter Notebook
- `python sandbox.py example` - Crear script de ejemplo
- `python sandbox.py status` - Ver estado del sandbox
- `python sandbox.py build` - Construir imagen Docker
- `python sandbox.py stop` - Detener contenedor

## Estructura de archivos

```
sandbox/
├── Dockerfile              # Configuración Docker
├── requirements.txt         # Dependencias Python
├── entrypoint.sh           # Script de entrada
├── sandbox.py              # Gestor del sandbox
├── user_scripts/           # Tus scripts Python
└── persistent_data/        # Datos que persisten entre sesiones
```

## Bibliotecas incluidas

- **Playwright** - Automatización de navegadores modernos
- **Requests** - Cliente HTTP simple
- **BeautifulSoup4** - Parser HTML/XML
- **Selenium** - Automatización de navegadores tradicional
- **Pandas** - Análisis de datos
- **NumPy** - Computación científica
- **aiohttp** - Cliente HTTP asíncrono
- **fake-useragent** - User agents aleatorios
- **Jupyter** - Notebooks interactivos

## Ejemplos

### Script de ejemplo básico

```python
from playwright.sync_api import sync_playwright
import json

def scrape_quotes():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        page.goto("http://quotes.toscrape.com")
        
        quotes = []
        for quote in page.query_selector_all(".quote"):
            text = quote.query_selector(".text").inner_text()
            author = quote.query_selector(".author").inner_text()
            quotes.append({"text": text, "author": author})
        
        # Guardar en el directorio persistente
        with open("/app/persistent/quotes.json", "w") as f:
            json.dump(quotes, f, indent=2)
        
        browser.close()
        return quotes

if __name__ == "__main__":
    quotes = scrape_quotes()
    print(f"Extraídas {len(quotes)} citas")
```

### Scraping con manejo de errores

```python
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError
import time

def robust_scraper(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        try:
            page = browser.new_page()
            
            # Configurar timeouts y user agent
            page.set_default_timeout(30000)
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            # Navegar con retry
            for attempt in range(3):
                try:
                    page.goto(url, wait_until="networkidle")
                    break
                except TimeoutError:
                    if attempt == 2:
                        raise
                    time.sleep(2)
            
            # Extraer datos
            data = extract_data(page)
            
            return data
            
        finally:
            browser.close()
```

## Persistencia de datos

Los archivos guardados en `/app/persistent/` dentro del contenedor se conservan en el directorio `persistent_data/` de tu máquina local. Esto significa que:

- Los datos persisten entre ejecuciones del sandbox
- Puedes acceder a los resultados desde fuera del contenedor
- Los scripts pueden leer datos de ejecuciones anteriores

## Consejos de uso

1. **Respeta robots.txt**: Siempre verifica los términos de uso de los sitios web
2. **Usa delays**: Implementa pausas entre requests para no sobrecargar servidores
3. **Maneja errores**: Los sitios web pueden cambiar, implementa manejo robusto de errores
4. **User agents**: Usa user agents realistas para evitar detección
5. **Headless mode**: Usa modo headless para mejor rendimiento en producción

## Troubleshooting

### La imagen Docker no se construye

```bash
# Reconstruir imagen forzando
docker build --no-cache -t auto_scrape_sandbox:latest .
```

### Problemas de permisos

```bash
# El contenedor corre como usuario no-root por seguridad
# Si tienes problemas de permisos, verifica que los directorios sean accesibles
chmod -R 755 persistent_data/ user_scripts/
```

### Playwright no encuentra navegadores

La imagen incluye navegadores preinstalados. Si hay problemas:

```bash
# Dentro del contenedor
playwright install --with-deps
```
