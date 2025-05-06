from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from models import Todos, Users
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user


router = APIRouter(
    prefix='/admin',
    tags=['admin']
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



@router.get('/', status_code=status.HTTP_200_OK)
async def read_all_todos(db: db_dependency, user: user_dependency):
    
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    return db.query(Todos).all()


@router.get("/users", status_code=status.HTTP_200_OK)
async def read_all_users(db: db_dependency, user: user_dependency):

    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    return db.query(Users).all()
    # JWT的本质：服务器/数据库不存token，每次请求只需要验证 token 本身成立即可，无需和数据库核对
    # 但是服务器仍然需要存user的基础信息用于首次登陆时给用户创建token，但是后续就无需访问数据库的用户信息来验证
    # 因为JWT登陆只需验证JWT本身，不检查数据库，所以他是无状态的（stateless）-- 服务器不保存任何登录状态和信息
    # 因此，非用户本人拿到token也可以直接验证成功；数据库的用户的role改变了，用token还是可以以之前的身份访问



@router.delete('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):

    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    # db.delete(todo_model)也可以，不行的是update中创建一条新的放回去
    # todo_model.delete() 不可用，因为 ORM 实例本身没有 delete() 方法。
    # 实例就像被取出的书，无法自己从数据库中删除，必须通过 db.delete(...) 让 session 管理员来删除。

    db.commit()