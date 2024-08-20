from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, dependencies, models, schemas, security
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# Register a new user
@router.post("/register/", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


# Authenticate and get a JWT token
@router.post("/login/", response_model=schemas.Token)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if not db_user or not security.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = security.create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Authenticate for FastAPI docs
@router.post("/authorize-fastapi-docs/", response_model=schemas.Token)
def authorize_fastapi_docs(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    db_user = crud.get_user_by_username(db, username=form_data.username)
    if not db_user or not security.verify_password(
        form_data.password, db_user.password
    ):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = security.create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Get a list of all users (authenticated users only)
@router.get("/", response_model=list[schemas.UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# Get details of a specific user (authenticated users only)
@router.get("/{user_id}/", response_model=schemas.UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
