from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from my_app import db

from ..forms import LoginForm, RegistrationForm
from ..models import Products, User

home = Blueprint(
    'home_bp', __name__
)



@home.route("/register", methods=["GET", "POST"])
def register():    
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = RegistrationForm()
    if form.validate_on_submit(): # From FLaskForm Base class: detects & validates POST requests
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
               username=form.username.data, 
               email=form.email.data,
               password=form.password.data # Pasword was auto hashed: Check 'User' class in models.py
            )
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for('home_bp.index')) # Blueprint name might be ommited and url_for still works; url_for(.index)
        flash('A user already exists with that email address.')
    return render_template(
        'home/index.html',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account.")


@home.route("/")
@login_required
def index():
    products = Products.query.all()
    return render_template('index.html', products=products )



@home.route("/login", methods=["GET", "POST"])
def login():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated: # From UserMixin Base class in models module: verifies if user is logged in
        return redirect(url_for('home_bp.index'))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user and user.is_correct_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home_bp.index'))
        flash('Invalid username/password combination')
        return redirect(url_for('home_bp.login'))
    return render_template(
        'login.html',
        form=form,
        title='Log in.',
        template='login-page',
        body="Log in with your User account."
    )





@home.route("/logout")
def logout():
    """Log user out"""

    logout_user()
    return redirect(url_for('home_bp.login'))
