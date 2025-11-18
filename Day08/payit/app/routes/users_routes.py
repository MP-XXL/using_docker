from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import APIRouter, HTTPException, status, Depends
from ..models import db_models
from ..schemas.users_schema import User, UserResponse
from datetime import datetime
from typing import List



router = APIRouter()



@router.post("/users")
def create_user(user: User, db: Session = Depends(get_db)):
    if db.query(db_models.User).filter(db_models.User.email == user.email).first():
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User email already exists!"
        )

    new_user = db_models.User(
        **user.model_dump()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return(new_user)

@router.get("/users/{user_id}")
def get_a_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User with ID not found"
        )

    return user

@router.put("/users/{user_id}")
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    updated_user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
    if not update_user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User with ID not found"
        )

    for field, value in user.dict().items():
        setattr(updated_user, field, value)

    db.commit()
    db.refresh(updated_user)
    return updated_user