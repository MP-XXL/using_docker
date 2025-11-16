from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    username: str
    email: str


class UserResponse(User):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None


class UserUpdateResponse(UserUpdate):
    updated_at: datetime

    class Config:
        from_attributes = True


class Todo(BaseModel):
    title: str
    user_id: int
    

class TodoResponse(Todo):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    

class TodoUpdate(BaseModel):
    title:str

class TodoUpdateResponse(TodoUpdate):
    updated_at: datetime

    class Config:
        from_attributes = True