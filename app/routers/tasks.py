from typing import List

from fastapi import APIRouter

from app import schemas

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


# Create a new task
@router.post("/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate):
    return {"message": "Create a new task"}


# Get a list of all tasks
@router.get("/", response_model=List[schemas.TaskResponse])
def read_tasks(skip: int = 0, limit: int = 10):
    return {"message": "Get a list of all tasks"}


# Get tasks for a specific user
@router.get("/user/{user_id}/", response_model=List[schemas.TaskResponse])
def read_user_tasks(user_id: int, skip: int = 0, limit: int = 10):
    return {"message": "Get tasks for a specific user"}


# Get details of a specific task
@router.get("/{task_id}/", response_model=schemas.TaskResponse)
def read_task(task_id: int):
    return {"message": "Get details of a specific task"}


# Update a specific task (task owner only)
@router.put("/{task_id}/", response_model=schemas.TaskResponse)
def update_task(task_id: int, task: schemas.TaskUpdate):
    return {"message": "Update a specific task"}


# Delete a specific task (task owner only)
@router.delete("/{task_id}/")
def delete_task(task_id: int):
    return {"message": "Delete a specific task"}


# Mark a task as completed (task owner only)
@router.patch("/{task_id}/complete/", response_model=schemas.TaskResponse)
def complete_task(task_id: int):
    return {"message": "Mark a task as completed"}


# Filter tasks by status
@router.get("/status/{status}/", response_model=List[schemas.TaskResponse])
def filter_tasks_by_status(status: schemas.TaskStatus, skip: int = 0, limit: int = 10):
    return {"message": "Filter tasks by status"}
