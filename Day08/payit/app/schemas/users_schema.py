from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    name: str
    phone: str
    email: str
    password: str
    gender: str
    category: str
    location: str

class UserResponse(User):
    created_at: datetime
    updated_at: datetime