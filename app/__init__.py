from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurações do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///saude.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialize a extensão SQLAlchemy
db = SQLAlchemy(app)
