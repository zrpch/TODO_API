from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, dependencies, models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


# Create a new task (authenticated users only)
@router.post("/", response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    return crud.create_task(db=db, task=task, user_id=current_user.id)


# Get a list of all tasks (authenticated users only)
@router.get("/", response_model=List[schemas.TaskResponse])
def read_tasks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


# Get tasks for a specific user (authenticated users only)
@router.get("/user/{user_id}/", response_model=List[schemas.TaskResponse])
def read_user_tasks(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    tasks = crud.get_user_tasks(db, user_id=user_id, skip=skip, limit=limit)
    return tasks


# Get details of a specific task (authenticated users only)
@router.get("/{task_id}/", response_model=schemas.TaskResponse)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Update a specific task (task owner only)
@router.put("/{task_id}/", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    updated_task = crud.update_task(db=db, task_id=task_id, task=task)
    return updated_task


# Delete a specific task (task owner only)
@router.delete("/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    crud.delete_task(db=db, task_id=task_id)
    return None


# Mark a task as completed (task owner only)
@router.patch("/{task_id}/complete/", response_model=schemas.TaskResponse)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    completed_task = crud.mark_task_as_completed(db=db, task_id=task_id)
    return completed_task


# Filter tasks by status (authenticated users only)
@router.get("/status/{status}/", response_model=List[schemas.TaskResponse])
def filter_tasks_by_status(
    status: schemas.TaskStatus,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    tasks = crud.filter_tasks_by_status(
        db=db, status=status, user_id=None, skip=skip, limit=limit
    )
    return tasks
