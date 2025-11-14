from fastapi import FastAPI, status, HTTPException, APIRouter
from ..models.models import User, UserResponse, UserUpdate,UserUpdateResponse
from datetime import datetime
from ..database.database import db
from ..raw_sql import queries

router = APIRouter()

class InvalidInputError(Exception):
    pass


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
        created_at = datetime.now(),
        updated_at = datetime.now()
    )
    # CREATE_USER = """
    # INSERT INTO users(username, email, password) VALUES(%s, %s, %s); ############# ALTERNATIVE METHOD
    # """
    with db.get_cursor() as cursor:
        cursor.execute(queries.CREATE_USER, (user.username, user.email, user.password))
    
    return {
        "success": True,
        "data": new_user,
        "message": "New user created sucessfully"
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
    if user.username == None:
        pass
    if user.email == None:
        pass
    if user.password == None:
        pass
    with db.get_cursor() as cursor:
        cursor.execute(queries.UPDATE_USER, (user.username, user.email, user.password, user_id))
    updated_user = UserUpdateResponse(
        **user.model_dump(),
        updated_at = datetime.now()
    )

    return {
            "success": True,
            "Data": updated_user,
            "message": "User details updated successfully"
        }

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    try:
        if not user_id:
            raise InvalidInputError()
        else:
             with db.get_cursor() as cursor:
                cursor.execute(queries.DELETE_USER, (user_id))
        raise HTTPException(
                    status_code = status.HTTP_204_NO_CONTENT,
                    detail = "Deleted sucessfully!"
                )
    except InvalidInputError:
        raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail = "User entered an invalid input"
            )
    except Exception:
        return {
            "message": "Ops! something went wrong!"
        }

@router.get("/users")
def get_all_users():
    with db.get_cursor() as cursor:
                cursor.execute(queries.GET_ALL_USERS)
                data = cursor.fetchall()

    return {
        "data":data
    }