from fastapi import FastAPI, Request, status
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import RedirectResponse


app = FastAPI()

Base.metadata.create_all(bind=engine)


app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static") 
# Mount the /static path and name it "static"
# This allows referencing static files in templates using url_for("static", path="img/xxx.png")
# The resulting path is /static/img/xxx.png

@app.get("/")
def test(request: Request): # Jinja2Templates requires the request object as a parameter
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)