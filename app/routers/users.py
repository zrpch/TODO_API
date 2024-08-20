from fastapi import APIRouter

from app import schemas

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# Register a new user
@router.post("/register/", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate):
    return {"message": "Register a new user"}


# Authenticate
@router.post("/login/")
def login_user(user: schemas.UserLogin):
    return {"message": "Authenticate"}


# Get a list of all users
@router.get("/", response_model=list[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 10):
    return {"message": "Get a list of all users"}


# Get details of a specific user
@router.get("/{user_id}/", response_model=schemas.UserResponse)
def read_user(user_id: int):
    return {"message": "Get details of a specific user"}
