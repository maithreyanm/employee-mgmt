# importing module
import datetime
import logging
from library.datetime_helper import DateTimeHelper
from jaeger_client import Config


class LoggingTracingConfig:
    logger_object = None
    tracing_obj = None

    @classmethod
    def logging_tracing_initialize(cls, db):
        logging.basicConfig(filename=DateTimeHelper.now_datetime_to_string(),
                            format="%(asctime)s | %(name)s | %(levelname)s | %(message)s", filemode='w')
        cls.logger_object = logging.getLogger()
        cls.logger_object.setLevel(logging.DEBUG)
        cls.logger_object.info("Logging initialized")
        config = Config(
            config={
                'enabled': True,
                'sampler': {
                    'type': 'const',
                    'param': 1,
                },
                'logging': True,
            },
            service_name='employee-mgmt',
            validate=True,
        )
        cls.tracing_obj = config.initialize_tracer()
        return cls.tracing_obj