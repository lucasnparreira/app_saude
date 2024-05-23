import os
import sys
import pytest
from app import get_db, main

# Adiciona o diretório principal do projeto ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def client():
    app = main.create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Inicializa o banco de dados aqui, se necessário
            get_db().executescript('''
            DROP TABLE IF EXISTS users;
            DROP TABLE IF EXISTS medidas_corporais;
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT
            );
            CREATE TABLE medidas_corporais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                peso REAL,
                altura REAL,
                braco REAL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            ''')
        yield client

def test_exibir_medidas(client):
    # Adiciona dados de teste
    with main.app_context():
        db = get_db()
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("testuser", "testpass"))
        db.execute("INSERT INTO medidas_corporais (user_id, date, peso, altura, braco) VALUES (?, ?, ?, ?, ?)", (1, "2024-01-01", 70.0, 1.75, 30.0))
        db.commit()

    response = client.get('/exibir_medidas')
    assert response.status_code == 200
    assert b"Historico de medidas" in response.data

def test_excluir_medidas(client):
    # Adiciona dados de teste
    with main.app_context():
        db = get_db()
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("testuser", "testpass"))
        db.execute("INSERT INTO medidas_corporais (user_id, date, peso, altura, braco) VALUES (?, ?, ?, ?, ?)", (1, "2024-01-01", 70.0, 1.75, 30.0))
        db.commit()

    response = client.delete('/excluir_medidas/1')
    assert response.status_code == 204
