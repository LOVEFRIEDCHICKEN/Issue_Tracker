from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from services.issue_service import IssueService
from config import Config
from typing import Dict, Any

issue_bp = Blueprint('issue', __name__, url_prefix='/api/issues') # flask blueprint's route decorator
service = IssueService(Config())

# @issue_be.route is only for issue
@issue_bp.route('/', methods=['POST']) # connect and post to api/issues/
def create_issue():
    """add issue API"""
    try:
        data = request.get_json()
        if not data or data.get('issue_title'):
            return jsonify({'Error': 'Title is requirement'}), 400 # bad request from data

        issue_id = service.create_issue(data)
        return jsonify({'Message': 'Issue has created', 'id': issue_id}), 201 # create success
    except Exception as e:
        return jsonify({'Error': str(e)}), 500 # internal server error, DB connect fail / exception code etc



@issue_bp.route('/', methods = ['GET']) # connect and get from api/issues
def get_issues(): # This will work differently with issue_list_page, better to leave it here.
    # For external tool, it can call json data later.
    """show all issues list API"""
    issues = service.get_all_issues()
    return jsonify(issues)


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
    return jsonify(issue)


# update issue
@issue_bp.route('/<int:issue_id>/status', methods = ['PUT']) # connect and put to api/issues
def update_issue_status(issue_id: int):
    """update issue status API"""
    data = request.get_json()
    status = data.get('status')
    if not status:
        return jsonify({'Error': 'Status is requirement'}), 400

    if service.update_issue_status(issue_id, status):
        return jsonify({'Message': f'Status has changed to {status}'})
    return jsonify({'Error': 'Issue cannot be found'}), 404


@issue_bp.route('/<int:issue_id>', methods = ['DELETE']) #connect and delete from api/issues
def delete_issue(issue_id: int):
    """delete issue"""
    if service.delete_issue(issue_id):
        return jsonify({'Message': 'Issue has been deleted'})
    return jsonify({'Error': 'Issue cannot be found'}), 404


@issue_bp.route('/search', methods = ['GET'])
def search_issue():
    """search issues by keyword"""
    keyword = request.args.get('q', '')
    if not keyword:
        return jsonify({'Error': 'Please enter the keyword'}), 400

    results = service.search_issue(keyword)
    return jsonify(results)


