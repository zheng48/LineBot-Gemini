from typing import List
from ..models.user import User
from ..dao.user_dao import UserDao

class UserService:
    def __init__(self):
        self.user_dao = UserDao()
        
    def get_all_users(self) -> List[User]:
        return self.user_dao.get_all_users()
        
    def create_user(self, user: User):
        self.user_dao.create_user(user)