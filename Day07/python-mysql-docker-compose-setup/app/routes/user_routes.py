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
    # CREATE_USER = """
    # INSERT INTO users(username, email, password) VALUES(%s, %s, %s); ############# ALTERNATIVE METHOD
    # """
    with db.get_cursor() as cursor:
        cursor.execute(queries.CREATE_USER, (user.username, user.email, user.password))
    
    return {
        "data": new_user
    }

@router.patch("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    try:
        if not user_id:
            raise Exception
        else:
            pass
    except Exception as e:
        raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail = "User entered an invalid input"
            )
    with db.get_cursor() as cursor:
        cursor.execute(queries.UPDATE_USER, ())