from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.auth.forms import SignInForm, SignUpForm
from app.auth.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/signin/', methods=['POST','GET'])
def signin():
    form = SignInForm(request.form)
    if form.validate_on_submit():
        if 'signup' in request.form:
            return redirect(url_for('auth.signup'))
        
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user'] = user.id
            if 'url' in session:
                return redirect(session['url'])
            else:
                return redirect('/')
        flash('Incorrect email or password')
    return render_template('auth/signin.html', form=form)

@auth.route('/signup/', methods=['POST','GET'])
def signup():
    form = SignUpForm(request.form)
    if form.validate_on_submit():
        if 'signin' in request.form:
            return redirect(url_for('auth.signin'))
        
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email address already registered')
            return redirect(url_for('auth.signup'))
        user = User(
            email=form.email.data,
            name=form.name.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        session['user'] = user.id
        return redirect(url_for('podcast.index'))
    return render_template('auth/signup.html', form=form)
        
@auth.route('/singout/')
def signout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('auth.signin'))