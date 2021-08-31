from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError

from .models import User
from .helpers import NoDuplicates

class RegistrationForm(FlaskForm):

    username = StringField(
        'Username',
        validators=[
            DataRequired(), 
            Length(min=2, max=20),
            NoDuplicates( 
                User,
                User.email,
                message='There is already an account with that username.'
            )
        ]
    )
    email = StringField(
        'Email',
        validators=[
            Email(),
            DataRequired(),
            NoDuplicates( 
                User,
                User.email,
                message='There is already an account with that email.'
            )
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, message='Select a stronger password.')
        ]
    )
    confirm_password = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Sign Up')



class LoginForm(FlaskForm):

    """User Log-in Form."""

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class BuyForm(FlaskForm):

    symbol =  StringField(
        'Symbols',
        validators=[
            DataRequired(), 
            Length(min=2, max=20),
        ]
    )

    shares = DecimalField(
        'Shares',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField('Buy')