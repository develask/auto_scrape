#!/usr/bin/env python3
"""
Sandbox para ejecutar código Python con Playwright en un entorno Docker aislado.

Este sandbox permite dos modos de operación:
1. Ejecutar scripts específicos
2. Modo interactivo con intérprete Python persistente

Características:
- Entorno Docker con Playwright preinstalado
- Persistencia de datos entre sesiones
- Acceso a bibliotecas de scraping populares
- Modo Jupyter Notebook opcional
"""

import os
import sys
import subprocess
import argparse
import json
from pathlib import Path
from typing import Optional, List


class PlaywrightSandbox:
    """Gestor del sandbox Docker con Playwright."""
    
    def __init__(self, container_name: str = "auto_scrape_sandbox"):
        self.container_name = container_name
        self.image_name = "auto_scrape_sandbox:latest"
        self.sandbox_dir = Path(__file__).parent
        self.persistent_dir = self.sandbox_dir / "persistent_data"
        self.scripts_dir = self.sandbox_dir / "user_scripts"
        
        # Crear directorios si no existen
        self.persistent_dir.mkdir(exist_ok=True)
        self.scripts_dir.mkdir(exist_ok=True)
    
    def build_image(self) -> bool:
        """Construir la imagen Docker del sandbox."""
        print("🔨 Construyendo imagen Docker del sandbox...")
        
        try:
            cmd = [
                "docker", "build",
                "-t", self.image_name,
                str(self.sandbox_dir)
            ]
            
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✅ Imagen construida exitosamente")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error construyendo imagen: {e}")
            print(f"Salida: {e.stdout}")
            print(f"Error: {e.stderr}")
            return False
    
    def check_image_exists(self) -> bool:
        """Verificar si la imagen Docker existe."""
        try:
            result = subprocess.run(
                ["docker", "images", "-q", self.image_name],
                capture_output=True, text=True, check=True
            )
            return bool(result.stdout.strip())
        except subprocess.CalledProcessError:
            return False
    
    def is_container_running(self) -> bool:
        """Verificar si el contenedor está ejecutándose."""
        try:
            result = subprocess.run(
                ["docker", "ps", "-q", "-f", f"name={self.container_name}"],
                capture_output=True, text=True, check=True
            )
            return bool(result.stdout.strip())
        except subprocess.CalledProcessError:
            return False
    
    def stop_container(self) -> bool:
        """Detener el contenedor si está ejecutándose."""
        if not self.is_container_running():
            return True
            
        try:
            subprocess.run(
                ["docker", "stop", self.container_name],
                check=True, capture_output=True
            )
            print(f"🛑 Contenedor {self.container_name} detenido")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error deteniendo contenedor: {e}")
            return False
    
    def run_interactive(self) -> bool:
        """Ejecutar el sandbox en modo interactivo."""
        if not self.check_image_exists():
            if not self.build_image():
                return False
        
        print("🚀 Iniciando sandbox en modo interactivo...")
        print("📝 Los archivos se guardarán en:", self.persistent_dir.absolute())
        
        cmd = [
            "docker", "run", "-it", "--rm",
            "--name", self.container_name,
            "-v", f"{self.persistent_dir.absolute()}:/app/persistent",
            "-v", f"{self.scripts_dir.absolute()}:/app/user_scripts",
        ]
        
        cmd.extend([self.image_name, "interactive"])
        
        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error ejecutando contenedor: {e}")
            return False
        except KeyboardInterrupt:
            print("\n👋 Saliendo del sandbox...")
            return True
    
    def run_script(self, script_name: str) -> bool:
        """Ejecutar un script específico en el sandbox."""
        script_path = self.scripts_dir / script_name
        
        if not script_path.exists():
            print(f"❌ Script no encontrado: {script_path}")
            return False
        
        if not self.check_image_exists():
            if not self.build_image():
                return False
        
        print(f"🏃 Ejecutando script: {script_name}")
        
        cmd = [
            "docker", "run", "--rm",
            "--name", f"{self.container_name}_script",
            "-v", f"{self.persistent_dir.absolute()}:/app/persistent",
            "-v", f"{self.scripts_dir.absolute()}:/app/user_scripts",
            self.image_name, "script", script_name
        ]
        
        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error ejecutando script: {e}")
            return False
   
    def create_example_script(self) -> None:
        """Crear un script de ejemplo."""
        example_script = '''#!/usr/bin/env python3
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
'''
        
        example_path = self.scripts_dir / "example_scraper.py"
        with open(example_path, "w") as f:
            f.write(example_script)
        
        print(f"📝 Script de ejemplo creado: {example_path}")
    
    def list_scripts(self) -> List[str]:
        """Listar scripts disponibles."""
        scripts = []
        for file in self.scripts_dir.glob("*.py"):
            scripts.append(file.name)
        return scripts
    
    def status(self) -> None:
        """Mostrar estado del sandbox."""
        print("📊 Estado del Sandbox:")
        print(f"   Imagen Docker: {'✅' if self.check_image_exists() else '❌'} {self.image_name}")
        print(f"   Contenedor: {'🟢' if self.is_container_running() else '⚫'} {self.container_name}")
        print(f"   Directorio persistente: {self.persistent_dir.absolute()}")
        print(f"   Directorio de scripts: {self.scripts_dir.absolute()}")
        
        scripts = self.list_scripts()
        if scripts:
            print(f"   Scripts disponibles ({len(scripts)}):")
            for script in scripts:
                print(f"     • {script}")
        else:
            print("   Scripts disponibles: Ninguno")


def main():
    """Función principal del CLI."""
    parser = argparse.ArgumentParser(
        description="Sandbox Docker con Playwright para scraping",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Modo interactivo (IPython)
  python sandbox.py interactive

  # Ejecutar un script específico
  python sandbox.py script mi_scraper.py

  # Crear script de ejemplo
  python sandbox.py example

  # Ver estado del sandbox
  python sandbox.py status

  # Construir imagen Docker
  python sandbox.py build
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")
    
    # Comando interactive
    interactive_parser = subparsers.add_parser("interactive", help="Modo interactivo con IPython")
    
    # Comando script
    script_parser = subparsers.add_parser("script", help="Ejecutar script específico")
    script_parser.add_argument("script_name", help="Nombre del script a ejecutar")
    
    # Comando example
    example_parser = subparsers.add_parser("example", help="Crear script de ejemplo")
    
    # Comando status
    status_parser = subparsers.add_parser("status", help="Mostrar estado del sandbox")
    
    # Comando build
    build_parser = subparsers.add_parser("build", help="Construir imagen Docker")
    
    # Comando stop
    stop_parser = subparsers.add_parser("stop", help="Detener contenedor")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    sandbox = PlaywrightSandbox()
    
    if args.command == "interactive":
        sandbox.run_interactive()
    elif args.command == "script":
        sandbox.run_script(args.script_name)
    elif args.command == "example":
        sandbox.create_example_script()
    elif args.command == "status":
        sandbox.status()
    elif args.command == "build":
        sandbox.build_image()
    elif args.command == "stop":
        sandbox.stop_container()


if __name__ == "__main__":
    main()