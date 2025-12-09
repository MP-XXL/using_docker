from pydantic import BaseModel, Field, EmailStr, validator, model_validator
from fastapi import HTTPException, status
from datetime import datetime
from enums import Gender, Category
import re
from typing import List, Optional, Dict

class User(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    phone: str = Field(min_length=11, pattern=r"\d")
    email: EmailStr
    password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)
    gender: Gender
    location: str = Field(min_length=1)

    @validator('phone')
    def phone_is_valid_numeric_value(cls, value):
        if value.isdigit() is not True:
            raise ValueError('phone number must be digits')
        return value
    
    @validator('password')
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError('password must contain atleast one capital letter')
        if not re.search(r"[a-z]", value):
            raise ValueError('password must contain atleast one lowercase letter')
        if not re.search(r"\d", value):
            raise ValueError('password must contain atleast one numeric value')
        if not re.search(r"[^A-Za-z0-9]", value):
            raise ValueError('password must contain atleast one special character')
        return value
    
    @model_validator(mode='after')
    def validate_confirm_password(self):
        if self.password != self.confirm_password:
            raise ValueError('passwords must match')
        return self

    @validator('name')
    def check_for_numbers(cls, value):
        if any(char.isdigit() for char in value):
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = 'Name can not contain numbers'
                )
        return value
    
    @validator('name')
    def validate_name(cls, value):
        if value.isspace() is True:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = 'Name can not be blank!'
                )
        return value

    


# @field_validator('phone')
# @classmethod
# def check_if_digit(cls, data: str)-> str:
#     if data.isdigit == True:
#         return data
#     else:
#         return {
#             "message": "Phone must be alphanumeric!"
#         }

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None
    gender: Optional[Gender] = None
    location: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    gender: str
    location: str
