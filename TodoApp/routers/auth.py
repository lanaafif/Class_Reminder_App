from datetime import timedelta, datetime, timezone
from typing import Annotated
from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'c376b1e1b6112627129877f30793f8b00598adb28659f1f5f8fb6614ce38540e'
ALGORITHM = 'HS256'  # algorithm used to encode the JWT token 

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token") 
# 1.
# /auth/token 是一个登录接口，她是你提交用户名密码后，可以查看已获取的，后端传过来的生成的 token 的接口，
#   不是一个可以访问没有生成，没有后端传过来的结果的，查看 token 的页面。
# 你必须提交用户名密码，验证成功后服务器才会生成并返回 token 给你在这个页面。
# 所以这个页面的最好理解是，get token，而不是check token
# 2. 
# OAuth2PasswordBearer 是当这个依赖被某个接口需要时，在接口函数运行前，
#   fastapi帮你获取前端发来的申请中带的header中的“Authorization”信息--token
# 如果依赖获取失败了，会有自动error反馈，然后swagger也更清楚这是一个依赖项/依赖函数

#refine：
# 1.
# /auth/token 是用于“获取 token”的接口，而不是“查看 token”的页面。
# 用户需要向这个接口提交用户名和密码，后端验证通过后才会生成并返回 token。
# 所以更准确地说，它是一个 “获取 token（login）” 的 API，而不是一个“查看 token” 的页面。

# 2.
# OAuth2PasswordBearer 是一个依赖项，用于在某个接口运行前，
# 由 FastAPI 自动从请求头中提取出 "Authorization" 字段里的 Bearer Token。
# 如果缺少 token 或格式不正确，FastAPI 会自动返回 401 错误。
# 同时，这个依赖还能帮助 Swagger UI 显示认证按钮，提升接口文档的可用性。



class CreateUserRequest(BaseModel):
    username: str
    email: str 
    first_name: str
    last_name: str
    password: str
    role: str 


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    # dependency injection
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(db, username: str, password: str):
    user = db.query(Users).filter(Users.user_name == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub':username, 'id':user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):      
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Could not validate user.",)
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Could not validate user.",)
                                                                        


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        user_name=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        roles=create_user_request.role,
        is_active=True
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login_for_access_token(db: db_dependency, 
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Could not validate user.",)
    token = create_access_token(user.user_name, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}