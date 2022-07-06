import jwt

from datetime import datetime, timedelta
from config import Config


class JWTEncoder():

    @classmethod
    def encode_jwt(cls, user):
        token = jwt.encode({
            'user_id': user.id.__str__(),
            'username': user.first_name,
            'role': user.job_role
        }, Config.secret_key)
        return token.decode('utf-8')
