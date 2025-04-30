from fastapi import Body, FastAPI

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
