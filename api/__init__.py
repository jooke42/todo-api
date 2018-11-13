from flask import Flask
from flask_restplus import Api

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import ProductionConfig

api = Api()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=ProductionConfig):
    """
    Entry point to the Flask RESTful Server application.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    return app


from api import routes, models
