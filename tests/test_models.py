import unittest

# from base import Base
from app.models.models import Employee, Address
from sqlalchemy import exc as sql_exc
import pytest
from main import app


class TestModel(unittest.TestCase):
    app.app_context().push()

    def test_by_name(self):
        response = Employee.by_name('superuser')
        self.assertEqual(len(response), 1)

    def test_by_email(self):
        response = Employee.by_email('superuser')
        self.assertEqual(len(response), 1)

    def test_by_employee_key(self):
        resposne = Address.by_employee_key(1)
        self.assertEqual(len(resposne), 0)

    def test_by_id(self):
        response = Employee.by_id(1)
        self.assertIsNotNone(response)

    def test_get_all(self):
        response = Employee.get_all()
        self.assertIsNotNone(response)

    def test_by_key_val_negative(self):
        with self.assertRaises(AttributeError):
            Employee.by_key_val({'aaaa': 'bbbb'})

    def test_save_me(self):
        emp = Employee(first_name='maithreyan', is_active=True)
        response = emp.save_me()
        self.assertIsNone(response)

    def test_by_ids(self):
        response = Employee.by_ids([1, 2, 3])
        self.assertNotEqual(len(response), 0)

    def test_negative_save_me(self):
        with self.assertRaises(sql_exc.StatementError):
            emp = Employee(first_name='maithreyan', is_active='True')
            emp.save_me()

    def test_delete_me_negative(self):
        with self.assertRaises(IndexError):
            emp = Employee.by_name('tt')
            emp[0].delete_me()

    def test_delete_me(self):
        emp = Employee.by_name('maithreyan')
        response = emp[0].delete_me()
        self.assertEqual(0, 0)


if __name__ == "__main__":
    pytest.main()