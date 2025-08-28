# Imagem base oficial do Python
FROM python:3.11-slim

# Criar diretório para app
WORKDIR /app

# Copiar arquivos de requisitos
COPY requirements-prod.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copiar restante do projeto
COPY . .

# Expõe a porta para o servidor
EXPOSE 8080

# Comando de inicialização
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
