from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash

from flask_login import login_user, logout_user
from flask_quiz_app.models import User
from flask_quiz_app.extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    error_message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username = username).first()

        if not user:
            error_message = 'Invalid username.'
        elif not check_password_hash(user.password, password):
            error_message = 'Invalid password.'
        else:
            login_user(user)
            return redirect(url_for('main_routes.home'))

    return render_template('login.html', title = 'Login', navbar_title = 'Login', error_message = error_message)

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    error_message = ''
    if request.method == 'POST':
        username = request.form['username']
        fullname = request.form['fullname']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if '' in [username, fullname, email, password1, password2]:
            error_message = 'All fields are required.'
        elif password1 != password2:
            error_message = 'Passwords do not match.'
        else:
            new_user = User(
                username = username,
                full_name = fullname,
                email = email,
                admin = False,
                teacher = False
            )
            new_user.gen_hashed_password(password1)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('auth.login'))

    return render_template('register.html', title = 'Register', navbar_title = 'Create an Account', error_message = error_message)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_routes.home'))