from models.database import DatabaseManager
from typing import List, Optional
from config import Config
from models.users import UserInfo
from werkzeug.security import generate_password_hash


class UserService:
    def __init__(self, config: Config):
        self.db_manager = DatabaseManager(config)

    def create_user(self, user_data: dict) -> int:
        """Create user and return user id as int type."""
        username = user_data.get('username')
        nickname = user_data.get('nickname')
        plain_password = user_data.get('password') # get plain text and deliver it to controller
        if not username or not plain_password or not nickname:
            raise ValueError("Need to fill every information")

        password_hash = generate_password_hash(plain_password) # for security, need to hashing the password

        user = UserInfo( # create dataclass, same as Issue Service
            username = username,
            nickname = nickname,
            password_hash = password_hash # hashed value
        )

        sql = """
        INSERT INTO users (username, nickname, password_hash)
        VALUES (%s, %s, %s) 
        """

        params = (
            user.username, user.nickname, user.password_hash
        )
        return self.db_manager.execute_query(sql, params) # will return user id
        # sql, params are set for sql query grammar


def get_user_by_id(self, user_id: int) -> Optional[dict]:
    """SELECT user by id"""
    sql = """
    SELECT id, username
    FROM users
    WHERE id = %s
    """
    results = self.db_manager.execute_query(sql, (user_id,), fetch=True)
    return self.row_to_dict(results[0]) if results else None
    # this def will have only one tuple as result

def get_user_by_username(self, username: str) -> Optional[dict]:
    """SELECT user by username"""
    sql = """
    SELECT id, username
    FROM users
    WHERE username = %s
    """
    results = self.db_manager.execute_query(sql, (username,), fetch=True)
    return self.row_to_dict(results[0]) if results else None
    # this def will have only one tuple as result

def delete_user_by_id(self, user_id: int) -> Optional[dict]:
    """DELETE user by id"""
    sql = """
    DELETE id, username, nickname, password_hash
    FROM users
    WHERE id = %s
    """
    results = self.db_manager.execute_query(sql, (user_id,), fetch=True)
    return self.row_to_dict(results[0]) if results else None
    # this def will have only one tuple as result