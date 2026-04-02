from models.database import DatabaseManager, Project
from typing import List, Optional
from config import Config

class ProjectService:
    def __init__(self,config: Config):
        self.db_manager = DatabaseManager(config)


    def row_to_dict(self, row: tuple) -> dict:
        return{
            'id': row[0], 'name': row[1], 'description': row[2], 'created_at': row[3]
        }


    def create_project(self, name:str, description:str) -> int:
        sql = """
        INSERT INTO projects (name, description)
        VALUES (%s, %s)
        """
        return self.db_manager.execute_query(sql, (name, description))


    def get_all_projects(self) -> List[dict]:
        sql = """
        SELECT id, name, description, created_at
        FROM projects
        ORDER by name
        """
        results = self.db_manager.execute_query(sql, fetch = True)
        return [self.row_to_dict(row) for row in results] if results else []


    def get_project_by_id(self, project_id: int) -> Optional[dict]:
        sql = """
        SELECT id, name, description, created_at
        FROM projects
        WHERE id = %s
        """
        results = self.db_manager.execute_query(sql, (project_id,), fetch =True)
        return self.row_to_dict(results[0]) if results else None


    def update_project(self, project_id:int, name:str, description:str) -> bool:
        # update = True, no update = False, so make it easy to check if it is updated or not
        sql = """
        UPDATE projects
        SET name = %s, description = %s
        WHERE id = %s
        """
        result = self.db_manager.execute_query(sql, (name, description, project_id))
        return result > 0


    def delete_project(self, project_id:int) -> bool:
        sql = """
        DELETE FROM projects
        WHERE id = %s
        """
        result = self.db_manager.execute_query(sql, (project_id,))
        return result > 0