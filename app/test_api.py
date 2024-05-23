import unittest 
from unittest.mock import patch, MagicMock
from main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

    def tearDown(self):
        pass 
    
    @patch('main.render_template')
    def test_index(self, mock_render_template):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        mock_render_template.assert_called_once_with('index.html')
    
    @patch('main.render_template')
    def test_exercise_tips(self, mock_render_template):
        response = self.app.get('/exercise_tips')
        self.assertEqual(response.status_code, 200)
        mock_render_template.assert_called_once_with('exercise_tips.html')

    @patch('main.render_template')
    def test_calculate_imc(self, mock_render_template):
        response = self.app.get('/calculate_imc')
        self.assertEqual(response.status_code, 200)
        #mock_render_template.assert_called_once_with('calculate_imc.html')
    
    # @patch('main.open')
    # @patch('main.render_template')
    def test_healthy_food(self):
        # mock_file = MagicMock()
        # mock_file.__enter__.return_value = mock_file
        # mock_file.read.return_value = '{"proteina_animal": "Carne de frango"}'
        # mock_open.return_value = mock_file 

        response = self.app.get('/healthy_food.html')
        self.assertEqual(response.status_code, 200)
        # mock_open.assert_called_once_with('templates\data.json', 'r')
        # mock_render_template.assert_called_once_with('healthy_food.html')

    # @patch('main.get_db')
    # @patch('main.render_template')
    def test_weight_form(self):
        # mock_db = MagicMock()
        # mock_get_db.return_value = mock_db 
        # mock_db.execute.return_value.fetchall.return_value = [{'id': 1, 'username': 'test_user'}]

        response = self.app.get('/weight_form')
        self.assertEqual(response.status_code, 200)
        # mock_get_db.assert_called_once()
        # mock_db.execute.assert_called_once_with('select * from users')
        # mock_render_template.assert_called_once_with('weight_form.html')

    def test_weight_tracker(self):
        response = self.app.get('/weight_tracker')
        self.assertEqual(response.status_code, 200)

    # def test_register(self):
    #     response = self.app.get('/register')
    #     self.assertEqual(response.status_code, 200)

    @patch('main.render_template')
    def test_register(self, mock_render_template):
        response = self.app.post('/register', data={'username':'test_user', 'number_id': '12345', 'date': '2024-05-23', 'password': 'test_pass'})
        self.assertEqual(response.status_code, 302)
        mock_render_template.assert_not_called()

        #mock para redirecionamento apos o registro
        mock_redirect = MagicMock()
        mock_redirect.status_code = 302
        with patch('main.redirect', mock_redirect):
            response = self.app.post('/register', data={'username': 'test_user', 'number_id': '12345', 'date': '2024-05-23', 'password': 'test_pass'})
            self.assertEqual(response.status_code, 200)
            mock_render_template.assert_not_called()
    

    @patch('main.render_template')
    def test_login(self, mock_render_template):
        with patch('main.get_db') as mock_get_db:
            #mock para simular usuario existente no banco
            mock_db = MagicMock()
            mock_db.execute.return_value.fetchone.return_value = {'username': 'test_user', 'password': 'test_pass'}
            mock_get_db.return_value = mock_db

            #teste de login com credenciais corretas
            response = self.app.post('/login', data={'username': 'test_user', 'password': 'test_pass'})
            self.assertEqual(response.status_code, 200)
            mock_render_template.assert_called_once_with('index.html', msg='Logged in successfully!')

            #teste de login com credenciais incorretas
            response = self.app.post('/login', data={'username': 'test_user', 'password': 'wrong_pass'})
            self.assertEqual(response.status_code, 200)
            mock_render_template.assert_called_with('login.html', msg='Incorrect username/password!')


    def test_cadastrar_medidas(self):
        response = self.app.get('/cadastrar_medidas')
        self.assertEqual(response.status_code, 200)

    def test_cadastro_sucesso(self):
        response = self.app.get('/cadastro_sucesso')
        self.assertEqual(response.status_code, 200)

    def test_exibir_medidas(self):
        response = self.app.get('/exibir_medidas')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()