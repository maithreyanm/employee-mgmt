from app import AppFactory
from app.services.logging_tracing_service import LoggingTracingConfig

app = AppFactory.initialize()


if __name__ == '__main__':
    app.run(port=8000)

    # http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/
    # https://flask-appbuilder.readthedocs.io/en/latest/quickcharts.html
    # https://pythonbasics.org/flask-mongodb/