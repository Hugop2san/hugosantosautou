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
# Cria pasta persistente para SQLite
RUN mkdir -p /var/data
# Porta que o Fly.io vai expor
EXPOSE 8080

# Comando para rodar o Flask
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]

# RODAR ASIM PARA TESTES LOCAIS
#CMD ["python", "app.py"]



