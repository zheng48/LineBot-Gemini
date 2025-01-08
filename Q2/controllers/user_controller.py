from fastapi import APIRouter
from typing import List
from ..models.user import User
from ..services.user_service import UserService

router = APIRouter()
user_service = UserService()

@router.get("/api/user", response_model=List[User])
async def get_users():
    return user_service.get_all_users()

@router.post("/api/user")
async def create_user(user: User):
    user_service.create_user(user)
    return {"message": "User created successfully"}