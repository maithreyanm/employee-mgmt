from app.models import MongoConfig as sqla
from app.models.models import Employee, Address, Person
from app import AppFactory
from library.datetime_helper import DateTimeHelper
from sqlalchemy import orm


class CustomException(Exception):
    pass


class UserService:

    @classmethod
    def check_user_exists(cls, username):
        employee = Employee.objects(email=username).first()
        if employee is None:
            return None
        else:
            return employee

    @classmethod
    def verify_password(cls, hashed_password, password):
        is_matched = AppFactory.bcrypt.check_password_hash(hashed_password, password)
        return True if is_matched else False


class EmployeeService:

    @classmethod
    def build_payload(cls, user_ent):
        address_list = []
        if user_ent.addresses is not None:
            for address in user_ent.addresses:
                addr_dict = {
                    'address_type': address['address_type'],
                    'address': address['full_address']
                }
                address_list.append(addr_dict)
        else:
            pass
        person_ent = user_ent.person if user_ent.person else None
        employee_dict = {
            'employee_name': f'{user_ent.first_name} {person_ent["last_name"] if person_ent else ""}',
            'date_of_joining': user_ent.date_of_joining,
            'is_active': user_ent.is_active,
            'email': user_ent.email,
            'blood_group': person_ent["blood_group"] if person_ent else "",
            'address': address_list
        }
        return employee_dict

    @classmethod
    def get_all_employees(cls, limit=None, offset=None):
        employee_list = Employee.get_all(limit=limit, offset=offset)
        payload_list = []
        for employee in employee_list:
            employee_dict = cls.build_payload(employee)
            payload_list.append(employee_dict)
        return payload_list

    @classmethod
    def add_employee(cls, name, password, lastname, address_list, date_of_joining,
                     job_role, email, gender, marital_status, blood_group):
        try:
            new_addr_list = []
            for address in address_list:
                full_address = address['full_address']
                address_type = address['address_type']
                address = {'full_address': full_address, 'address_type': address_type}
                new_addr_list.append(address)
            pers_ent = {'last_name': lastname, 'gender': gender, marital_status: marital_status,
                        'blood_group': blood_group}
            emp_ent = Employee(first_name=name, is_active=True, job_role=job_role,
                               date_of_joining=DateTimeHelper.dt_from_string(date_of_joining),
                               email=email, secret=AppFactory.bcrypt.generate_password_hash(password),
                               addresses=new_addr_list, person=pers_ent)
            emp_ent.save()
            return emp_ent

        except Exception as e:
            raise e

    @classmethod
    def delete_employee(cls, username):
        emp = Employee.by_username(username)
        if emp:
            emp.delete_me()
            return True
        else:
            return False

    @classmethod
    def update_employee(cls, employee_ent, data):
        try:
            msg = ''
            data_keys_list = data.keys()
            person_keys_list = list(employee_ent.person.keys())
            for data_key in data_keys_list:
                if data_key in person_keys_list:
                    to_be_updated_dict = employee_ent.person
                    to_be_updated_dict.update(data)
                    employee_ent.update(person=to_be_updated_dict)
                    msg = f'Updated {data_key} for employee id: {employee_ent.email}'
                else:
                    raise CustomException(f'Error in updating for employee_id: {employee_ent.email}')
            employee_ent.save_me()
            return msg
        except Exception as e:
            raise e
