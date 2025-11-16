from fastapi import FastAPI, APIRouter, HTTPException, status


router = APIRouter()

@router.get("/")
def home():
    return {
        "success": True,
        "message": "Welcome to student manager hompage!"
    }