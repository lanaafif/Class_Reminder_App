from fastapi import APIRouter, Depends, HTTPException, Path, status, Request
from pydantic import BaseModel, Field
from ..models import Todos
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="TodoApp/templates")  


router = APIRouter(
    prefix='/todos',
    tags=['todos']
)


def get_db():
    # dependency injection
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]



class TodoRequest(BaseModel):
    # only 4 fields here since the id donnot need to be provided by the user
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, le=5)
    complete: bool


def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


### Pages ###

@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        # request 就是“这次浏览器发来的 HTTP 请求的完整信息包”，
        # 你可以用它查到任何细节，包括 cookie、参数、headers、body、IP 等等。

        if user is None:
            return redirect_to_login()
        
        todos = db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

        return templates.TemplateResponse("todo.html", {"request": request, "todos": todos})
    
    except:
        return redirect_to_login()




### Endpoints ###

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user:user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    # db.query(Todos) just creates a query object, it doesn't execute the query 
    # "创建了一个可链式调用的查询语句构建器"
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    # 在正式接口里这段代码是冗余的（因为已经验证过user了），但为了测试、兼容性和防御性考虑，可以保留这段判断。

    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    # TodoRequest 是一个 Pydantic Schema（表示请求数据结构）
    # Todos 是一个 SQLAlchemy Model（表示数据库中的表结构）
    # todo_model 是一个 SQLAlchemy Model 实例/instance（表示数据库中即将插入的一行）
    
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, 
                      todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # we cannot create a new updated todo and delete the old one b/c sqlalchemy try to increment the id 
    #  so the new id will be different from the old one
    # so we should directly update the existing todo 
    # 我们不能也不应该手动设置id
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    
    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
    db.commit()