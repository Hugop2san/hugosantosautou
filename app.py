import os
import requests
from flask import Flask, render_template, request, redirect, url_for
import nltk
from nltk.corpus import stopwords
from PyPDF2 import PdfReader
from words_train import WordsTrain
from models import db, EmailHistorico




import logging
#from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.DEBUG)

# Token da Hugging Face (variável de ambiente)
HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# URLs de API Hugging Face
CLASSIFIER_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased"
GENERATOR_URL = "https://api-inference.huggingface.co/models/facebook/bart-large"

# Inicializa Flask
app = Flask(__name__)

# Certifique-se que a pasta existe
os.makedirs("/var/data", exist_ok=True)
# Banco de dados


db_path = os.getenv("DATABASE_PATH", "/var/data/emails.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# RENDER CHAMADA

SECRET_KEY = os.environ.get("SECRET_KEY", "fallback_key")
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)




# Inicializa NLTK
def ensure_nltk_data():
    try:
        nltk.data.find("tokenizers/punkt")
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("punkt")
        nltk.download("stopwords")

ensure_nltk_data()
stop_words = set(stopwords.words('portuguese'))

# Inicializa dados de treinamento
words_train = WordsTrain()

# Função para requisição à API Hugging Face
def query_huggingface_api(url, payload):
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

# Funções que simulam o pipeline usando API
def classifier(inputs, candidate_labels):
    return query_huggingface_api(CLASSIFIER_URL, {
        "inputs": inputs,
        "parameters": {"candidate_labels": candidate_labels}
    })

def generator(inputs, max_new_tokens=50, num_return_sequences=1):
    return query_huggingface_api(GENERATOR_URL, {
        "inputs": inputs,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "num_return_sequences": num_return_sequences
        }
    })

# Função para pré-processar texto
def preprocess_text(text):
    words = text.lower().split()
    words = [w for w in words if w not in stop_words]
    return ' '.join(words)

# Função para extrair texto de arquivo
def extract_text_from_file(file):
    if file.filename.endswith('.txt'):
        return file.read().decode('utf-8', errors='ignore')
    elif file.filename.endswith('.pdf'):
        pdf_reader = PdfReader(file)
        return ''.join([page.extract_text() or '' for page in pdf_reader.pages])
    return None

# Função para classificar email
def classify_email(text):
    prompt_examples = "".join(
        [f"Email: {example}\nCategoria: {label}\n\n"
         for example, label in words_train.example_texts]
    )
    prompt = prompt_examples + f"Email: {text}\nCategoria:"
    result = generator(prompt)
    predicted = result[0]['generated_text'].strip().split()[0]
    if predicted not in words_train.labels:
        predicted = "Improdutivo"
    return predicted

# Ajuste por palavras-chave importantes
def boost_keywords(text, predicted, important_keywords):
    text_lower = text.lower()
    for word in important_keywords:
        if word in text_lower:
            return "Produtivo"
    return predicted

# Função para gerar resposta automática
def generate_response(category, text, email):
    if category == "Produtivo":
        prompt = f"Email de {email} foi classificado como {category}."
    else:
        prompt = (
            f"Email de {email} foi classificado como {category}. "
            "Gere uma resposta curta, educada e neutra, sem compromissos adicionais."
        )
    result = generator(prompt)
    return result[0]['generated_text']

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        result = None
        if request.method == 'POST':
            email_name = request.form.get('email_name')
            email_text = request.form.get('email_text')
            email_file = request.files.get('email_file')

            if email_text.strip():
                text = email_text
            elif email_file:
                text = extract_text_from_file(email_file)
            else:
                text = ""

            if text:
                preprocessed = preprocess_text(text)
                category = classify_email(preprocessed)
                category = boost_keywords(preprocessed, category, words_train.important_keywords)
                response = generate_response(category, preprocessed, email_name)
                result = {'category': category, 'response': response}

                novo_email = EmailHistorico(
                    email_nome=email_name,
                    email_texto=email_text,
                    arquivo=email_file.filename if email_file else None,
                    tag=category
                )
                db.session.add(novo_email)
                db.session.commit()

        historico = EmailHistorico.query.filter(EmailHistorico.ativo == True).all()
        return render_template('index.html', result=result, historico=historico)
    
    except Exception as e:
        logging.exception("Erro ao processar requisição")
        return f"Erro interno: {e}", 500
        
        
    

# Rotas de manipulação de emails
@app.route('/delete/<int:email_id>')
def delete_email(email_id):
    email = EmailHistorico.query.get(email_id)
    if email:
        email.ativo = False
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/voltar_caixaentrada/<int:email_id>')
def voltar_caixaentrada(email_id):
    email = EmailHistorico.query.get(email_id)
    if email:
        email.ativo = True
        db.session.commit()
    return redirect(url_for('lixeira'))

@app.route('/permanent_delete/<int:email_id>')
def permanent_delete(email_id):
    email = EmailHistorico.query.get(email_id)
    if email:
        db.session.delete(email)
        db.session.commit()
    return redirect(url_for('lixeira'))

@app.route('/lixeira')
def lixeira():
    historico_deleted = EmailHistorico.query.filter(EmailHistorico.ativo == False).all()
    return render_template('lixeira.html', historico=historico_deleted)


port = int(os.environ.get("PORT", 8080))
#app.run(host="0.0.0.0", port=port)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
