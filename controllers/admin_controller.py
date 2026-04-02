from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from services.project_service import ProjectService
from services.user_service import UserService
from config import Config
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
project_service = ProjectService(Config())
user_service = UserService(Config())


def admin_required(f):
    """Admin Only"""
    @wraps(f)
    #wraps will store original function's meta info
    # if not, when Flask register the route func, all decorator's func name will be 'decorated'
    def decorated(*args, **kwargs):
        # args can accept unlimited positional arguments like f(1, 2, 3 ...) -> args = (1, 2, 3 ...)
        # kwargs can accept unlimited keyword arguments f(x=1, x=2...) -> kwargs = { 'x':1, 'y':2 ...}
        # Cuz don't know what f will take as an arguments
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access only')
            return redirect(url_for('issue.issue_list_page'))
        return f(*args, **kwargs)
    return decorated


def manager_required(f):
    """Admin and Manager both"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ('admin', 'manager'):
            flash('Access Denied')
            return redirect(url_for('issue.issue_list_page'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/', methods = ['GET'])
@login_required
@manager_required
def admin_page():
    projects = project_service.get_all_projects()
    users = user_service.get_all_users() if current_user.role == 'admin' else None
    return render_template('admin.html', projects = projects, users = users)


# Project CRUD ------

@admin_bp.route('/project/create', methods = ['POST'])
@login_required
@manager_required
def create_project():
    name = request.form.get('name')
    description = request.form.get('description', '')
    # in the get(key, default) format, '' is for defense code, not to put 'None' in the DB.
    if not name:
        flash('Project name required')
        return redirect(url_for('admin.admin_page'))
    project_service.create_project(name, description)
    flash(f'Project {name} has been created')
    return redirect(url_for('admin.admin_page'))


@admin_bp.route('/project/<int:project_id>/update', methods = ['POST'])
@login_required
@manager_required
def update_project(project_id: int):
    name = request.form.get('name')
    description = request.form.get('description')
    if not name:
        flash('Project Name required')
        return redirect(url_for('admin.admin_page'))
    project_service.update_project(project_id, name, description)
    flash(f'Project has been updated')
    return redirect(url_for('admin.admin_page'))


@admin_bp.route('/project/<int:project_id>/delete', methods = ['POST'])
@login_required
@manager_required
def delete_project(project_id: int):
    project_service.delete_project(project_id)
    flash('Project has been deleted')
    return redirect(url_for('admin.admin_page'))


# User Role Manage ------

@admin_bp.route('/user/<int:user_id>/role', methods = ['POST'])
@login_required
@admin_required
def update_user_role(user_id: int):
    role = request.form.get('role')
    if role not in ('user', 'admin', 'manager'):
        flash('Invalid role')
        return redirect(url_for('admin.admin_page')) # Maybe better to redirect to other page?
    user_service.update_user_role(user_id, role)
    flash("User role has been updated")
    return redirect(url_for('admin.admin_page'))