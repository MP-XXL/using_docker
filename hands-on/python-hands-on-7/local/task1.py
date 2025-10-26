"""

LEARNING OBJECTIVES:
- Practice CRUD operations with REST APIs
- Implement filtering and searching
- Handle query parameters for sorting and pagination
- Generate summaries and reports
- Work with enumerations and validation

PROJECT OVERVIEW:
Build a REST API to manage a library of books with categories, authors, and reporting features.

INSTRUCTIONS:
Complete the TODO sections below to build a fully functional Book Library AP
Note: Containerize your App
"""

""" Model"""
from enum import Enum
from pydantic import BaseModel
from datetime import date
from typing import List, Optional, Dict

class BookCategory(str, Enum):
    """Enum for book categories"""
    FICTION = "fiction"
    NONFICTION = "nonfiction"
    SCIENCE = "science"
    HISTORY = "history"
    BIOGRAPHY = "biography"
    TECHNOLOGY = "technology"
    OTHER = "other"

class BookCreate(BaseModel):
    title: str
    author: str
    category: BookCategory
    published_date: date

class Book(BookCreate):
    book_id: int

class AuthorSummary(BaseModel):
    author: str
    book_count: int


class CategorySummary(BaseModel):
    category: str
    book_count: int


""" Databasemodel"""

from typing import List, Optional

class Database:
    """In-memory database template for books"""

    def __init__(self):
        self._books: List[Book] = []
        self._current_id = 1

    def generate_id(self) -> int:
        """Generate next book ID"""
        # TODO: Implement ID generation
        self._current_id += 1

    def add_book(self, book: BookCreate) -> Book:
        """Add a new book to the database"""
        # TODO: Implement adding a book
        if not book:
            raise HTTPException(
                    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail = "Invalid content entered!")
        else:
            db._books.append(book)


    def get_all_books(self) -> List[Book]:
        """Return all books"""
        # TODO: Implement retrieving all books
        if len(self._books) == 0:
            raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = "Library is empty!")
        else:
            data = self._books
            return data

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Find a book by ID"""
        # TODO: Implement lookup by ID
        for book in db._books:
            if book.book_id == book_id:
                return book
        else:
            raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = "Book with ID not found!")

    def update_book(self, book_id: int, updates: dict) -> Optional[Book]:
        """Update book details by ID"""
        # TODO: Implement update
        for book in db._books:
            if book.book_id == book_id:
                """if book.title != None:
                    book.title = updates.title
                if book.author != None:
                    book.author = updates.author
                if book.category != None:
                    book.category = updates.category"""
                return {
                        "message": "Book updated successfully",
                        "data":book
                        }
        #return updates

    def delete_book(self, book_id: int) -> bool:
        """Delete a book by ID"""
        # TODO: Implement delete
        for book in db._books:
            if book.book_id == book_id:
                value = db._books.index(book)
                del db._books[value]
                return True

    def get_books_by_category(self, category: BookCategory) -> List[Book]:
        """Retrieve all books in a given category"""
        # TODO: Implement category filter
        category_list = []
        for book in db._books:
            if book.category == category:
                category_list.append(book)

        return category_list
                


    def get_author_summary(self) -> List[AuthorSummary]:
        """Return count of books per author"""
        # TODO: Implement author summary
        authors_summary = []
        authors_list = []
        count = 0

        for book in db._books:
            if book.author in authors_list:
                continue
            if book.author not in authors_list:
                authors_list.append(book.author)
        for author in authors_list:
            for book in db._books:
                if author == book.author:
                    count += 1
            summary = AuthorSummary(
                        author = author,
                        book_count =  count
                        )
            authors_summary.append(summary)
            count = 0
        return authors_summary

    def get_category_summary(self) -> List[CategorySummary]:
        """Return count of books per category"""
        # TODO: Implement category summary
        category_summary = []
        category_list = []
        count = 0

        for book in db._books:
            if book.category in category_list:
                continue
            if book.category not in category_list:
                category_list.append(book.category)
        for category in category_list:
            for book in db._books:
                if category == book.category:
                    count += 1
            summary = CategorySummary(
                        category = category,
                        book_count =  count
                        )
            category_summary.append(summary)
            count = 0
        return category_summary



"""
API ENDPOINT
"""

from fastapi import FastAPI, HTTPException, status
from typing import List, Optional

app = FastAPI(title="Book Library API")

db = Database()  # in-memory database instance

@app.get("/")
def home():
    return {
            "message": "Welcome to library home!"
            }

@app.post("/books")
def create_book(book: BookCreate):
    """Add a new book"""
    # TODO: Call db.add_book and return the new book
    new_book = Book(
                book_id = db._current_id,
                title = book.title,
                author = book.author,
                category = BookCategory.FICTION,
                published_date = book.published_date
                )
    db.add_book(new_book)
    db.generate_id()
    return {
            "message": "Book added successfully to the library",
            "data": new_book
            }


@app.get("/books")
def list_books(category: Optional[BookCategory] = None) -> List[Book]:
    """List all books or filter by category"""
    # TODO: Return db.get_all_books or db.get_books_by_category
    if category != None:
        return db.get_books_by_category(category)
    else:
        return db.get_all_books()

@app.get("/books/{book_id}")
def get_book(book_id: int):
    """Retrieve a book by ID"""
    # TODO: Return db.get_book_by_id or raise 404
    if not book_id:
            raise HTTPException(
                    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail = "Invalid input received!")
    else:
        return db.get_book_by_id(book_id)

@app.put("/books/{book_id}")
def update_book(book_id: int, updates: BookCreate):
    """Update a book by ID"""
    # TODO: Call db.update_book and return updated book
    for book in db._books:
        if book.book_id == book_id:
            if book.title != None:
                book.title = updates.title
            if book.author != None:
                book.author = updates.author
            if book.category != None:
                book.category = updates.category
            return db.update_book(book_id,updates)
    else:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Book with ID not found")



@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    """Delete a book by ID"""
    # TODO: Call db.delete_book or raise 404
    for book in db._books:
        if book.book_id == book_id:
            db.delete_book(book_id)
            return {
                    "message": "Book deleted successfully"
                    }
    else:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Book with ID not found!"
                )

@app.get("/summary/authors")
def author_summary():
    """Return summary of books per author"""
    # TODO: Call db.get_author_summary
    return db.get_author_summary()

@app.get("/summary/categories")
def category_summary():
    """Return summary of books per category"""
    # TODO: Call db.get_category_summary
    return db.get_category_summary()

