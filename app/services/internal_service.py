from app.services.logging_tracing_service import LoggingTracingConfig


class InternalService:

    @classmethod
    def super_user_creation(cls, db):
        try:
            # most possibly circular import will happen so imported locally
            from app import AppFactory
            from app.models.models import Employee
            from app.services.employee_svc import UserService
            super_user = UserService.check_user_exists(username='superuser')
            if not super_user:
                first_name = 'superuser'
                emp_ent = Employee(first_name=first_name, email='superuser', is_active=True, job_role='admin',
                                   secret=AppFactory.bcrypt.generate_password_hash(first_name))
                emp_ent.save()
                LoggingTracingConfig.logger_object.info("Superuser created")
            else:
                pass
        except Exception as e:
            LoggingTracingConfig.logger_object.error(f"error in super user creation:{e}")
            raise e
