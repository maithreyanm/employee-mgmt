from flask import Flask
from config import Config
from flask_cors import CORS
from app.models import SQLAConfig
from swagger_stack.swagger_initialize import SwaggerConfig
from flask_bcrypt import Bcrypt
from app.services.internal_service import InternalService
from app.services.logging_tracing_service import LoggingTracingConfig


class AppFactory:
    bcrypt = None
    tracing = None

    @classmethod
    def initialize(cls):
        try:
            app = Flask(__name__)
            config = Config()
            CORS(app)
            app.config['SECRET_KEY'] = config.secret_key
            SwaggerConfig.initialize(app)
            cls.bcrypt = Bcrypt(app)

            from app.api.api import api_bp
            app.register_blueprint(api_bp)

            SQLAConfig.initialize()
            cls.tracing = LoggingTracingConfig.logging_tracing_initialize()
            InternalService.super_user_creation()
            with app.app_context():
                pass
            LoggingTracingConfig.logger_object.info("App factory created")
            return app

        except Exception as e:
            LoggingTracingConfig.logger_object.info(f"Error in app factory creation: {e}")
            print(e)