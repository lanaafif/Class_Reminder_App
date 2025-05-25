from fastapi import APIRouter, Request
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from fastapi.responses import RedirectResponse
from datetime import timedelta
import os

from TodoApp.models import Users
from TodoApp.database import SessionLocal
from TodoApp.routers.auth import create_access_token

router = APIRouter()

# OAuth settings
config = Config(environ=os.environ)
oauth = OAuth(config)

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/auth/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/callback")
async def auth_callback(request: Request):
    try:
        print("🔄 Received Google callback")

        token = await oauth.google.authorize_access_token(request)
        print("✅ Got token successfully")

        user_info = token["userinfo"]
        print("✅ Got user info:", user_info.get("email"), "|", user_info.get("name"))

        email = user_info["email"]
        username = email.split("@")[0]
        first_name = user_info.get("given_name", "")
        last_name = user_info.get("family_name", "")

        db = SessionLocal()
        db_user = db.query(Users).filter(Users.email == email).first()

        if not db_user:
            print("🆕 Registering new user:", email)
            db_user = Users(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                hashed_password="",
                role="user",
                is_active=True,
                phone_number=""
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)

        jwt_token = create_access_token(
            username=db_user.username,
            user_id=db_user.id,
            role=db_user.role,
            expires_delta=timedelta(minutes=20)
        )

        print("✅ Issued JWT for", db_user.username)

        response = RedirectResponse(url="/todos/todo-page")
        response.set_cookie(key="access_token", value=jwt_token, httponly=True)
        return response

    except Exception as e:
        print("❌ Error in auth_callback:", e)
        raise e
