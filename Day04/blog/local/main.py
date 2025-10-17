from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

posts: Dict[int, dict] = {
        1: {
            "author": "Walsh",
            "content": "Something nice!"
            },
        2: {
            "author": "Lizz",
            "content": "Something very nice!"
            },
        3: {
            "author": "Andy",
            "content": "Something extremely nice!!!!"
            }


        }

class CreatePost(BaseModel):
    author: str
    content: str

class UpdatePost(BaseModel):
    author: str | None = None
    content: str | None = None

@app.get("/")
def home():
    return {
            "message": "Welcome to our blog"
            }
@app.get("/posts")
def all_post():
    return {
            "success": True,
            "post library": posts,
            "message": "Displaying all posts"
            }

@app.post("/posts/{post_id}")
def create_post(post_id: int, post: CreatePost):
    if post_id in posts:
        raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "Post ID already exists!")
    else:
        posts.update(
                {
                    post_id: {
                        "author": post.author,
                        "content": post.content
                        }
                    }
                )
        return {
                "success": True,
                "message": "Post created successfully!"
                }

@app.put("/posts/{post_id}")
def update_post(post_id: int, post: UpdatePost):
    if post_id not in posts:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Post ID not found!"
                )
    else:
        if post.author != None:
            posts[post_id]["author"] = post.author
        if post.content != None:
            posts[post_id]["content"] = post.content
        return {
                "success": True,
                "data": posts[post_id],
                "message": "Post updated successfully!"
                }

@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    if post_id not in posts:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Post ID not found!"
                )
    else:
        del posts[post_id]
        return {
                "success": True,
                "message": "Post deleted successfully!"
                }
