import json
import os
from typing import List
from ..models.user import User

class UserDao:
    def __init__(self, file_path: str = "users.json"):
        # 確保文件路徑是相對於當前檔案的
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(current_dir, "..", "..", file_path)
        
    def _read_file(self) -> List[dict]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
            
    def _write_file(self, users: List[dict]):
        # 確保目錄存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
            
    def get_all_users(self) -> List[User]:
        users_data = self._read_file()
        return [User(**user) for user in users_data]
        
    def create_user(self, user: User):
        users_data = self._read_file()
        users_data.append(user.dict())
        self._write_file(users_data)