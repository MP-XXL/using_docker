from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class CreateUser(BaseModel):
    name: str
    age: int
    isMarried: bool

class UpdateUser(BaseModel):
    name: str | None = None
    age: int | None = None
    isMarried: bool | None = None


users = {
        1: {
            "name": "Mac",
            "age": 20,
            "isMarried": False
            },
        2: {
            "name": "Ken",
            "age": 30,
            "isMarried": True
            }
        }


@app.get("/")
async def roots():
    return {"message": "Hello Fast API"}

@app.get("/get_user_by_id/{user_id}")
def get_user_id(user_id: int):
    if user_id in users:
        return users[user_id]
    else:
        return "User with ID does not exist!"

@app.get("/get_user_by_name/{username}")
async def get_user_name(name: str):
    for user in users:
        if users[user]["name"] == name:
            return users[user]
        else:
            return "No user with that name!"

@app.post("/add_user/{user_id}")
def add_user(userId: int, user: CreateUser):
    if userId in users:
        return "User already exists!"
    else:
        users.update({userId:{"name": user.name, "age": user.age, "isMarried": user.isMarried}})
        return users[userId]

@app.put("/update_user/{user_id}")
def update_user(user_id: int, user: UpdateUser):
    if user_id in users:
        if user.name != None:
            users[user_id]["name"] = user.name
        if user.age != None:
            users[user_id]["age"] = user.age
        if user.isMarried != None:
            users[user_id]["isMarried"] = user.isMarried
        return users[user_id]
    else:
        return "User does not exist!"

@app.delete("/delete_user/{user_id}")
def delete_user(user_id:int):
    if user_id in users:
        del users[user_id]
        return "User deleted successfully!"
    else:
        return "User does not exist!"
