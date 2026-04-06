from flask import Blueprint, request, jsonify, render_template, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from controllers.admin_controller import project_service
from services.project_service import ProjectService
from services.issue_service import IssueService
from config import Config
from typing import Dict, Any

issue_bp = Blueprint('issue', __name__, url_prefix='/api/issues') # flask blueprint's route decorator
service = IssueService(Config())


@issue_bp.route('/new', methods = ['GET'])
@login_required
def register_issue_page():
    """Render page for Register New Issue"""
    projects = project_service.get_all_projects()
    return render_template('register_new_issue.html', projects = projects)


@issue_bp.route('/', methods=['POST']) # connect and post to api/issues/
@login_required
def create_issue():
    """Add issue - Form Post or JSON API"""
    try:
        # Form (submit from issues.html)
        if request.content_type and 'application/json' in request.content_type:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        data['reporter'] = current_user.nickname # for common use, place it out of if statement

        if not data or not data.get('issue_title'):
            flash('Title required')
            return redirect(url_for('issue.issue_list_page'))

        issue_id = service.create_issue(data)
        flash('Issue has been created')
        return redirect(url_for('issue.get_issue', issue_id = issue_id)) # redirect to created issue page
    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('issue.issue_list_page'))


@issue_bp.route('/list', methods = ['GET'])
@login_required
def issue_list_page():
    """For HTML Issue List Page Render"""
    issues = service.get_all_issues()
    return render_template('issues.html', issues = issues)


@issue_bp.route('/<int:issue_id>', methods = ['GET']) # connect and get from api/issues
def get_issue(issue_id: int):
    """search specific issue by id"""
    issue = service.get_issue_by_id(issue_id)
    if not issue:
        return jsonify({'Error' : 'Issue cannot be found'}), 404 # not found
    return render_template('issue_detail.html', issue = issue)


# update issue
@issue_bp.route('/<int:issue_id>/status', methods = ['POST'])
def update_issue_status(issue_id: int):
    """update issue status"""
    data = request.form
    status = data.get('status')
    if not status:
        flash('Status Required')
        return redirect(url_for('issue.get_issue', issue_id = issue_id))

    if service.update_issue_status(issue_id, status):
        flash(f'Status has been changed to {status}')

    return redirect(url_for('issue.get_issue', issue_id = issue_id))


@issue_bp.route('/<int:issue_id>/edit', methods = ['GET'])
@login_required
def edit_issue_page(issue_id:int):
    """Render page for editing issue"""
    issue = service.get_issue_by_id(issue_id)
    if not issue:
        flash('Issue cannot be found')
        return redirect(url_for('issue.issue_list_page'))
    projects = project_service.get_all_projects()
    return render_template('edit_issue.html', issue = issue, projects = projects)


@issue_bp.route('/<int:issue_id>/edit', methods = ['POST'])
@login_required
def update_issue(issue_id:int):
    """Update Issue"""
    data = request.form.to_dict()
    if not data.get('issue_title'):
        flash('Title is required')
        return redirect(url_for('issue.edit_issue_page', issue_id = issue_id))

    if service.update_issue(issue_id, data):
        flash('Issue has been updated')
    else:
        flash('Failed to update issue')
    return redirect(url_for('issue.get_issue', issue_id = issue_id))


@issue_bp.route('/search', methods = ['GET'])
def search_issue():
    """search issues by keyword"""
    keyword = request.args.get('q', '')
    if not keyword:
        return redirect(url_for('issue.issue_list_page'))

    results = service.search_issue(keyword)
    return render_template('issues.html', issues = results)


@issue_bp.route('/<int:issue_id>', methods = ['POST']) #connect and delete from api/issues
def delete_issue(issue_id: int):
    """delete issue"""
    if service.delete_issue(issue_id):
        flash('Issue has been deleted')
    else:
        flash('Issue cannot be found') # it only works in detail page, you will never see this but just in case.
    return redirect(url_for('issue.issue_list_page'))





