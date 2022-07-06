import jwt
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, make_response

from app import LoggingTracingConfig
from app.models.models import Employee
from swagger_stack.swagger_initialize import SwaggerConfig
from flask_restx import Resource
from library.jwt_encoder import JWTEncoder
from library.decorators import userauth, adminauth

from app.services.employee_svc import UserService, EmployeeService
from app import AppFactory

api_bp = Blueprint('api_bp', __name__, url_prefix='/v1')

swagger_route = SwaggerConfig.swagger_route


@api_bp.route('/hello_world')
def hello_world():
    return 'hello world'


@swagger_route.route('/login')
@swagger_route.expect(SwaggerConfig.login_parser)
class EmployeeLogin(Resource):
    def post(self):
        with AppFactory.tracing.start_span('first-span') as span:
            try:

                username = request.form.get('username')
                password = request.form.get('password')
                user = UserService.check_user_exists(username)
                is_pwd_correct = UserService.verify_password(user.secret, password)
                LoggingTracingConfig.logger_object.info(f"user: {username} tried to log in")
                span.set_tag('login-tag', f'user: {username} tried to log in')
                if not user or is_pwd_correct is False:
                    span.set_tag('login-tag', 'could not verify the login credentials')
                    return make_response('could not verify the login credentials', 401)
                token = JWTEncoder.encode_jwt(user)
                return make_response(jsonify({'token': token}), 201)
            except Exception as e:
                span.set_tag('login-tag', f'{e}')
                LoggingTracingConfig.logger_object.error(f"error in logging in: {e}")
                return make_response(jsonify({'error': e.args[0]}), 500)


@swagger_route.route('/get_my_detail')
@swagger_route.expect(SwaggerConfig.auth_token)
class GetEmployee(Resource):
    @userauth
    def get(*args):
        try:
            response = EmployeeService.build_payload(*args)
            return make_response(response, 200)
        except Exception as e:
            return make_response(jsonify({'error': e.args[0]}), 500)


@swagger_route.route('/get_all_details')
@swagger_route.expect(SwaggerConfig.auth_token, SwaggerConfig.limit, SwaggerConfig.offset)
class GetEmployees(Resource):
    @adminauth
    def get(self):
        try:
            limit, offset = request.args.get('limit'), request.args.get('offset')
            response = EmployeeService.get_all_employees(limit, offset)
            return make_response(jsonify({'employees_list': response}), 200)
        except Exception as e:
            return make_response(jsonify({'error': e.args[0]}), 500)


@swagger_route.route('/add_employee')
@swagger_route.expect(SwaggerConfig.auth_token, SwaggerConfig.new_user)
class AddEmployee(Resource):
    @adminauth
    def post(self):
        with AppFactory.tracing.start_span('add-employee') as span:
            try:
                first_name = request.json.get('first_name')
                last_name = request.json.get('last_name')
                date_of_joining = request.json.get('date_of_joining')
                job_role = request.json.get('job_role')
                email = request.json.get('email')
                gender = request.json.get('gender')
                marital_status = request.json.get('marital_status')
                blood_group = request.json.get('blood_group')
                address_list = request.json.get('address')
                password = first_name
                user = UserService.check_user_exists(email)
                if not user:
                    employee_id = EmployeeService.add_employee(first_name, password, last_name, address_list,
                                                               date_of_joining,
                                                               job_role, email, gender, marital_status, blood_group)
                    LoggingTracingConfig.logger_object.info(f"User created and his employee_id:{employee_id.id.__str__()}")
                else:
                    return make_response(f'user already exists with email: {email}', 209)
                return make_response(jsonify({'employee_id': employee_id.id.__str__(), 'username': email, 'password': first_name}),
                                     200)
            except Exception as e:
                span.set_tag('add-user-tag')
                # AppFactory.tracing.start_span().error('its an error maithreyan')
                LoggingTracingConfig.logger_object.error(f"Error in adding user: {e}")
                return make_response(jsonify({'error': e.args[0]}), 500)


@swagger_route.route('/delete_employee')
@swagger_route.expect(SwaggerConfig.auth_token, SwaggerConfig.delete_input)
class DeleteEmployee(Resource):
    @adminauth
    def delete(self):
        try:
            username = request.args.get('username')
            delete_response = EmployeeService.delete_employee(username)
            LoggingTracingConfig.logger_object.info(f"User: {username} was attempted to delete")
            if not delete_response:
                return make_response('record not found or already deleted', 404)
            LoggingTracingConfig.logger_object.info(f"User: {username} was deleted")
            return make_response(f'User {username} deleted', 204)
        except Exception as e:
            LoggingTracingConfig.logger_object.error(f"Error in deleting user: {e}")
            return make_response(jsonify({'error': e.args[0]}), 500)


@swagger_route.route('/update_employee')
@swagger_route.expect(SwaggerConfig.auth_token, SwaggerConfig.update_user)
class UpdateEmployee(Resource):
    @userauth
    def put(self):
        try:
            username = request.json.get('username')
            employee_ent = UserService.check_user_exists(username)
            request.json.pop('username')
            if not employee_ent:
                return make_response('record not found or deleted', 404)
            update_response = EmployeeService.update_employee(employee_ent, request.json)
            LoggingTracingConfig.logger_object.info(f"User: {username} was updated")
            return make_response(update_response, 200)
        except Exception as e:
            LoggingTracingConfig.logger_object.error(f"Error in updating user: {e}")
            return make_response(jsonify({'error': e.args[0]}), 500)
