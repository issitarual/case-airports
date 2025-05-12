from fastapi import APIRouter
from services.user import UserService

router = APIRouter()
user_service = UserService()

@router.post("/")
async def insert(data: dict):
    return user_service.insert_user(data)

@router.get("/{name}")
async def get(name: str):
    return user_service.get_user(name)

@router.get("/")
async def list_users():
    return user_service.list_users()
