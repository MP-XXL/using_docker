from sqlmodel import Field, SQLModel, create_engine
from fastapi import FastAPI, HTTPException


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    todo: str = Field(max_length=100)
