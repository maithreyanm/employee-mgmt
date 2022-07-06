import unittest

# from base import Base
from app.models.models import Employee
from app.services.employee_svc import UserService, EmployeeService
# from app.models.models import Employee
import pytest
from main import app


class TestUserService(unittest.TestCase):
    app.app_context().push()

    def test_check_user_exists(self):
        response = UserService.check_user_exists('superuser')
        self.assertIsNotNone(response)

    def test_check_user_exists_negative(self):
        response = UserService.check_user_exists('testuser')
        self.assertIsNone(response)

    def test_verify_password(self):
        hashed_pwd = '$2a$12$k.Kuk14J1vgMWk.CxVjGr.cKzZxwlYNiMKT42.CC5KjgX6t9bQRVC'
        password = 'justin@12345'
        response = UserService.verify_password(hashed_password=hashed_pwd, password=password)
        self.assertTrue(response)

    def test_verify_password_negative(self):
        hashed_pwd = '$2a$12$k.Kuk14J1vgMWk.CxVjGr.cKzZxwlYNiMKT42.CC5KjgX6t9bQRVC'
        password = 'test123'
        response = UserService.verify_password(hashed_password=hashed_pwd, password=password)
        self.assertFalse(response)


class TestEmployeeService(unittest.TestCase):
    app.app_context().push()

    def test_get_all_employees(self):
        response = EmployeeService.get_all_employees()
        self.assertIsNotNone(response)

    def test_add_employee(self):
        address_list = [
            {
                'full_address': 'salem',
                'address_type': 'home'
            }
        ]
        response = EmployeeService.add_employee('maithreyan', 'maithreyan', 'mahy', address_list, '2022-02-02',
                                                'admin', 'maithreyan2@gmail.com', 'M', 'single', 'b+ve')
        global employee_id
        employee_id = response.pid
        self.assertIsNotNone(response)

    def test_update_employee(self):
        user_ent = Employee.by_id("627a2ba8008657f1b1865fac")
        response = EmployeeService.update_employee(user_ent, {'gender': 'M'})
        self.assertIsNotNone(response)

    def test_delete_employee(self):
        response = EmployeeService.delete_employee(employee_id)
        self.assertIsNotNone(response)


if __name__ == "__main__":
    pytest.main()
