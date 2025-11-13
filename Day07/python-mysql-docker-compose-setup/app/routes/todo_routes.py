from fastapi import FastAPI, status, HTTPException, APIRouter
from ..models.models import Todo, TodoResponse
from datetime import datetime
from ..database.database import db
from ..raw_sql import queries

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