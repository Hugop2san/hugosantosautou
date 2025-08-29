# AutoU - Sistema de Automação

Sistema de automação desenvolvido com Flask e tecnologias de IA.

## Pré-requisitos

- Python 3.9 ou superior
- Git
- pip (gerenciador de pacotes Python)

## 🚀 Como executar o projeto

### 1. Clone o repositório
```bash
git clone https://github.com/Hugop2san/HugoSantosAutoU.git
cd HugoSantosAutoU
```

# Crie um ambiente virtual
```bash
# Windows
python -m venv env
env\Scripts\activate

# Linux/Mac
python -m venv env
source env/bin/activate
```

# Instale as dependências
```bash
pip install -r requirements.txt 
```
# Configure as variáveis de ambiente

## Crie um arquivo .env na raiz do projeto:
```bash
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///instance/autou.db
HUGGINGFACE_TOKEN=seu_token_aqui
```

# Inicialize o banco de dados
```bash
python create_db.py
```

# Execute a aplicação
```bash
# Flask development server
python app.py
  
# A aplicação estará disponível em: http://localhost:5000
```

# Executar com Docker

## Build da imagem
```bash
docker build -t autou-app .
```

# Executar container
```bash
docker run -p 5000:5000 -e FLASK_ENV=development autou-app
```

# Estrutura do Projeto
```bash
HugoSantosAutoU/
├── app.py              # Aplicação principal Flask
├── models.py           # Modelos de banco de dados
├── create_db.py        # Script de criação do banco
├── words_train.py      # Treinamento de modelos de IA
├── requirements.txt    # Dependências de desenvolvimento
├── requirements-prod.txt # Dependências de produção
├── Dockerfile         # Configuração Docker
├── .dockerignore      # Arquivos ignorados no Docker
├── .gitignore         # Arquivos ignorados no Git
├── instance/          # Banco de dados SQLite
├── static/           # Arquivos estáticos (CSS, JS, imagens)
└── templates/        # Templates HTML
```