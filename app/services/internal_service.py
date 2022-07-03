from app.services.logging_tracing_service import LoggingTracingConfig


class InternalService:

    @classmethod
    def super_user_creation(cls):
        try:
            # most possibly circular import will happen so imported locally
            from app import AppFactory
            from app.models.models import Employee, Secrets
            from app.services.employee_svc import UserService

            super_user = UserService.check_user_exists(username='superuser')
            if not super_user:
                emp_ent = Employee()
                emp_ent.first_name = 'superuser'
                emp_ent.email = 'superuser'
                emp_ent.job_role = 'admin'
                emp_ent.is_active = True
                secr_ent = Secrets(login_password=AppFactory.bcrypt.generate_password_hash(emp_ent.first_name))
                emp_ent.secrets.append(secr_ent)
                emp_ent.save_me()
                LoggingTracingConfig.logger_object.info("Superuser created")
            else:
                pass
        except Exception as e:
            LoggingTracingConfig.logger_object.error(f"error in super user creation:{e}")
            raise e
