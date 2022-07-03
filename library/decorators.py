from functools import wraps

import jwt
from flask import request, jsonify, make_response
from config import Config
from app.models.models import Employee


def userauth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'authToken' in request.headers:
            token = request.headers['authToken']
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            data = jwt.decode(token, Config.secret_key)
            current_user = Employee.by_id(data['user_id'])
        except Exception as e:
            return make_response('invalid token', 401)
        return func(current_user)

    return decorated


def adminauth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'authToken' in request.headers:
            token = request.headers['authToken']
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            data = jwt.decode(token, Config.secret_key)
            current_user = Employee.by_id(data['user_id'])
            if current_user.job_role != 'admin':
                return make_response('unauthorized to perform operation', 403)
        except Exception as e:
            return make_response('invalid token', 401)
        return func(current_user)

    return decorated
