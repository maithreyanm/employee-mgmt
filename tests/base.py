import unittest
from main import app
import pytest


class Base(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = app
        cls.client = cls.app.test_client
        cls.app_context = cls.app.app_context()
        cls.app_context.push()