# Dockerfile para el sandbox con Playwright
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    procps \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Playwright y navegadores
RUN playwright install --with-deps

# Crear directorio para scripts de usuario
RUN mkdir -p /app/user_scripts
RUN mkdir -p /app/data
RUN mkdir -p /app/persistent

# Establecer variables de entorno para Playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Script de entrada por defecto
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Crear usuario no root para seguridad
RUN useradd -m -u 1000 sandbox && \
    chown -R sandbox:sandbox /app /ms-playwright
USER sandbox

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["interactive"]
