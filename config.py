import os
from dotenv import load_dotenv
# dotenv for .env file. Read 'KEY=VALUE' and load on 'os.environ'
# and also for security

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'flask_issue_db')

    PERMANENT_SESSION_LIFETIME = 3600  # Keep the login session (seconds)
    SESSION_COOKIE_HTTPONLY = True  # Block JS (Secure from XSS)
    SESSION_COOKIE_SECURE = False  # Production HTTPS True