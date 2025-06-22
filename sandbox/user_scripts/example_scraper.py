#!/usr/bin/env python3
"""
Script de ejemplo para el sandbox con Playwright.
"""

from playwright.sync_api import sync_playwright
import json
import time

def scrape_example():
    """Ejemplo básico de scraping con Playwright."""
    print("🎭 Iniciando ejemplo con Playwright...")
    
    with sync_playwright() as p:
        # Lanzar navegador
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navegar a una página de ejemplo
        print("📄 Navegando a example.com...")
        page.goto("https://example.com")
        
        # Extraer información
        title = page.title()
        heading = page.query_selector("h1").inner_text()
        
        print(f"📑 Título: {title}")
        print(f"📋 Encabezado: {heading}")
        
        # Guardar resultados
        results = {
            "url": "https://example.com",
            "title": title,
            "heading": heading,
            "timestamp": time.time()
        }
        
        with open("/app/persistent/example_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print("💾 Resultados guardados en example_results.json")
        
        browser.close()

if __name__ == "__main__":
    scrape_example()
