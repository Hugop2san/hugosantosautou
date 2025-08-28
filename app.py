import os
from flask import Flask, render_template, request
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from PyPDF2 import PdfReader
from words_train import WordsTrain
from models import db, EmailHistorico
from flask import Flask, render_template, request, redirect, url_for


# Configurar NLTK
nltk.download('stopwords')
stop_words = set(stopwords.words('portuguese'))

app = Flask(__name__)

# Lista temporária para simular lixeira
lixeira_temp = []

# criacao banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

 
# Função para pré-processar texto (remover stopwords)
def preprocess_text(text):
    text = text.lower()
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)

# Função para extrair texto de arquivo
def extract_text_from_file(file):
    filename = file.filename.lower()
    
    if file.filename.endswith('.txt'):
        return file.read().decode('utf-8', errors='ignore')
    elif file.filename.endswith('.pdf'):
        pdf_reader = PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text() or ''
        return text
    else:
        return None

# Inicializar pipelines Hugging Face
classifier = pipeline("zero-shot-classification", model="distilbert-base-uncased")
generator = pipeline("text2text-generation", model="facebook/bart-large")


words_train = WordsTrain()
 
 
# Função para classificar email
def classify_email(text):
        # Construindo um prompt few-shot
    prompt_examples = ""
    for example, label in words_train.example_texts:
        prompt_examples += f"Email: {example}\nCategoria: {label}\n\n"
    
    prompt = prompt_examples + f"Email: {text}\nCategoria:"

    # Usando o pipeline de classificação como "text2text" para ler prompt
    result = generator(prompt, max_new_tokens=50, num_return_sequences=1)
    
    # Retorna a primeira palavra como categoria prevista
    predicted = result[0]['generated_text'].strip().split()[0]
    
        # Se a previsão não bater com labels, retorna 'Improdutivo' como default
    if predicted not in words_train.labels:
        predicted = "Improdutivo"
    
    return predicted

def boost_keywords(text, predicted, important_keywords):
    """
    Ajusta a previsão se palavras-chave importantes forem detectadas no texto.

    Args:
        text (str): Texto analisado.
        predicted (str): Previsão original do modelo.
        important_keywords (list): Lista de palavras-chave.

    Returns:
        str: Previsão ajustada.
    """
    text_lower = text.lower()
    for word in important_keywords:
        if f"{word}" in f"{text_lower}":
            return "Produtivo"
    return predicted


# Função para gerar resposta automática
def generate_response(category, text, email):
    
    
    if category == "Produtivo":
        prompt = (
            f"Email de {email} foi classificado como {category}.")
    else:
        prompt = (
            f"Email de {email} foi classificado como {category}. "
            f"Gere uma resposta curta, educada e neutra, sem compromissos adicionais." )
        
    
    result = generator(prompt, max_new_tokens=50, num_return_sequences=1)
    return result[0]['generated_text']

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def index():
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
            category = boost_keywords(preprocessed, category, words_train.important_keywords)  # força Produtivo se palavra-chave encontrada
            response = generate_response(category, preprocessed, email_name)
            result = {'category': category, 'response': response}
                # Persistência no banco

            novo_email = EmailHistorico(
            email_nome=email_name, 
            email_texto=email_text, 
            arquivo=email_file.filename if email_file else None, 
            tag=category) # usando a classificação como tag
            
            db.session.add(novo_email)
            db.session.commit()
        
    historico = EmailHistorico.query.filter(EmailHistorico.ativo == True).all()
    
    return render_template('index.html', result=result, historico=historico)



#ENDPOINT PARA TRANSFERENCIA PARA A LIXEIRA, SIMULANDO UMA EXCLUSAO PARCIAL
@app.route('/delete/<int:email_id>')
def delete_email(email_id):
    # Pega email do histórico
    email = EmailHistorico.query.get(email_id)
    if email: 
        email.ativo = False 
        db.session.commit()
  
    return redirect(url_for('index'))

# ENDPOINT QUE TORNA O EMAIL QUE ESTA NA LIXEIRA PARA A CAIXA DE ENTRADA NOVAMENTE COMO TRUE
@app.route('/voltar_caixaentrada/<int:email_id>')
def voltar_caixaentrada(email_id):
    # Pega email do histórico de lixeira e torna-lo true novamente
    email = EmailHistorico.query.get(email_id)
    if email: 
        email.ativo = True 
        db.session.commit()
    return redirect(url_for('lixeira'))

#ENDPOINT PARA EXCLUSAO PERMANENTE DO BANCO
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




if __name__ == '__main__':
    app.run(debug=True)
