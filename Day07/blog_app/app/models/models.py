from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(User):
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None

class UserUpdateResponse(UserUpdate):
    updated_at: datetime


class Post(BaseModel):
    title: str
    user_id: int
    

class PostResponse(Post):
    created_at: datetime
    updated_at: datetime

class PostUpdate(BaseModel):
    title:str

class PostUpdateResponse(PostUpdate):
    updated_at: datetime