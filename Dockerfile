# Use imagem slim para reduzir tamanho
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Copia apenas requirements primeiro para aproveitar cache
COPY requirements.txt .

# Instala dependências básicas
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copia todo o código
COPY . .

# Porta que o Fly.io vai expor
EXPOSE 8080

# Comando para rodar o Flask
CMD ["python", "app.py","gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
#CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
