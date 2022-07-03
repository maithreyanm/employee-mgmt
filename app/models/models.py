import datetime

import sqlalchemy
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.models import SQLAConfig as sqla

base = declarative_base()


class BaseModel(base):
    __abstract__ = True
    pid = Column('pid', Integer, primary_key=True)
    created_on = Column('created_on', sqlalchemy.DateTime, default=datetime.datetime.now())
    updated_on = Column('updated_on', sqlalchemy.DateTime, default=datetime.datetime.now(),
                        onupdate=datetime.datetime.now())

    # def __init__(self):
    #     self.new_records = []

    def save_me(self):
        try:
            sqla.session.add(self)
            sqla.session.commit()
        except Exception as e:
            sqla.session.rollback()
            raise e

    def delete_me(self):
        try:
            sqla.session.delete(self)
            sqla.session.commit()
        except Exception as e:
            sqla.session.rollback()
            raise e

    @classmethod
    def by_id(cls, id):
        try:
            q = sqla.session.query(cls)
            q = q.filter(cls.pid == id)
            record = q.scalar()
            return record
        except Exception as e:
            sqla.session.rollback()
            raise e

    @classmethod
    def get_all(cls, limit=None, offset=None):
        try:
            q = sqla.session.query(cls)
            if limit and offset:
                q = q.limit(limit).offset(offset)
            q = q.all()
            return q
        except Exception as e:
            sqla.session.rollback()
            raise e

    @classmethod
    def by_key_val(cls, key_val):
        try:
            query = sqla.session.query(cls)
            for key, val in key_val.items():
                attrib = getattr(cls, key)
                query = query.filter(attrib == val)
            entities = query.all()
            return entities
        except Exception as e:
            sqla.session.rollback()
            raise e

    @classmethod
    def by_ids(cls, ids):
        try:
            query = sqla.session.query(cls)
            entities = query.filter(cls.pid.in_(ids)).all()
            return entities
        except Exception as e:
            sqla.session.rollback()
            raise e


class Employee(BaseModel):
    __tablename__ = 'Employee'
    first_name = Column('first_name', String(50))
    date_of_joining = Column('date_of_joining', Date)
    is_active = Column('is_active', Boolean)
    job_role = Column('job_role', String(30))
    email = Column('email', String(30))
    '''backref is a shortcut for configuring both parent.children and child.parent relationships
    at one place only on the parent or the child class (not both)..
    back_populates is just the opposite'''

    '''lazy is used to get the contents of the table, when we try to query the child table by Employee.person.pid
    it makes another db call'''
    person = relationship("Person", backref="Employee", cascade="all, delete", lazy='joined')
    addresses = relationship("Address", backref="Employee", cascade="all, delete", lazy='joined')
    secrets = relationship("Secrets", backref="Employee", cascade="all, delete", lazy='select')

    def __repr__(self):
        return "<Employee %s>" % self.pid

    @classmethod
    def by_name(cls, name_string):
        key_val_dict = {'first_name': name_string}
        records = cls.by_key_val(key_val_dict)
        return records

    @classmethod
    def by_email(cls, email):
        employee = cls.by_key_val({'email': email})
        return employee


class Person(BaseModel):
    __tablename__ = 'Person'
    employee_key = Column('employee_key', Integer, sqlalchemy.ForeignKey('Employee.pid'))
    last_name = Column('last_name', String(100))
    gender = Column('gender', String(1))
    marital_status = Column('marital_status', String(10))
    blood_group = Column('blood_group', String(10))

    def __repr__(self):
        return "<Person %s>" % self.pid


class Address(BaseModel):
    __tablename__ = 'Address'
    employee_key = Column('employee_key', Integer, sqlalchemy.ForeignKey('Employee.pid'))
    full_address = Column('full_address', String(10))
    address_type = Column('address_type', String(10))

    def __repr__(self):
        return "<Address %s>" % self.pid

    @classmethod
    def by_employee_key(cls, emp_key):
        addresses = cls.by_key_val({'employee_key': emp_key})
        return addresses


class Secrets(BaseModel):
    __tablename__ = 'Secrets'
    login_password = Column('login_password', String(100))
    employee_key = Column('employee_key', Integer, sqlalchemy.ForeignKey('Employee.pid'))

    def __repr__(self):
        return "<Secrets %s>" % self.pid
