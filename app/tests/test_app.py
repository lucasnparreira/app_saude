import unittest
from unittest.mock import patch
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to My App', response.data)

    def test_invalid_route(self):
        response = self.app.get('/invalid')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Not Found', response.data)

    @patch('app.some_external_dependency')  # Mock external dependency
    def test_custom_route(self, mock_dependency):
        mock_dependency.return_value = 'Custom Response'
        response = self.app.get('/custom')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Custom Response', response.data)

if __name__ == '__main__':
    unittest.main()

