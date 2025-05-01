from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Book:
    id: int
    title: str  
    author: str
    description: str
    rating: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length = 3) 
    author: str = Field(min_length = 1)
    description: str = Field(min_length = 1, max_length = 100)
    rating: int = Field(gt = -1, lt = 6)


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book', 5),
    Book(2, 'Learn fastapi', 'codingwithroby', 'A good book', 5),
    Book(3, 'Learn python', 'codingwithroby', 'A ok book', 5),
    Book(4, 'Learnnnnn', 'author 1', 'good', 2),
    Book(5, 'Learn1', 'author 2', 'good', 3),
    Book(6, 'Learn2', 'author 3', 'good', 1),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.post("/create-nook")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book
