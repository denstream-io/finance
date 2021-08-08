from datetime import datetime

from flask_login import UserMixin # Gives access to 4 Useful function
from sqlalchemy.ext.hybrid import hybrid_property

from my_app import bcrypt, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Checks if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(int(user_id))
    return None


class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    cash = db.Column(db.Integer, nullable=False, default=100000)
    user =  db.relationship('Products', backref='customer', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.cash}')"

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext) # Auto hashes password before storing

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext) # Confirms password on login


class Products(db.Model):

    __tablename__ = 'Products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shares = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    symbols = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __repr__(self):
        return f"Products('{self.symbols}', '{self.shares}', '{self.price}')"



class TransactionHistory(db.Model):

    __tablename__ = 'finance'

    id = db.Column(db.Integer, primary_key=True)
    symbols = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stocks = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"('{self.stock}', '{self.price}', '{self.date}')"

