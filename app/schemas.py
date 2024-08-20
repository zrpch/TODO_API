from enum import Enum
from typing import Optional

from pydantic import BaseModel


# Task Status Enum
class TaskStatus(str, Enum):
    new = "New"
    in_progress = "In Progress"
    completed = "Completed"


# User Models
class UserBase(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str


# Task Models
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
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
