from flask import Flask
from config import Config
from flask_restplus import Api


app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

from api import routes
