from app import AppFactory
from app.services.logging_tracing_service import LoggingTracingConfig

app = AppFactory.initialize()


if __name__ == '__main__':
    app.run(port=8000)