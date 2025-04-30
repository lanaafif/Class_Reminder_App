from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title one', 'author': 'Author one', 'category': 'science'},
    {'title': 'Title two', 'author': 'Author two', 'category': 'history'},
    {'title': 'Title three', 'author': 'Author three', 'category': 'science'},
    {'title': 'Title four', 'author': 'Author two', 'category': 'science'},
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


@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_category_by_query(boook_author: str, category: str):
    books_to_rerurn = []
    for book in BOOKS:
        if book.get('author').casefold() == boook_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_rerurn.append(book)
    
    return books_to_rerurn