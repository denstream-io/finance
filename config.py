"""Flask configuration"""
import os
from urllib.parse import quote_plus as urlquote

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Sets Flask config variables."""

    # Basic Configuration
    try:
        SECRET_KEY = os.environ["SECRET_KEY"] # set a 'SECRET_KEY' to enable the Flask session cookies
    except KeyError:
        raise RuntimeError("API_KEY not set")

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Database 
    SQLALCHEMY_TRACK_MODIFICATION = False

class ProdConfig(Config): # Inherits from Config class
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

    # Database 
    SQLALCHEMY_DATABASE_URI = "postgresql://username:%s@hostname:port/database" % urlquote('password') # Gets absolute path of database file


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False

     # Database 
    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,  'finance.db') 

    # Flask-Toolbar
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = True


