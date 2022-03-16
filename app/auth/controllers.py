from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
from app import db
from app.auth.forms import LoginForm
from app.auth.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/signin/', methods=['POST','GET'])
def signin():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() 
        if user and check_password_hash(user.password, form.password.data):
            session['user'] = user.id
            flash(f'Hello {user.name}!')
            if 'url' in session:
                return redirect(session['url'])
            else:
                return redirect() 
        flash('Incorrect email or password', 'error-message')
    return render_template('auth/signin.html',form=form)

@auth.route('/singout/')
def signout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('auth.signin'))