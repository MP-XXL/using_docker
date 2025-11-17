from sqlalchemy.orm import Session
from database.database import get_db
from database_models.data_models import User, UserResponse
from database_models import db_model
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from typing import List

router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create_user(user: User, db: Session = Depends(get_db)):
    if db.query(db_model.User).filter(db_model.User.email == user.email).first():
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User already exists!"
        )
    if db.query(db_model.User).filter(db_model.User.username == user.username).first():
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Username already taken! Try another"
        )
    new_user = db_model.User(
        **user.model_dump(),
        created_at = datetime.now(),
        updated_at = datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(db_model.User).filter(db_model.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found!"
        )
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    updated_user = db.query(db_model.User).filter(db_model.User.id == user_id).first()
    if not updated_user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found!"
        )
    for field, value in user.dict().items():
        setattr(updated_user, field, value)
    db.commit()
    db.refresh(updated_user)
    return updated_user

@router.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(db_model.User).filter(db_model.User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found!"
        )
    db.delete(db_user)
    db.commit()
    raise HTTPException(
        status_code = status.HTTP_204_NO_CONTENT,
        detail = "Deleted user"
    )

@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(db_model.User).all()
 
