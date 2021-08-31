

"""Initialize app."""

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy # Enables easy linkage to original sqlalchemy modules
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
# from flask_session import Session # Pending Import


db = SQLAlchemy() # Gives access to Model class 
bcrypt = Bcrypt()
toolbar = DebugToolbarExtension()
# session = Session()

login_manager = LoginManager()
login_manager.login_view =  "home_bp.login"
login_manager.login_message_category = 'info'



def create_app(): # Flask Factory function
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object('config.DevConfig')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    toolbar.init_app(app)
    # session.init_app(app)

    with app.app_context():
        from .helpers import NoDuplicates, lookup, usd
        from .forms import RegistrationForm, LoginForm, BuyForm
        from .models import User, UserActivities, TransactionHistory
        from .views.home import home
        from .views.finance import finance


        # Register Blueprints
        app.register_blueprint(home)
        app.register_blueprint(finance)

        # Custom filter
        app.jinja_env.filters["usd"] = usd


        # Create Database Models
        db.create_all()

    return app
