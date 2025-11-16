from sqlalchemy.orm import Session
from database.database import get_db
from database_models.data_models import User, UserResponse
from database_models import db_model
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime

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
    
    
