from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# Task Status Enum
class TaskStatus(str, Enum):
    new = "New"
    in_progress = "In Progress"
    completed = "Completed"


# User Models
class UserBase(BaseModel):
    username: str = Field(..., max_length=150, min_length=1)
    first_name: str = Field(..., max_length=50)
    last_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str = Field(..., max_length=150, min_length=1)
    password: str = Field(..., min_length=6)


# Task Models
class TaskBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    status: TaskStatus


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# JWT Token Model
class Token(BaseModel):
    access_token: str
    token_type: str
