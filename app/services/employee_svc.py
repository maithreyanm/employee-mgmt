from app.models import SQLAConfig as sqla
from app.models.models import Employee, Address, Person, Secrets
from app import AppFactory
from library.datetime_helper import DateTimeHelper
from sqlalchemy import orm


class CustomException(Exception):
    pass


class UserService:

    @classmethod
    def check_user_exists(cls, username):
        employee = Employee.by_email(username)
        if len(employee) == 0:
            return None
        else:
            return employee[0]

    @classmethod
    def verify_password(cls, hashed_password, password):
        is_matched = AppFactory.bcrypt.check_password_hash(hashed_password, password)
        return True if is_matched else False


class EmployeeService:

    @classmethod
    def build_payload(cls, user_ent):
        address_list = []
        if len(user_ent.addresses) != 0:
            for address in user_ent.addresses:
                addr_dict = {
                    'address_type': address.address_type,
                    'address': address.full_address
                }
                address_list.append(addr_dict)
        else:
            pass
        person_ent = user_ent.person[0] if len(user_ent.person) else None
        employee_dict = {
            'employee_name': f'{user_ent.first_name} {person_ent.last_name if person_ent else ""}',
            'date_of_joining': user_ent.date_of_joining,
            'is_active': user_ent.is_active,
            'email': user_ent.email,
            'blood_group': person_ent.blood_group if person_ent else "",
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
    def get_all_employees_limit_offset(cls, limit, offset):
        query = sqla.session.query(Employee)
        query = query.options(orm.joinedload('person'))
        query = query.options(orm.joinedload('addresses'))
        query = query.limit(limit).offset(offset)
        query = query.all()
        return query

    @classmethod
    def add_employee(cls, name, password, lastname, address_list, date_of_joining,
                     job_role, email, gender, marital_status, blood_group):
        try:
            emp_ent = Employee()
            for address in address_list:
                full_address = address['full_address']
                address_type = address['address_type']
                add = Address(full_address=full_address, address_type=address_type)
                emp_ent.addresses.append(add)
            pers_ent = Person(last_name=lastname, gender=gender, marital_status=marital_status,
                              blood_group=blood_group)
            secr_ent = Secrets(login_password=AppFactory.bcrypt.generate_password_hash(password))
            emp_ent.is_active = True
            emp_ent.job_role = job_role
            emp_ent.date_of_joining = DateTimeHelper.dt_from_string(date_of_joining)
            emp_ent.first_name = name
            emp_ent.email = email
            emp_ent.secrets.append(secr_ent)
            emp_ent.person.append(pers_ent)

            emp_ent.save_me()
            return emp_ent

        except Exception as e:
            raise e

    @classmethod
    def delete_employee(cls, id=None):
        emp = Employee.by_id(id)
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
            person_keys_list = Person().__table__.columns.keys()
            for data_key in data_keys_list:
                if data_key in person_keys_list:
                    # indexing as employee-person has 1-1 relationship so for one employee would be one person record
                    exec(f"employee_ent.person[0].{data_key}=\'{data[data_key]}\'")
                    msg = f'Updated {data_key} for employee id: {employee_ent.pid}'
                else:
                    raise CustomException(f'Error in updating for employee_id: {employee_ent.pid}')
            employee_ent.save_me()
            return msg
        except Exception as e:
            raise e
