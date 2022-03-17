from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email, EqualTo

class LoginForm(Form):
    email = TextField('Email Address', [Email(), Required(message='Enter your email address.')])
    password = PasswordField('Password', [Required(message = 'Enter your password.')])