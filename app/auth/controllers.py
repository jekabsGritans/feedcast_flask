from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.auth.forms import SignInForm, SignUpForm
from app.auth.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/test/', methods=['POST','GET'])
def test():
    return redirect('google.com')

@auth.route('/signin/', methods=['POST','GET'])
def signin():
    form = SignInForm(request.form)
    if form.validate_on_submit():
        if 'signup' in request.form:
            session['tmp_usr'] = {"name":'example', "email":form.email, "password":form.password}
            return redirect(url_for('auth.signup'))
        
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user'] = user.id
            if 'url' in session:
                return redirect(session['url'])
            else:
                return redirect()
        flash('Incorrect email or password')
    return render_template('auth/signin.html',form=form)

@auth.route('/signup/', methods=['POST','GET'])
def signup():
    form = SignUpForm(request.form,)#obj=User(**session.pop('tmp_usr',None)))
    
    if form.validate_on_submit():
        # user = User(**session.pop('tmp_usr', None))
        user=User()
        form.populate_obj(user)
        # db.session.add(user)
        if 'url' in session:
            return redirect(session['url'])
        else:
            return redirect()
    form = SignUpForm(obj=User(name='example',email='example@exm.com',password='password123'))
    return render_template('auth/signup.html', form=form)
        
@auth.route('/singout/')
def signout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('auth.signin'))