from fastapi import FastAPI, status, HTTPException, APIRouter
from ..models.models import User, UserResponse
from datetime import datetime
from ..database.database import db
from ..raw_sql import queries

router = APIRouter()


# @router.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/")
def home():
    return {
        "success": True,
        "message": "Welcome to todo hompage!"
    }

@router.post("/users")
def creat_user(user: User):
    new_user = UserResponse(
        **user.model_dump(),
        #id = UserResponse.id,
        created_at = datetime.now(),
        updated_at = datetime.now()
    )
    with db.get_cursor() as cursor:
        cursor.execute(queries.CREATE_USER)
    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)

    return {
        "data": new_user
    }