from models.database import DatabaseManager
from typing import List, Optional
from config import Config
from models.users import UserInfo
from werkzeug.security import generate_password_hash


class UserService:
    def __init__(self, config: Config):
        self.db_manager = DatabaseManager(config)


    def row_to_dict(self, row: tuple, columns: list) -> dict:
        # This works differently with row_to_dict in issue_service.py
        """Convert tuple row to dic with use column names"""
        return dict(zip(columns, row))


    def create_user(self, user_data: dict) -> int:
        """Create user and return user id as int type."""
        username = user_data.get('username')
        nickname = user_data.get('nickname')
        email = user_data.get('email')
        plain_password = user_data.get('password') # get plain text and deliver it to controller
        if not username or not plain_password or not nickname:
            raise ValueError("Need to fill every information")

        password_hash = generate_password_hash(plain_password) # for security, need to hashing the password

        user = UserInfo( # create dataclass, same as Issue Service, bring it from users.py
            username = username,
            nickname = nickname,
            email = email,
            password_hash = password_hash # hashed value
        )

        sql = """
        INSERT INTO users (username, nickname, email, password_hash)
        VALUES (%s, %s, %s, %s) 
        """

        params = ( # bring data from user above. instance created by UserInfo class.
            user.username, user.nickname, user.email, user.password_hash
        )
        return self.db_manager.execute_query(sql, params) # will return user id
        # sql, params are set for sql query grammar


    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        """SELECT user by id"""
        sql = """
        SELECT id, username, nickname, email
        FROM users
        WHERE id = %s AND is_deleted = FALSE
        """
        results = self.db_manager.execute_query(sql, (user_id,), fetch=True)
        if not results:
            return None
        row = results[0]
        return UserInfo(id = row[0], username = row[1], nickname = row[2], email = row[3]) if results else None
        # this def will have only one tuple as result


    def get_user_by_email(self, email: str) -> Optional[dict]:
        """SELECT user by username"""
        sql = """
        SELECT id, username, nickname, email
        FROM users
        WHERE username = %s AND is_deleted = FALSE
        """
        results = self.db_manager.execute_query(sql, (email,), fetch=True)
        if not results:
            return None
        columns = ['id', 'username', 'nickname', 'email']
        return self.row_to_dict(results[0], columns) if results else None
        # this def will have only one tuple as result


    def get_user_with_password(self, email: str) -> Optional[dict]:
        """Select user with password for login"""
        sql = """
        SELECT id, username, nickname, email, password_hash
        FROM users
        WHERE email = %s AND is_deleted = FALSE
        """
        results = self.db_manager.execute_query(sql, (email,), fetch=True)
        if not results:
            return None # Add defense code
        columns = ['id', 'username', 'nickname', 'email', 'password_hash']
        return self.row_to_dict(results[0], columns)


    def get_user_with_password_by_id(self, user_id: int) -> Optional[dict]:
        """Select user with password and id for change password / delete account"""
        sql = """
        SELECT id, username, nickname, email, password_hash
        FROM users
        WHERE id = %s AND is_deleted = FALSE
        """
        result = self.db_manager.execute_query(sql, (user_id,), fetch = True)
        if not result:
            return None
        columns = ['id', 'username', 'nickname', 'email', 'password_hash']
        return self.row_to_dict(result[0], columns)


    def update_nickname(self, user_id: int, new_nickname: str) -> bool:
        """Update user nickname"""
        sql = """
        UPDATE users
        SET nickname = %s
        WHERE id = %s AND is_deleted = FALSE
        """
        result = self.db_manager.execute_query(sql, (new_nickname, user_id))
        return result > 0


    def update_password(self, user_id: int, new_password: str) -> bool:
        """Update Password"""
        new_hash = generate_password_hash(new_password) # new_password will be hashed.
        sql = """
        UPDATE users
        SET password_hash = %s
        WHERE id = %s AND is_deleted = FALSE
        """
        result = self.db_manager.execute_query(sql, (new_hash, user_id))
        return result > 0


    def deactivate_user(self, user_id: int) -> bool:
        """Soft Delete of user account"""
        sql = """
        UPDATE users
        SET username = '', password_hash = '', is_deleted = TRUE, deleted_time = NOW()
        WHERE id = %s AND is_deleted = FALSE
        """
        result = self.db_manager.execute_query(sql, (user_id,))
        return result > 0