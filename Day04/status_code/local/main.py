from fastapi import FastAPI, status, HTTPException
from typing import Dict, List
from pydantic import BaseModel

app = FastAPI()

db: Dict[int, str] = {
        1: "Sarah",
        2: "Tom",
        3: "Aaron",
        4: "Dorcas"
        }

class User(BaseModel):
    userId: int
    name: str

@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return "Welcome to status codes home!"

@app.get("/code_201", status_code=status.HTTP_201_CREATED)
def created():
    return "Welcome to status codes 201!"

@app.get("/code_204", status_code=status.HTTP_204_NO_CONTENT)
def no_content():
    return "Welcome to status codes 204!"

@app.get("/names")
def get_names():
    return {
            "success": True,
            "data": db,
            "message": "Names retrieved successfully"
            }

@app.get("/get-names")
def get_names_without_id():
    names: List[str] = []
    for _, name in db.items():
        names.append(name)
    return {
            "success": True,
            "data": names,
            "message": "Names retrieved successfully"
            }


@app.get("/names/{userId}")
def get_names_id(userId: int):
    if userId not in db:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = "Id does not exist"
                )
    return db[userId]

@app.post("/create-user", status_code=status.HTTP_200_OK)
def create_user(user: User):
    if not user.userId or not user.name:
        raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail = "All fields are required!"
                )

    new_user = User(
            userId = user.userId,
            name = user.name
    )
    db[new_user.userId] = new_user.name

    return {
            "success": True,
            "data": new_user,
            "message": "User created successfully"
    }
