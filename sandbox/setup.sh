#!/bin/bash

# Script de configuración inicial para el sandbox Docker con Playwright

echo "🚀 Configurando sandbox Docker con Playwright..."

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor, instala Docker primero."
    echo "   Visita: https://docs.docker.com/get-docker/"
    exit 1
fi

# Verificar que Docker esté ejecutándose
if ! docker info &> /dev/null; then
    echo "❌ Docker no está ejecutándose. Por favor, inicia Docker."
    exit 1
fi

echo "✅ Docker está disponible"

# Crear directorios necesarios
mkdir -p persistent_data user_scripts

echo "✅ Directorios creados"

# Hacer ejecutable el script sandbox.py
chmod +x sandbox.py

echo "✅ Permisos configurados"

# Construir la imagen Docker
echo "🔨 Construyendo imagen Docker (esto puede tardar unos minutos)..."
python sandbox.py build

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 ¡Sandbox configurado exitosamente!"
    echo ""
    echo "📋 Comandos disponibles:"
    echo "   python sandbox.py interactive  # Modo interactivo"
    echo "   python sandbox.py jupyter      # Jupyter Notebook"
    echo "   python sandbox.py script <nombre>  # Ejecutar script"
    echo "   python sandbox.py status       # Ver estado"
    echo ""
    echo "📝 Para empezar, prueba:"
    echo "   python sandbox.py example      # Crear script de ejemplo"
    echo "   python sandbox.py script example_scraper.py  # Ejecutar ejemplo"
    echo ""
else
    echo "❌ Error configurando el sandbox. Revisa los mensajes de error anteriores."
    exit 1
fi
