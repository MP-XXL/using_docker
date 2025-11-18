from sqlalchemy.orm import Session
from database.database import get_db
from database_models.data_models import Todo, TodoResponse, User
from database_models import db_model
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from typing import List

router = APIRouter()


@router.post("/todos", response_model=TodoResponse)
def create_todo(todo: Todo, db: Session = Depends(get_db)):
    new_todo = db.query(db_model.User).filter(db_model.User.id == todo.user_id).first()
    if not new_todo:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User does not exists!"
        )

    new_todo = db_model.Todo(
        **todo.model_dump(),
        created_at = datetime.now(),
        updated_at = datetime.now()
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo
    
@router.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(db_model.Todo).filter(db_model.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Todo not found!"
        )
    return todo

@router.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: Todo, db: Session = Depends(get_db)):
    updated_todo = db.query(db_model.Todo).filter(db_model.Todo.id == todo_id).first()
    if not updated_todo:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Todo not found!"
        )
    for field, value in todo.dict().items():
        setattr(updated_todo, field, value)
    db.commit()
    db.refresh(updated_todo)
    return updated_todo

@router.delete("/todos/{todo_id}", response_model=TodoResponse)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(db_model.Todo).filter(db_model.Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Todo not found!"
        )
    db.delete(db_todo)
    db.commit()
    raise HTTPException(
        status_code = status.HTTP_204_NO_CONTENT,
        detail = "Deleted todo"
    )

@router.get("/todos", response_model=List[TodoResponse])
def get_all_todos(db: Session = Depends(get_db)):
    return db.query(db_model.Todo).all()
 
