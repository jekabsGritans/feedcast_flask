from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo


class SignInForm(FlaskForm):
    email = StringField('Email Address') #, [Email(), InputRequired(message='Enter your email address.')])
    password = PasswordField('Password')#, [InputRequired(message = 'Enter your password.')])
    submit = SubmitField('Sign In')

class SignUpForm(FlaskForm):
    email = StringField('Email Address', [Email(), InputRequired(message='Enter your email address.')])
    name = StringField('Name', [InputRequired(message='Enter your name.')])
    password = PasswordField('Password', [InputRequired(message = 'Enter your password.')])
    confirm_password = PasswordField('Confirm Password', [EqualTo('password', 'Passwords must match.')])
    submit = SubmitField('Sign Up')
