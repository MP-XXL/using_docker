from fastapi import FastAPI
from fastapi import Path
from pydantic import BaseModel

app = FastAPI()

users = {
        1: {
            "username": "jonie",
            "isAdmin": True,
            "status": "active"
            }
        }

class User(BaseModel):
    username: str
    isAdmin: bool
    status: str

class UserUpdate(BaseModel):
    username: str | None = None
    isAdmin: bool | None = None
    status: str | None = None


@app.get("/")
def root():
    return {"name":"Dummy data"}


@app.get("/get-user/{user_id}")
def getuser(user_id: int): #= Path(None, description="The ID of the user to be got")):
    return users[user_id]


@app.get("/get_username/{user_id}")
def get_user_by_name(user_id:int, name: str | None = None):
    for ids in users:
        if users[ids]["username"] == name:
            return users.ids
    return {"Data": "Not found!"}

@app.post("/create-user/{user_id}")
def create_user(user_id: int, user: User):
    if user_id in users:
        return {"Error": "User already exists"}
    users[user_id] = user
    return users[user_id]


@app.put("/update-records/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    if user_id not in users:
        return {"Error": "User does not exist!"}
    if user.username != None:
        users[user_id].username = user.username
    if user.isAdmin != None:
        users[user_id].isAdmin = user.isAdmin
    if user.status != None:
        users[user_id].status = user.status

    return users[user_id]

@app.delete("/delete-user/{user_id}")
def delete_user(user_id: int):
    if user_id not in users:
        return {"Error": "Student does not exist!"}
    del users[user_id]
    return {"message": "Student deleted!"}
