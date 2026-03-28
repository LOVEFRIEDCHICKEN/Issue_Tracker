# Identify dataclass User ( id, username, password )
from dataclasses import dataclass
from typing import Optional


@dataclass()
class UserInfo:
    id: Optional[int] = None # id will be automatically increased
    username: str = ""
    nickname: str = ""
    password_hash: str = ""
