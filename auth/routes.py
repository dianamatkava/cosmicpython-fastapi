from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash

from auth.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login')
def login():
    print(current_user)
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    return render_template('auth/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    # remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=True)
    return redirect(url_for('admin.index'))

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
