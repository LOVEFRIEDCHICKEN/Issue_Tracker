# Identify dataclass User ( id, username, password )
from dataclasses import dataclass
from typing import Optional
from flask_login import UserMixin


@dataclass()
class UserInfo(UserMixin):
    id: Optional[int] = None # id will be automatically increased
    username: str = ""
    nickname: str = ""
    email: str = ""
    password_hash: str = ""
