import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from config import Config

@dataclass()
class Issue:
    id: Optional[int] = None # id will be automatically increased
    project: str = ""
    issue_title: str = ""
    issue_description: str = ""
    priority: str = ""
    fatality: str = ""
    version: str = ""
    issue_status: str = "open"
    reporter: str = ""
    assignee: str = ""
    log_date: Optional[datetime] = None # date will be automatically logged
    update_date: Optional[datetime] = None # same above


@dataclass()
class Project:
    id: Optional[int] = None # DB will automatically log
    name: str = ""
    description: str = ""
    created_at: Optional[datetime] = None # DB will automatically log


class DatabaseManager:
    def __init__(self, config: Config): # from config.py, load Config class
        self.config = config
        self.connection = None

    # connect to DB
    def get_connection(self):
        """Make connection with DB"""
        try:
            self.connection = mysql.connector.connect(
                host = self.config.MYSQL_HOST,
                user = self.config.MYSQL_USER,
                password = self.config.MYSQL_PASSWORD,
                database = self.config.MYSQL_DATABASE
            )
            return self.connection
            # if config info above is right, will get connection with db
        except Error as e:
            raise Exception(f"Fail to Connect to Database: {e}")
        # if user cannot reach to db, show the reason

    # execute query to DB
    def execute_query(self, query: str, params: tuple = None, fetch: bool = False):
        """SQL query execution method"""
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor() # cursor make sql run + return result
            cursor.execute(query, params or ())

            if fetch:
                # fetch will decide if it will bring the result of SELECT or ETC
                # or only the counts of 'effected row' or 'lastrowid'
                # fetch=true will call fetchall, fetch=false will call rowcount or 'lastrowid'
                return cursor.fetchall() # it will return the list of tuple
            else:
                conn.commit()
                # INSERT = lastrowid, else rowcount
                if query.strip().upper().startswith("INSERT"):
                    return cursor.lastrowid
                else:
                    return cursor.rowcount
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
