import os



class BaseConfig:
    SECRET_KEY = 'may_the_force_be_with_you'
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                             'sqlite:///%s' % (os.path.join(PROJECT_ROOT, "app.db"))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = False
    ERROR_404_HELP = False


class ProductionConfig(BaseConfig):
    SECRET_KEY = os.getenv('SECRET_KEY_TODO')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABSASE_URI_TODO')

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True

    # Use in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
