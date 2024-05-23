import sqlite3
import tempfile
import os
import unittest
from unittest.mock import MagicMock, patch
from main import app, get_db

class TestAPI(unittest.TestCase):
    # Métodos setUp e tearDown para criar o banco de dados teste
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['DATABASE'] = 'test_database.db'
        self.app = app.test_client()
      
        with app.app_context():
            with app.test_request_context():
                # Criar o esquema do banco de dados
                db = get_db()
                with app.open_resource('schema.sql', mode='r') as f:
                    db.cursor().executescript(f.read())
                db.commit()

    def tearDown(self):
        pass
        # os.close(self.db_fd)
        # os.unlink(app.config['DATABASE'])

    def test_login(self):
        # Popule o banco de dados de teste com um usuário de teste
        with app.app_context():
            conn = sqlite3.connect(app.config['DATABASE'])
            conn.execute("INSERT INTO users (username, number_id, date, password) VALUES (?, ?, ?, ?)",
                         ['test_user', 1113, '2024-05-23','test_pass'])
            conn.commit()
            conn.close()

        # Faça o login com credenciais corretas
        response = self.app.post('/login', data={'username': 'test_user', 'password': 'test_pass'})
        self.assertEqual(response.status_code, 200)

        # Faça o login com credenciais incorretas
        response = self.app.post('/login', data={'username': 'test_user', 'password': 'wrong_pass'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Senha incorreta!', response.data)

        # Faça o login com um usuário não cadastrado
        response = self.app.post('/login', data={'username': 'non_existing_user', 'password': 'some_password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Usuario nao cadastrado!', response.data)



if __name__ == '__main__':
    unittest.main()
