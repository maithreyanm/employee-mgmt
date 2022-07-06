from flask_mongoengine import MongoEngine


class MongoConfig:
    mongo_db = None

    @classmethod
    def initialize(cls, app):
        app.config["MONGO_URI"] = "mongodb://localhost:27017/employee-mgmt"
        # mongo = PyMongo(app)
        cls.mongo_db = MongoEngine()
        cls.mongo_db.init_app(app)
        return cls.mongo_db