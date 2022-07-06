from flask_restx import Api, fields
from flask import Flask, Blueprint


class SwaggerConfig:
    swagger_route = None
    login_parser = None
    auth_token = None
    new_user = None
    update_user = None
    delete_input = None
    limit = None
    offset = None

    @classmethod
    def initialize(cls, app):
        blueprint = Blueprint('api', __name__, url_prefix='/v1')
        api = Api(blueprint)
        app.register_blueprint(blueprint)
        cls.swagger_route = api.namespace('employee-mgmt', description='Employee Swagger')
        add_user = api.parser()
        cls.swagger_inputs(api)
        cls.auth_token_input(api)
        cls.new_user_input(api)
        cls.update_user_input(api)
        cls.delete_user_input(api)
        cls.limit = api.parser().add_argument('limit', type=int, location='body', required=False)
        cls.offset = api.parser().add_argument('offset', type=int, location='body', required=False)

    @classmethod
    def swagger_inputs(cls, api):
        cls.login_parser = api.parser()
        user_form = cls.login_parser.add_argument('username', type=str, location='form', help='Username/Email',
                                                  required=True)
        pwd_form = cls.login_parser.add_argument('password', type=str, location='form', help='Password', required=True)

    @classmethod
    def auth_token_input(cls, api):
        cls.auth_token = api.parser()
        auth_token = cls.auth_token.add_argument('authToken', type=str, location='headers', help='authToken',
                                                 required=True)

    @classmethod
    def update_user_input(cls, api):
        cls.update_user = api.model('Resource2', {'username': fields.String})

    @classmethod
    def delete_user_input(cls, api):
        cls.delete_input = api.parser()
        username = cls.delete_input.add_argument('username', type=str, location='body', help='username',
                                                    required=True)

    @classmethod
    def new_user_input(cls, api):
        address_fields = api.model('address', {
            'full_address': fields.String,
            'address_type': fields.String,
        })
        cls.new_user = api.model('Resource', {
            'first_name': fields.String,
            'last_name': fields.String,
            'date_of_joining': fields.Date,
            'job_role': fields.String,
            'email': fields.String,
            'gender': fields.String,
            'marital_status': fields.String,
            'blood_group': fields.String,
            'address': fields.List(fields.Nested(address_fields))})
