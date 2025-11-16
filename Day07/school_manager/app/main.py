from fastapi import FastAPI, HTTPException, status
from .routes import students_routes

app = FastAPI(
    title = "School Manager",
    version = "0.0.1",
    description = "My Integrated docker fastApi + mySQL"
    )

app.include_router(students_routes.router)