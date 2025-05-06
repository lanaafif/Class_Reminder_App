from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from models import Todos, Users
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix='/users',
    tags=['users']
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
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
# bcrypt_context是一次类的构造函数调用（创建对象）, bcrypt_context.verify(...)才是一个function call


class UserVerification(BaseModel):
    password: str
    new_password: str



@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    return db.query(Users).filter(Users.id == user.get('id')).first()


# 如果要接收多个字段的 JSON 数据，建议用一个 Pydantic 模型，而不是多个 Body(...)
# 因为实际上，一个json请求体是在一个{}里的key value pair，本质上他应该只对应一个接收对象（一个花括号是一个整体
# 因此，一个pydantic structure正好很好的捕获一个完整的json请求
# 在这个例子，我们要同时接受新的密码和旧的密码
@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    # 在 SQLAlchemy 中，数据库中的每一张表，都会被映射成一个 Python 类
    # 每一行数据，就是这个类的一个 实例对象，一个 SQLAlchemy 的对象

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Wrong old password')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    # encode不是加密，是把人读的文字二进制化等等，进行编码，方便传输
    # hash也不是加密，加密是可以解密的，hash不可以解密，
    # hash过程不可逆，hash了就还原不回来了，只能对比hash之后是否一样

    db.add(user_model)
    db.commit()
    # 如果这个对象是新建的（从来没存过），add() + commit() ➜ 会 INSERT 新数据
    # 如果这个对象是查出来然后被修改了，commit() ➜ 会 UPDATE 原有数据
    # add() 并不会立刻写入数据库，它只是“登记这个对象”，等待 commit() 提交