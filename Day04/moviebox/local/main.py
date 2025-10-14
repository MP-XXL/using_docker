from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

movies: Dict[int, dict] = {
        1: {
            "title": "one_punch_man",
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

class AddMovie(BaseModel):
    title: str
    ratings: float
    year: int
    trending: bool

class UpdateMovie(BaseModel):
    title: str | None = None
    ratings: float | None = None
    year: int | None = None
    trending: bool | None = None



@app.get("/")
def home_page():
    return "Welcome to the movie box api home!"

@app.get("/get-movie-id/{movie_id}")
def get_movie_id(movie_id: int):
    if movie_id not in movies:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Movie ID not found!"
                )
    else:
        return {
                "success": True,
                "data": movies[movie_id],
                "message": "movie found"
                }

@app.get("/get-movie_title/{movie_title}")
def get_movie_title(movie_title: str):
    for movie in movies:
        if movies[movie]["title"] == movie_title:
            return {
                    "success": True,
                    "data": movies[movie],
                    "message": "movie found"
                    }
    else:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Movie name not found")
        details= "Movie not found!"

@app.get("/all-movies")
def all_movies():
    return {
            "success": True,
            "movie_libray": movies,
            "message": "All movies retrieved successfully"}

@app.post("/add-movie/{movie_id}")
def add_movie(movie_id: int, movie: AddMovie):
    if movie_id in movies:
        return {
                "success": False,
                "message": "Movie ID already exists"
                }
    else:
        movies.update(
                {movie_id: {
                    "title":movie.title,
                    "ratings": movie.ratings,
                    "year": movie.year,
                    "trending": movie.trending
                    }
                }
            )
        return {
                "success": True,
                "data": movies[movie_id],
                "message": "Movie added successfully"
                }

@app.put("/update-movie/{movie_id}")
def update_movie(movie_id: int, movie: UpdateMovie):
    if movie_id not in movies:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Movie ID not found")
    else:
        if movie.title != None:
            movies[movieId]["title"] = movie.title
        if movie.ratings != None:
            movies[movie_id]["ratings"] = movie.ratings
        if movie.year != None:
            movies[movie_id]["year"] = movie.year
        if movie.trending != None:
            movies[movie_id]["trending"] = movie.trending
        return {
                "success": True,
                "data": movies[movie_id],
                "message": "Movie updated successfully"}

@app.delete("/delete-movie/{movie_id}")
def delete_movie(movie_id: int):
    if movie_id not in movies:
        raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail = "Movie ID does not exist"
                )
    else:
        del movies[movie_id]
        return {
                "success": True,
                "message": "Movie deleted successfully"
                }
