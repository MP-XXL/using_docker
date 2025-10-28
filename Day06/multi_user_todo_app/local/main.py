from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional

app = FastAPI(title="Multi-user Todo")

class USER_NOT_FOUND_ERROR(HTTPException):
    def __init__(self, status_code=status.HTTP_404_NOT_FOUND, detail="User not found"):
        super().__init__(status_code, detail)
        pass

class User(BaseModel):
    username: str

class UserCreate(User):
    password: str

class UserInDb(UserCreate):
    created_at: datetime
    updated_at: datetime

class UserResponse(User):
    created_at: datetime
    updated_at: datetime

class TaskCreate(BaseModel):
    title: str
    description: str

class TaskInDb(TaskCreate):
    task_id: int
    created_at: datetime
    updated_at: datetime
    is_completed: bool

class Database:
    def __init__(self):
        # two tables
        self._users: Dict[int, UserInDb] = {}
        self._tasks: Dict[int, List[TaskInDb]] = {}
        self.user_id = 1
        self.task_id = 1

    def increment_user_id(self):
        self.user_id += 1

    def add_user(self, user: UserInDb) -> UserInDb | None:
        for _, user_details in self._users.items():
            if user_details.username == user.username:
                return None
        user_id = self.user_id
        self._users[user_id] = user
        self.increment_user_id()
        return user
    
    def get_all_users(self):
        return self._users

    def get_user_by_id(self, user_id: int):
        if user_id not in self._users:
            raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = "User with ID not found"
                    )
        return {
                "success": True,
                "data": self._users[user_id],
                "message": "User retrieved successfully"
                }
    def user_delete(self, user_id):
        if user_id not in self._users:
            raise USER_NOT_FOUND_ERROR()
        del self._users[user_id]
        raise HTTPException(
                status_code = status.HTTP_204_NO_CONTENT,
                detail = "Deleted"
                )




    def increment_task_id(self):
        self.task_id += 1

    def add_task(self, user_id: int, task: TaskInDb):
        self._tasks.setdefault(user_id, []).append(task)

    def all_task(self):
        return self._tasks

    def username_get_task(self, username: str):
        for user, user_details in self._users.items():
            if user_details.username == username:
                return self._tasks[user]
        else:
            raise USER_NOT_FOUND_ERROR()




db_instance = Database()

# 
#END POINTS
#

@app.get("/home")
def todo_home():
    return {
            "message": "Welcome to Multi-user Todo home"
            }

@app.post("/users")
def register_user(user: UserCreate):
    if not user.username or not user.password:
        raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "All fields are required"
                )
    new_user = UserInDb(
            **user.model_dump(),
            created_at = datetime.now(),
            updated_at = datetime.now()
            )
    user = db_instance.add_user(new_user)
    if not user:
        raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "User already exist"
                )
    return {
            "success": True,
            "data": UserResponse(**user.model_dump(exclude_unset=True)),
            "message": "User created successfully"
            }

@app.get("/users")
def get_users():
    users = db_instance.get_all_users()
    if len(users) < 1:
        raise HTTPException(
                status_code = status.HTTP_200_OK,
                detail = "No user has been created"
                )
    return {
            "success": True,
            "data": users,
            "message": "All users retrieved successfully"
            }

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if not user_id:
        raise HTTPEception(
                status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail = "Invalid input")
    return db_instance.get_user_by_id(user_id)

@app.delete("/users")
def delete_user(user_id: int):
    return db_instance.user_delete(user_id)


@app.post("/users/tasks")
def add(task: TaskCreate, user_id: int):
    if user_id not in db_instance._users:
        raise USER_NOT_FOUND_ERROR()


    new_task = TaskInDb(
            **task.model_dump(),
            task_id = db_instance.task_id,
            created_at = datetime.now(),
            updated_at = datetime.now(),
            is_completed = False
            )
    db_instance.increment_task_id()
    task = db_instance.add_task(user_id=user_id, task= new_task)

    return {
            "success": True,
            "data": new_task,
            "message": "Task created successfully"
            }

@app.get("/tasks")
def get_all_tasks():
    return db_instance.all_task()

@app.get("/username")
def get_task_by_username(username: str):
    return db_instance.username_get_task(username)

@app.delete("tasks/users")
def delete_user_task(user_id: int)
