from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField, StringField
from wtforms.validators import InputRequired, Email, EqualTo

class SignInForm(FlaskForm):
    email = StringField('Email Address', [Email(), InputRequired(message='Enter your email address.')])
    password = PasswordField('Password', [InputRequired(message = 'Enter your password.')])

class SignUpForm(FlaskForm):
    email = StringField('Email Address', [Email(), InputRequired(message='Enter your email address.')])
    name = StringField('Name', [InputRequired(message='Enter your name.')])
    password = PasswordField('Password', [InputRequired(message = 'Enter your password.')])
    confirm_password = PasswordField('Password', [EqualTo(password, 'Passwords must match.')])