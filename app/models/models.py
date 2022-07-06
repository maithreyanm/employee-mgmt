from datetime import datetime

from mongoengine import Document
from mongoengine import StringField, ReferenceField, ListField, BooleanField, DateField, DateTimeField, EmbeddedDocumentField, DictField


class Base:
    created_on = DateTimeField(default=datetime.now)
    updated_on = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        if not self.created_on:
            self.created_on = datetime.now()
        self.updated_on = datetime.now()
        return super(Base, self).save(*args, **kwargs)


class Person(Document):
    __tablename__ = 'Person'

    last_name = StringField(max_length=60, required=True)
    gender = StringField(max_length=1, required=True)
    marital_status = StringField(max_length=60, required=True)
    blood_group = StringField(max_length=60, required=True)

    def __repr__(self):
        return "<Person %s>" % self.last_name


class Address(Document):
    __tablename__ = 'Address'
    DBRef = False
    full_address = StringField(max_length=60, required=True)
    address_type = StringField(max_length=60, required=True)

    def __repr__(self):
        return "<Address %s>" % self.full_address


class Employee(Document, Base):
    __tablename__ = 'Employee'
    first_name = StringField(max_length=60, required=True)
    date_of_joining = DateField()
    is_active = BooleanField()
    job_role = StringField(max_length=60, required=True)
    email = StringField(max_length=60, required=True, unique=True)
    person = DictField()
    addresses = ListField(DictField())
    secret = StringField(max_length=100, required=True)

    def __repr__(self):
        return "<Employee %s>" % self.first_name

    @classmethod
    def by_id(cls, id):
        try:
            q = cls.objects(id=id).first()
            return q
        except Exception as e:
            raise e

    @classmethod
    def by_username(cls, username):
        try:
            q = cls.objects(email=username).first()
            return q
        except Exception as e:
            raise e

    @classmethod
    def get_all(cls, limit=None, offset=None):
        try:
            if limit and offset:
                q = cls.objects.limit(limit).skip(offset)
            else:
                q = cls.objects
            return q
        except Exception as e:
            raise e

    def delete_me(self):
        try:
            self.delete()
        except Exception as e:
            raise e

    def update_me(self):
        try:
            self.update()
        except Exception as e:
            raise e