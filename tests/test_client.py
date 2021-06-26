import unittest
from server import create_app
from app.blueprints.user.model import delete_user
from app.blueprints.user.token import generate_confirmation_token, confirm_token
import jwt


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

    def test_unauthorised_converter_call(self):
        response = self.client.get('/btcRate')
        self.assertEqual(response.status_code, 401)

    def test_registration_login_activation_converter(self):
        email = 'john@example.com'
        password = 'cat'
        delete_user(email)
        response = self.client.post('/user/create', headers={
                'email': email,
                'password': password})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/user/login', headers={
                'email': email,
                'password': password})
        jwt_token = response.data
        decoded = jwt.decode(jwt_token, options={"verify_signature": False})
        self.assertEqual(decoded['is_activated'], False)

        response = self.client.get('/btcRate', headers={'Authorization': jwt_token})
        self.assertEqual(response.status_code, 401)

        confirmation_token = generate_confirmation_token(email)
        result = self.client.get(f'/user/confirm/{confirmation_token}')
        self.assertEqual(result.status_code, 200)

        response = self.client.post('/user/login', headers={
            'email': email,
            'password': password})
        jwt_token = response.data
        decoded = jwt.decode(jwt_token, options={"verify_signature": False})
        self.assertEqual(decoded['is_activated'], True)

        response = self.client.get('/btcRate', headers={'Authorization': jwt_token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('amount', response.json)

        delete_user('john@example.com')