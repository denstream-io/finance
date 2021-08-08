"""Flask configuration"""
from decouple import config
from pathlib import Path

filepath = Path(__file__)
basedir = str(filepath.absolute().parent.joinpath('finance.db'))

class Config:
    """Sets Flask config variables."""

    # Basic Configuration
    SECRET_KEY = config('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    #SESSION_COOKIE_NAME = config('SESSION_COOKIE_NAME')

class ProdConfig(Config): # Inherits from Config class
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

    # Database 
    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir  # Gets absolute path of database file


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False

     # Database 
    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir 


