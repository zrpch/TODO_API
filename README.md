# TODO API Application

## Overview

This project is a simple RESTful API for managing a task list (ToDo list) built using FastAPI and SQLAlchemy with PostgreSQL as the database. The API supports user registration, authentication using JWT, and CRUD operations for tasks. The API also allows filtering tasks by status and includes pagination support for the task list.

## Features

- **User Management:**
  - Register a new user.
  - Authenticate and obtain a JWT token.
  - Only authenticated users can access the application features.

- **Task Management:**
  - Create, read, update, and delete tasks.
  - Filter tasks by status.
  - Mark tasks as completed.
  - Tasks can only be updated or deleted by the user who created them.

- **Pagination:**
  - Supports pagination for task lists.

- **Testing:**
  - Comprehensive test coverage using `pytest`.

## Technical Features

- **FastAPI:** Fast and modern web framework for building APIs with Python 3.7+.
- **SQLAlchemy:** ORM for the database models and handling database migrations.
- **PostgreSQL:** As the database backend.
- **Alembic:** For handling database migrations.
- **JWT (JSON Web Tokens):** For user authentication and authorization.
- **Pydantic:** For data validation and settings management.
- **Pytest:** For writing unit and integration tests.
- **Ruff, Black, and Isort:** For code quality, formatting, and imports organization.

## Installation

### Prerequisites

- Python 3.7+
- PostgreSQL

### Clone the Repository

```bash
git clone https://github.com/zrpch/TODO_API.git
cd todo-api
```

### Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Set Up Environment Variables

Create a `.env` file from `.env.example` in the project root and update the following environment variables:

```plaintext
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
SECRET_KEY=your_secret_key
```

### Apply Database Migration

```bash
alembic upgrade head
```

### Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### Run Tests

```bash
pytest
```

## API Endpoints

### User Endpoints

- **POST /users/register/**: Register a new user.
- **POST /users/login/**: Authenticate and get a JWT token.
- **GET /users/**: Get a list of all users (authenticated users only).
- **GET /users/{user_id}/**: Get details of a specific user (authenticated users only).

### Task Endpoints

- **POST /tasks/**: Create a new task (authenticated users only).
- **GET /tasks/**: Get a list of all tasks (authenticated users only).
- **GET /tasks/user/{user_id}/**: Get tasks for a specific user (authenticated users only).
- **GET /tasks/{task_id}/**: Get details of a specific task (authenticated users only).
- **PUT /tasks/{task_id}/**: Update a specific task (task owner only).
- **DELETE /tasks/{task_id}/**: Delete a specific task (task owner only).
- **PATCH /tasks/{task_id}/complete/**: Mark a task as completed (task owner only).
- **GET /tasks/status/{status}/**: Filter tasks by status (authenticated users only).