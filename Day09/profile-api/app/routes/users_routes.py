from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from ..models import users_model
from ..models import profile_pictures_model
from ..schemas.users_schema import User, UserResponse, UserUpdate
from ..middlewares.auth import AuthMiddleware
from datetime import datetime
from typing import List
import logging
import bcrypt
import pymysql
from uuid import uuid4
import aiofiles
import os
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/profileapi",
    tags=["Users"]
)


class ImageTooLargeError(Exception):
    pass

class FailedToUploadError(Exception):
    pass

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create(user_request: User, db: Session = Depends(get_db)):

    userExists = db.query(users_model.User).filter(user_request.email == users_model.User.email).first()

    if userExists:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "email already exists"
            )
    
    salts = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(user_request.password.encode('utf-8'), salts)
    
    new_user = users_model.User(
        **user_request.dict(exclude={"password", "confirm_password"}),
        password=hashed_password.decode(),
    )

    try:  
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except pymysql.DataError as e:
        raiseError(e)
    except Exception as e:
        raiseError(e)


def raiseError(e):
    logger.error(f"failed to create record error: {e}")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail = {
            "status": "error",
            "message": f"failed to create user: {e}",
            "timestamp": f"{datetime.utcnow()}"
        }
    )


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_current_user(current_user = Depends(AuthMiddleware), db: Session = Depends(get_db)):
    return current_user


@router.post("/upload_image")    
async def upload_image(image: UploadFile =  File(...), current_user = Depends(AuthMiddleware), db: Session = Depends(get_db)):


   
    allowed_extns = ["png", "jpeg", "jpg"]

    file_extn = image.filename.split(".")[-1].lower()
    if not file_extn in allowed_extns:
        raiseError("Invalid file extension", status.HTTP_400_BAD_REQUEST)

    try:
        file_name = f"{uuid4()}.{file_extn}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        async with aiofiles.open(file_path, "wb") as output_file:
            content = await image.read()
            file_size = len(content)
            if file_size > 5000000:
                raise ImageTooLargeError()
            await output_file.write(content)
    
    except ImageTooLargeError:
        return {
            "message": "File size must not be greater than 5MB"
        }
        
    except Exception as e:
        raiseError("Internal Server Error", status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    if db.query(profile_pictures_model.Image).filter(profile_pictures_model.Image.user_id == current_user.id).first():
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User image already exist, try updating"
        )

    try:
        image_url = f"static/uploads/{file_name}"
        if image_url:

            new_image = profile_pictures_model.Image(
                image_url =  image_url,
                user_id = current_user.id
                )
        
            db.add(new_image)
            db.commit()
            db.refresh(new_image)

            return {
                "message": "Upload successful",
                "id": current_user.id,
                "name": current_user.name,
                "email": current_user.email,
                "image_url": new_image.image_url
                }
        else:
            raise FailedToUploadError()

    except FailedToUploadError:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Could not upload image!"
        )


@router.put("/update_image")    
async def update_image(image: UploadFile =  File(...), current_user = Depends(AuthMiddleware), db: Session = Depends(get_db)):
   
    allowed_extns = ["png", "jpeg", "jpg"]

    file_extn = image.filename.split(".")[-1].lower()
    if not file_extn in allowed_extns:
        raiseError("Invalid file extension", status.HTTP_400_BAD_REQUEST)

    try:
        file_name = f"{uuid4()}.{file_extn}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        async with aiofiles.open(file_path, "wb") as output_file:
            content = await image.read()
            file_size = len(content)
            if file_size > 5000000:
                raise ImageTooLargeError()
            await output_file.write(content)
    
    except ImageTooLargeError:
        return {
            "message": "File size must not be greater than 5MB"
        }
        
    except Exception as e:
        raiseError("Internal Server Error", status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    new_image = db.query(profile_pictures_model.Image).filter(profile_pictures_model.Image.user_id == current_user.id).first()
    if new_image:

        try:
            image_url = f"static/uploads/{file_name}"
            if image_url:

                new_image.image_url = image_url
        
                db.add(new_image)
                db.commit()
                db.refresh(new_image)

                return {
                    "success": True,
                    "message": "Image update successful",
                    "id": current_user.id,
                    "name": current_user.name,
                    "email": current_user.email,
                    "image_url": new_image.image_url
                    }
            else:
                raise FailedToUploadError()

        except FailedToUploadError:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Could not upload image!"
            )


@router.put("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def update_user(user_request: UserUpdate, current_user = Depends(AuthMiddleware), db: Session = Depends(get_db)):

    userExists = db.query(users_model.User).filter(current_user.id == users_model.User.id).first()

    if userExists:
        userExists.name = user_request.name

    try:  
        db.add(userExists)
        db.commit()
        db.refresh(userExists)

        return userExists
    except pymysql.DataError as e:
        raiseError(e)
    except Exception as e:
        raiseError(e)