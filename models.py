from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EmailHistorico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_nome = db.Column(db.String(120), nullable=False)
    email_texto = db.Column(db.Text, nullable=False)
    arquivo = db.Column(db.String(255))  # caminho do arquivo salvo
    tag = db.Column(db.String(50))  # Ex.: 'Importante' ou 'Não Importante'
    ativo = db.Column(db.Boolean, default=True  )  

    def __init__(self, email_nome, email_texto, arquivo, tag, ativo=True):
        self.email_nome = email_nome
        self.email_texto = email_texto
        self.arquivo = arquivo
        self.tag = tag
        self.ativo= ativo
    
    def __repr__(self):
        return f"<EmailHistorico {self.email}>"

