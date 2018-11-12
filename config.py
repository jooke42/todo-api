import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    DEBUG = True

    # Define the application directory


    # ( Define the database - we are working with
    # SQLite for this example
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
