from models.database import DatabaseManager, Issue  # Connect with MySQL, execute query, Issue object
from typing import List, Optional  # Optional = select type or none / List = for dictionary list
from config import Config  # for bring config


class IssueService:
    def __init__(self, config: Config):
        self.db_manager = DatabaseManager(config)

    def create_issue(self, issue_data: dict) -> int:
        """Create issue and return issue id as int type."""
        issue = Issue(
            project=issue_data.get('project', ''),
            issue_title=issue_data['issue_title'],
            issue_description=issue_data.get('issue_description', ''),
            priority=issue_data.get('priority', ''),
            fatality=issue_data.get('fatality', ''),
            version=issue_data.get('version', ''),
            # issue_status='open', # no need
            reporter=issue_data.get('reporter', 'anonymous')
        )
        sql = """
        INSERT INTO issue_list (project, issue_title, issue_description, priority, fatality, version, issue_status, reporter)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        params = (
            issue.project, issue.issue_title, issue.issue_description, issue.priority,
            issue.fatality, issue.version, issue.issue_status, issue.reporter
        )
        return self.db_manager.execute_query(sql, params)
        # sql, params are set for sql query


    # Show 'Every' issues by list
    def get_all_issues(self) -> List[dict]:
        """get issues as list and show it"""
        """sorted by priority"""
        sql = """
        SELECT id, project, issue_title, issue_description, priority, fatality, version, issue_status, log_date, update_date, reporter
        FROM issue_list
        ORDER BY FIELD(priority, 'high', 'medium', 'low'), id
        """
        # sorted by priority first then sorted by id
        results = self.db_manager.execute_query(sql, fetch=True)
        return [self.row_to_dict(row) for row in results]
        # it will run 'for' in results and show the full list


    # Pick one issue by id number
    def get_issue_by_id(self, issue_id: int) -> Optional[dict]:
        """SELECT issue by id"""
        sql = """
        SELECT id, project, issue_title, issue_description, priority, fatality, version, issue_status, log_date, update_date, reporter
        FROM issue_list
        WHERE id = %s
        """
        results = self.db_manager.execute_query(sql, (issue_id,), fetch=True)
        return self.row_to_dict(results[0]) if results else None
        # this def will have only one tuple as result


    # Update status of issue
    def update_issue_status(self, status: str, issue_id: int) -> bool:  # bool means it will return true or false
        sql = """
        UPDATE issue_list
        SET issue_status = %s, update_date = NOW()
        WHERE id = %s
        """
        result = self.db_manager.execute_query(sql, (status, issue_id))
        # it will check status first then id, so need to put status first in result
        return result > 0


    # Delete Issue
    def delete_issue(self, issue_id: int) -> bool:
        """Delete issue by issue id"""
        sql = """
        DELETE FROM issue_list
        WHERE id = %s
        """
        # need caution. use delete very carefully.
        result = self.db_manager.execute_query(sql, (issue_id))
        # it will check status first then id, so need to put status first in result
        return result > 0


    def search_issue(self, keyword: str) -> List[dict]:
        """search issue by keyword
        can be more than result
        """
        sql = """
        SELECT id, project, issue_title, issue_description, priority, fatality, version, issue_status, log_date, update_date, reporter
        FROM issue_list
        WHERE issue_title LIKE %s OR issue_description LIKE %s OR priority LIKE %s or fatality LIKE %s or issue_status LIKE %s OR reporter LIKE %s
        """
        params = (f"%(keyword)%",) * 6  # 6 cases above, check 6 times
        results = self.db_manager.execute_query(sql, params, fetch=True)
        return [self.row_to_dict(row) for row in results]
        # same as for row in results


    def row_to_dict(self, row: tuple) -> dict: # This works differently with row_to_dict in user_service.py
        """change row to tuple"""
        return {
            'id': row[0], 'project': row[1], 'issue_title': row[2],
            'issue_description': row[3], 'priority': row[4], 'fatality': row[5],
            'version': row[6], 'issue_status': row[7], 'log_date': row[8],
            'update_date': row[9], 'reporter': row[10]
        }

