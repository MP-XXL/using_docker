from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Dict

app = FastAPI(title = "Todo List")


#next_id = 1

class TaskCreate(BaseModel):
    title: str
    description: str

class Task(TaskCreate):
    task_id: int
    created_at: datetime
    updated_at: datetime
    is_completed: bool

class UpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None

class ToggleStatus(BaseModel):
    is_completed: bool


class Database:
    def __init__(self):
        self._tasks = {}

    def add(self, task: Task):
        self._tasks.update({task.task_id: task})

    def show_added(self, task: Task):
        added_task = {task.task_id: task}
        return added_task

    def get_all_tasks(self):
        data = self._tasks
        return data

task_instance = Database()

next_id = 1

def generate_next_id():
    global next_id
    next_id += 1
    return next_id

#Endpoints

@app.get("/")
def index():
    return {
            "message": "Todo App"
            }

@app.get("/tasks")
def all_tasks():
    return {
            "message": "Displaying all tasks",
            "data": task_instance.get_all_tasks()
            }

@app.get("/tasks/{task_id}")
def get_one_task(task_id:int):
    if task_id in task_instance._tasks:
            return {
                    "message": "Task found",
                    "data": task_instance._tasks[task_id]
                    }
    else:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Task with ID not found"
                )

@app.post("/tasks", status_code = status.HTTP_201_CREATED)
def add(task: TaskCreate):
    if not task.title and not task.description:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Invalid inputs")
    global next_id
    new_task = Task(
            task_id = next_id,
            title = task.title,
            description = task.description,
            created_at = datetime.now(),
            updated_at = datetime.now(),
            is_completed = False
            )
    """new_task ={
            "task_id": next_id,
            "title": task.title,
            "description": task.description,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "is_completed": False
            }"""
                

    #generate_next_id()
    task_instance.add(task = new_task)
    pre = new_task
    generate_next_id()
    return {
            "message": "Task created successfully",
            "data": task_instance.show_added(pre)
            }

@app.patch("/tasks/{task_id}", status_code = status.HTTP_201_CREATED)
def update(task_id: int, task: UpdateTask):
    if task_id not in task_instance._tasks:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Task with ID not found"
                )
    else:
        if task.title != None:
            task_instance._tasks[task_id].title = task.title
        if task.description != None:
            task_instance._tasks[task_id].description = task.description
        return {
                "message": "Task update successfully",
                "data": task_instance._tasks[task_id]
                }

@app.put("/tasks/{task_id}", status_code = status.HTTP_201_CREATED)

def toggle(task_id:int, task: ToggleStatus):
    if task_id not in task_instance._tasks:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Task with ID not found"
                )
    else:
        if task.is_completed == True and task_instance._tasks[task_id].is_completed == True:
            return {
                    "message": "Task already completed"
                    }
        if task.is_completed == False and task_instance._tasks[task_id].is_completed == False:
            return {
                    "message": "Task already incomplete"
                    }
        if task.is_completed == True and task_instance._tasks[task_id].is_completed == False:
            task_instance._tasks[task_id].is_completed = task.is_completed
            return {
                "message": "Task update successfully",
                "data": task_instance._tasks[task_id]
                }
        if task.is_completed == False and task_instance._tasks[task_id].is_completed == True:
            task_instance._tasks[task_id].is_completed = task.is_completed
            return {
                "message": "Task update successfully",
                "data": task_instance._tasks[task_id]
                }

@app.delete("/tasks/{task_id}")#, status_code = status.HTTP_204_NO_CONTENT)
def delete(task_id:int):
    if task_id in task_instance._tasks:
        del task_instance._tasks[task_id]
        return {
                "message": "Task deleted successfully"
                }
    else:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Task with ID not found"
                )

