from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def just_read_root():
    return {"Hello FastApi"}

just_read_root()
