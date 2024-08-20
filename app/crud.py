from sqlalchemy.orm import Session

from . import models, schemas
from .security import get_password_hash


# Create user
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Get user by ID
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# Get user by username
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# Get all users
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()


# Create task
def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# Get task by ID
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


# Get all tasks
def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Task).offset(skip).limit(limit).all()


# Get tasks by user ID
def get_user_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Task)
        .filter(models.Task.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# Update task
def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = get_task(db, task_id=task_id)
    if db_task:
        for var, value in vars(task).items():
            setattr(db_task, var, value) if value else None
        db.commit()
        db.refresh(db_task)
    return db_task


# Delete task
def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id=task_id)
    if db_task:
        db.delete(db_task)
        db.commit()


# Mark task as completed
def mark_task_as_completed(db: Session, task_id: int):
    db_task = get_task(db, task_id=task_id)
    if db_task:
        db_task.status = schemas.TaskStatus.completed
        db.commit()
        db.refresh(db_task)
    return db_task


# Filter tasks by status
def filter_tasks_by_status(
    db: Session,
    status: schemas.TaskStatus,
    user_id: int = None,
    skip: int = 0,
    limit: int = 10,
):
    query = (
        db.query(models.Task)
        .filter(models.Task.status == status)
        .offset(skip)
        .limit(limit)
    )
    if user_id:
        query = query.filter(models.Task.user_id == user_id)
    return query.all()
