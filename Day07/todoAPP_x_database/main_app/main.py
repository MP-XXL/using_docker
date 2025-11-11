from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel
from database_models import models
from database.database import engine

SQLModel.metadata.create_all(engine)

app = FastAPI()
