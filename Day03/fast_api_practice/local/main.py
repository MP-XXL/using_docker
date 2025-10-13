from fastapi import FastAPI


app = FastAPI()

users = {
        1: {
            "name": "Mac"
            }
        }
@app.get("/")
async def roots():
    return {"message": "Hello Fast API"}

@app.get("/get_user/{user_id}")
def test2(user_id: int):
    return users[user_id]
