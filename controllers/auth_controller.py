from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from services.user_service import UserService
from config import Config
from models.users import UserInfo

"""URL routing and HTTP handling"""
# By Blueprint, Grouping URL, make app.py simple

auth_bp = Blueprint('auth', __name__, url_prefix = '/auth') # variable for url prefix
#  template_folder = 'templates'
service = UserService(Config()) # variable for user service
login_manager = LoginManager() # variable for manage login

@login_manager.user_loader
def load_user(user_id):
    return service.get_user_by_id(int(user_id))


@auth_bp.route('/register', methods = ['GET', 'POST'])
# GET = register rendering / POST = form data -> call user_service.create_user() and redirect, flash msg
def user_register():
    """register new account"""
    if request.method == 'POST':
        username = request.form['username']
        nickname = request.form['nickname']
        password = request.form['password']
        if service.get_user_by_username(username): # check if it is already exist
            flash('Already Exist username')
            return redirect(url_for('auth.user_register')) # before = auth.register

        user_data = {'username': username, 'nickname': nickname, 'password_hash': password}
        service.create_user(user_data)
        flash('Sign up complete')
        return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    """login account"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username and password:
            flash('Enter the ID and Password')
            return render_template('login.html')

        user = service.get_user_by_username(username)
        if user and check_password_hash(user['password_hash'], request.form['password']):
            login_user(UserInfo(id=user['id'], username = user['username'], password_hash = ''))
            return redirect(url_for('issues.list')) # if there is landing page, need to change url here
        flash('Failed to login')
        return render_template('login.html')

    return render_template('login.html')


@auth_bp.route('/delete', methods = ['POST'])
@login_required
def delete():
    """delete account"""
    service.delete_user(current_user.id)
    logout_user()
    flash('Delete Account Completed')
    return redirect(url_for('health_check')) # to main page # before = main.index


@auth_bp.route('/logout')
@login_required
def logout():
    """logout account"""
    logout_user()
    return redirect(url_for('health_check'))