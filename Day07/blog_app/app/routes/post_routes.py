from fastapi import FastAPI, status, HTTPException, APIRouter
from ..models.models import Post, PostResponse, PostUpdate, PostUpdateResponse
from ..database.database import db
from ..raw_sql import queries
from datetime import datetime

router = APIRouter()



@router.post("/posts")
def create_post(post: Post):
    new_post = PostResponse(
        **post.model_dump(),
        created_at = datetime.now(),
        updated_at = datetime.now()
    )
    # CREATE_POST = """
    # INSERT INTO users(title, user_id) VALUES(%s, %s); ############# ALTERNATIVE METHOD
    # """
    with db.get_cursor() as cursor:
        cursor.execute(queries.CREATE_POST, (post.title, post.user_id))
    
    return {
        "success": True,
        "data": new_post,
        "message": "New post added successfully!"
    }

@router.patch("/posts/{user_id}")
def update_post(user_id: int, post: PostUpdate):
    if not user_id:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail = "Bad user input"
        )
    with db.get_cursor() as cursor:
        cursor.execute(queries.UPDATE_POST, (post.title, user_id))
    updated_post = PostUpdateResponse(
        **post.model_dump(),
        updated_at = datetime.now()
    )
    return {
        "sucess": True,
        "data": updated_post,
        "message": "Post updated successfully"
    }


@router.get("/posts")
def get_all_posts():
    with db.get_cursor() as cursor:
                cursor.execute(queries.GET_ALL_POSTS)
                data = cursor.fetchall()

    return {
        "data":data
    }