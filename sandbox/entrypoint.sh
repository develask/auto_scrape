#!/bin/bash

# Script de entrada para el contenedor sandbox

case "$1" in
    "interactive")
        echo "Iniciando modo interactivo con IPython..."
        echo "Playwright está disponible. Ejemplo de uso:"
        echo "from playwright.sync_api import sync_playwright"
        echo "=================================="
        cd /app/persistent
        exec ipython
        ;;
    "script")
        if [ -z "$2" ]; then
            echo "Error: Debes especificar un script para ejecutar"
            echo "Uso: docker run ... script <nombre_del_script>"
            exit 1
        fi
        echo "Ejecutando script: $2"
        cd /app/persistent
        exec python "/app/user_scripts/$2"
        ;;
    "jupyter")
        echo "Iniciando Jupyter Notebook..."
        cd /app/persistent
        exec jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=''
        ;;
    *)
        echo "Modo no reconocido. Modos disponibles:"
        echo "  interactive - Intérprete IPython interactivo"
        echo "  script <nombre> - Ejecutar un script específico"
        echo "  jupyter - Iniciar Jupyter Notebook"
        exit 1
        ;;
esac
