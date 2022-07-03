import unittest

from app.models.models import Employee
from library.jwt_encoder import JWTEncoder

from main import app
from library.decorators import authtoken


class TestDecorators(unittest.TestCase):
    app.app_context().push()

    def test_for_decorator_negative(self):
        with app.test_request_context('http://www.example.com/', headers={"authToken": "text"}):
            self.test_auth_token()

    def test_for_decorator(self):
        with app.test_request_context('http://www.example.com/',
                                      headers={"authToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
                                                            ".eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InN1cGVydXNlciIsInJvbG"
                                                            "UiOiJhZG1pbiJ9.odKTuXjdpKBEr8K8aBF2VxImqeOUxot7QAo33eKA"
                                                            "8xo"}):
            self.test_auth_token()

    @authtoken
    def test_auth_token(self):
        print('done test')

    def test_encode_jwt(self):
        user_ent = Employee.get_all()
        response = JWTEncoder.encode_jwt(user_ent[0])
        self.assertIsNotNone(response)
