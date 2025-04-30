from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title one', 'author': 'Author one', 'category': 'science'},
    {'title': 'Title two', 'author': 'Author two', 'category': 'history'},
    {'title': 'Title three', 'author': 'Author three', 'category': 'science'},
    {'title': 'Title four', 'author': 'Author two', 'category': 'history'},
    {'title': 'Title five', 'author': 'Author four', 'category': 'math'},
    {'title': 'Title six', 'author': 'Author three', 'category': 'history'}
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
