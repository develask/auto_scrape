#!/usr/bin/env python3
"""
Script de utilidades para el sandbox Playwright.
Proporciona funciones comunes y plantillas para scraping.
"""

import os
import json
from pathlib import Path
from datetime import datetime


class SandboxUtils:
    """Utilidades para trabajar con el sandbox."""
    
    @staticmethod
    def create_basic_scraper_template(script_name: str, url: str = "https://example.com"):
        """Crear plantilla básica de scraper."""
        template = f'''#!/usr/bin/env python3
"""
Script de scraping generado automáticamente.
Creado: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

from playwright.sync_api import sync_playwright
import json
import time
from datetime import datetime


def scrape_data():
    """Función principal de scraping."""
    print("🎭 Iniciando scraper con Playwright...")
    
    results = []
    
    with sync_playwright() as p:
        # Configurar navegador
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Configurar user agent y timeouts
        page.set_extra_http_headers({{
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }})
        
        try:
            print(f"📄 Navegando a: {url}")
            page.goto("{url}", wait_until="networkidle")
            
            # Esperar a que la página cargue
            page.wait_for_timeout(2000)
            
            # Extraer título
            title = page.title()
            print(f"📑 Título de página: {{title}}")
            
            # TODO: Agregar tu lógica de extracción aquí
            # Ejemplo:
            # elements = page.query_selector_all(".item")
            # for element in elements:
            #     data = {{
            #         "text": element.inner_text(),
            #         "link": element.query_selector("a").get_attribute("href") if element.query_selector("a") else None
            #     }}
            #     results.append(data)
            
            # Datos de ejemplo
            results.append({{
                "title": title,
                "url": "{url}",
                "timestamp": datetime.now().isoformat(),
                "data_extracted": "Modifica este script para extraer datos reales"
            }})
            
        except Exception as e:
            print(f"❌ Error durante el scraping: {{e}}")
            
        finally:
            browser.close()
    
    return results


def save_results(data, filename=None):
    """Guardar resultados en archivo JSON."""
    if filename is None:
        filename = f"scraping_results_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.json"
    
    filepath = f"/app/persistent/{{filename}}"
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados guardados en: {{filename}}")
    print(f"📊 Total de elementos: {{len(data)}}")


def main():
    """Función principal."""
    print("🚀 Ejecutando scraper...")
    
    # Ejecutar scraping
    data = scrape_data()
    
    # Guardar resultados
    if data:
        save_results(data)
        print("✅ Scraping completado exitosamente")
    else:
        print("⚠️  No se encontraron datos")


if __name__ == "__main__":
    main()
'''
        
        script_path = Path("user_scripts") / script_name
        with open(script_path, "w") as f:
            f.write(template)
        
        print(f"📝 Plantilla de scraper creada: {script_path}")
        return script_path
    
    @staticmethod
    def create_async_scraper_template(script_name: str):
        """Crear plantilla de scraper asíncrono."""
        template = f'''#!/usr/bin/env python3
"""
Script de scraping asíncrono con Playwright.
Creado: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

import asyncio
from playwright.async_api import async_playwright
import json
import time
from datetime import datetime


async def scrape_page(page, url):
    """Scraping de una página individual."""
    try:
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        # Extraer datos (personalizar según necesidades)
        title = await page.title()
        
        return {{
            "url": url,
            "title": title,
            "timestamp": datetime.now().isoformat()
        }}
        
    except Exception as e:
        print(f"❌ Error en {{url}}: {{e}}")
        return None


async def scrape_multiple_urls(urls):
    """Scraping de múltiples URLs en paralelo."""
    print(f"🎭 Iniciando scraping asíncrono de {{len(urls)}} URLs...")
    
    results = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Crear múltiples páginas para paralelización
        tasks = []
        for url in urls:
            page = await browser.new_page()
            await page.set_extra_http_headers({{
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }})
            
            task = scrape_page(page, url)
            tasks.append(task)
        
        # Ejecutar todas las tareas en paralelo
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filtrar resultados válidos
        valid_results = [r for r in results if r is not None and not isinstance(r, Exception)]
        
        await browser.close()
    
    return valid_results


async def main():
    """Función principal asíncrona."""
    # URLs de ejemplo (modificar según necesidades)
    urls = [
        "https://example.com",
        "https://httpbin.org/html",
        # Agregar más URLs aquí
    ]
    
    start_time = time.time()
    
    # Ejecutar scraping
    results = await scrape_multiple_urls(urls)
    
    end_time = time.time()
    
    # Guardar resultados
    filename = f"async_scraping_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.json"
    filepath = f"/app/persistent/{{filename}}"
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Scraping completado en {{end_time - start_time:.2f}} segundos")
    print(f"💾 Resultados guardados en: {{filename}}")
    print(f"📊 Total de resultados: {{len(results)}}")


if __name__ == "__main__":
    asyncio.run(main())
'''
        
        script_path = Path("user_scripts") / script_name
        with open(script_path, "w") as f:
            f.write(template)
        
        print(f"📝 Plantilla de scraper asíncrono creada: {script_path}")
        return script_path


def main():
    """CLI para utilidades del sandbox."""
    import sys
    
    if len(sys.argv) < 2:
        print("""
🛠️  Utilidades del Sandbox Playwright

Uso: python utils.py <comando> [argumentos]

Comandos disponibles:
  template <nombre_script> [url]  - Crear plantilla básica de scraper
  async <nombre_script>           - Crear plantilla de scraper asíncrono
  
Ejemplos:
  python utils.py template mi_scraper.py https://quotes.toscrape.com
  python utils.py async scraper_paralelo.py
        """)
        return
    
    command = sys.argv[1]
    utils = SandboxUtils()
    
    if command == "template":
        if len(sys.argv) < 3:
            print("❌ Debes especificar el nombre del script")
            return
        
        script_name = sys.argv[2]
        url = sys.argv[3] if len(sys.argv) > 3 else "https://example.com"
        
        utils.create_basic_scraper_template(script_name, url)
        
    elif command == "async":
        if len(sys.argv) < 3:
            print("❌ Debes especificar el nombre del script")
            return
        
        script_name = sys.argv[2]
        utils.create_async_scraper_template(script_name)
        
    else:
        print(f"❌ Comando no reconocido: {command}")


if __name__ == "__main__":
    main()
