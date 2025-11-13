from fastapi import FastAPI, status, HTTPException, APIRouter
from ..models.models import Todo, TodoResponse, TodoUpdate, TodoUpdateResponse
from ..database.database import db
from ..raw_sql import queries
from datetime import datetime

router = APIRouter()



@router.post("/todos")
def create_todo(todo: Todo):
    new_todo = TodoResponse(
        **todo.model_dump(),
        created_at = datetime.now(),
        updated_at = datetime.now()
    )
    # CREATE_TODO = """
    # INSERT INTO users(title, user_id) VALUES(%s, %s); ############# ALTERNATIVE METHOD
    # """
    with db.get_cursor() as cursor:
        cursor.execute(queries.CREATE_TODO, (todo.title, todo.user_id))
    
    return {
        "success": True,
        "data": new_todo,
        "message": "New todo added successfully!"
    }

@router.patch("/todos/{user_id}")
def update_todo(user_id: int, todo: TodoUpdate):
    if not user_id:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail = "Bad user input"
        )
    with db.get_cursor() as cursor:
        cursor.execute(queries.UPDATE_TODO, (todo.title, user_id))
    updated_todo = TodoUpdateResponse(
        **todo.model_dump(),
        updated_at = datetime.now()
    )
    return {
        "sucess": True,
        "data": updated_todo,
        "message": "Todo updated successfully"
    }