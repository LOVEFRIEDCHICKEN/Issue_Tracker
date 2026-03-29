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
    service.delete_user_by_id(current_user.id)
    logout_user()
    flash('Delete Account Completed')
    return redirect(url_for('health_check')) # to main page # before = main.index


@auth_bp.route('/logout')
@login_required
def logout():
    """logout account"""
    logout_user()
    return redirect(url_for('health_check'))

@auth_bp.route('/delete_account', methods = ['GET'])
@login_required
def delete_account_page():
    """Delete account page landing"""
    return render_template('delete_account.html')

@auth_bp.route('/delete_account', methods = ['POST'])
@login_required
def delete_account():
    """Check Password and Soft Delete"""
    password = request.form.get('Password') # need to check if this name is right or not
    user = service.get_user_by_username(current_user.username)

    if not user or not check_password_hash(user['password_hash'], password):
        flash('Incorrect Password')
        return redirect(url_for('auth.delete_account_page')) # is this really right name?? need to check

    success = service.delete_user_by_id(current_user.id) # need to make other def and need to change here
    if not success:
        flash('There is an error for delete account')
        return redirect(url_for('auth.delete_account_page'))

    logout_user()
    flash('Delete complete')
    return redirect(url_for('health_check')) # if I change landing page, need to change here