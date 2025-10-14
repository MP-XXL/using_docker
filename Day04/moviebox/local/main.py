from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

movies = {
        1: {
            "title": "one punch man",
            "ratings": 8.9,
            "year": 2013,
            "trending": True
            },
        2: {
            "title": "invincible",
            "ratings": 9.0,
            "year": 2022,
            "trending": True
            },
         3: {
            "title": "fireforce",
            "ratings": 8.7,
            "year": 2023,
            "trending": False
            }
        }


@app.get("/")
def home_page():
    return "Welcome to the movie box api home!"

@app.get("/get-movie-id/{movie_id}")
def get_movie_id(movie_id: int):
    if movie_id not in movies:
        return "Movie ID not found!"
    else:
        return movies[movie_id]

@app.get("/get-movie_title/{movie_title}")
def get_movie_title(movie_title: str):
    for movie in movies:
        if movies[movie]["title"] == movie_title:
            return movies[movie]
        else:
            return "Movie not found!"
