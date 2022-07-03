import unittest

from main import app


class TestAPI(unittest.TestCase):
    app.app_context().push()

    def setUp(self):
        self.tester = app.test_client(self)

    def test_hello_world(self):
        response = self.tester.get('/v1/hello_world')
        self.assertEqual(response.status_code, 200)

    def test_login_exception(self):
        response = self.tester.post('/v1/employee-mgmt/login')
        self.assertEqual(response.status_code, 500)

    # def test_get_all_exception(self):
    #     response = self.tester.post('/v1/employee-mgmt/get_all_details')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_get_my_details(self):
    #     response = self.tester.post('/v1/employee-mgmt/get_my_detail',
    #                                 headers={"authToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
    #                                                       ".eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InN1cGVydXNlciIsInJvbG"
    #                                                       "UiOiJhZG1pbiJ9.odKTuXjdpKBEr8K8aBF2VxImqeOUxot7QAo33eKA"
    #                                                       "8xo"})
