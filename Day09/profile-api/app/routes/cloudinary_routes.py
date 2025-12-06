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
import pymysql
#from uuid import uuid4
import aiofiles
import os
#from fastapi.staticfiles import StaticFiles
import cloudinary
from cloudinary.uploader import upload, destroy
from dotenv import load_dotenv 

load_dotenv()

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/profileapi/cloudinary",
    tags=["Upload"]
)

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
    )
    
class ImageTooLargeError(Exception):
    pass

class InvalidFileExtensionError(Exception):
    pass

class UserExistError(Exception):
    pass


@router.post("/users")
async def handle_upload(image: UploadFile = File(...), current_user=Depends(AuthMiddleware), db:Session=Depends(get_db)):
    if db.query(profile_pictures_model.Image).filter(profile_pictures_model.Image.user_id == current_user.id).first():
            raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User image already exist, try updating"
        )

    try:
        content = image.file.read()
        file_size = len(content)
        if file_size > 5000000:
            raise ImageTooLargeError()
        
        image.file.seek(0)
        result = upload(image.file)
        url = result["secure_url"]
        public_id = result["public_id"]

        new_image = profile_pictures_model.Image(
            image_url = url,
            user_id = current_user.id,
            public_id = public_id
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

    except InvalidFileExtensionError:
        return {
            "message": "File with invalid extension"
        }
    except ImageTooLargeError as e:
        return {
            "message": "File size must not be greater than 5MB"
        }

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"ERROR: Failed to upload image: {e}"
        )


@router.delete("/users")
async def delete_image(current_user = Depends(AuthMiddleware), db: Session = Depends(get_db)):
    url_to_delete = db.query(profile_pictures_model.Image).filter(profile_pictures_model.Image.user_id == current_user.id).first()
    if url_to_delete != None:
        destroy(url_to_delete.public_id)
    
    user_to_delete = db.query(users_model.User).filter(users_model.User.id == current_user.id).first()
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
        raise HTTPException(
        status_code = status.HTTP_204_NO_CONTENT,
        detail = "Deleted successfully"
        )




    

        