from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.orm import load_only, session
from my_app import db, bcrypt


from ..forms import LoginForm, RegistrationForm
from ..models import UserActivities, User
from ..helpers import lookup

home = Blueprint(
    'home_bp', __name__
)



@home.route("/login", methods=["GET", "POST"])
@home.route("/", methods=["GET", "POST"])
def login():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    # if current_user.is_authenticated: # From UserMixin Base class in models module: verifies if user is logged in
    #     return redirect(url_for('home_bp.index'))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user and user.is_correct_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('.index'))
        flash('Invalid username/password combination')
        return redirect(url_for('home_bp.login'))
    return render_template(
        'home/login.html',
        form=form,
        title='Log in.',
        template='login-page',
        body="Log in with your User account."
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
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user = User(
               username=form.username.data, 
               email=form.email.data,
               password=hashed_password 
            )
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for('home_bp.index')) # Blueprint name might be ommited and url_for still works; url_for(.index)
        flash('A user already exists with that email address.')
    return render_template(
        'home/register.html',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account.")


@home.route("/index", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    # Query database to get a particular user cash or cash balance
    user_info = User.query.filter_by(username=current_user.username).first()
    cash_balance = user_info.cash

    grand_total = cash_balance

    user_activities = UserActivities.query.all()
    for row in user_activities:
        quote = lookup(row["symbols"]) # Query IEX for fresh updates
        total = row["shares"] * quote["price"]
        setattr(User,*{"price": quote["price"], "total": total}) # Updates stocks price and total in database
        session.commit()
        grand_total += total

    return render_template(
        'home/index.html',
        title='index',
        user_activities=user_activities, 
        cash_balance=cash_balance, 
        grand_total=grand_total,
        template='index-page'
    )


@home.route("/logout")
def logout():
    """Log user out"""

    logout_user()
    return redirect(url_for('home_bp.login'))
