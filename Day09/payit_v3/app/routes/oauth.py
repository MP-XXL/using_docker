from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import APIRouter, HTTPException, status, Depends, Request
from ..models import users_model
from ..schemas.users_schema import User, UserResponse, UserUpdate
from ..middlewares.auth import AuthMiddleware
from fastapi.responses import RedirectResponse
from ..config.oauth import oauth, AUTH0_DOMAIN, AUTH0_CLIENT_ID
from ..auth.jwt import create_access_token
from datetime import datetime
from typing import List
import logging
import bcrypt
import pymysql

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/oauth",
    tags=["Oauth"]
)


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("callback")
    try:
        return await oauth.auth0.authorize_redirect(request, redirect_uri = redirect_uri)
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Auth Error: Fialed to authenticate user {e}"
        )

@router.get("/callback", name="callback")
async def callback(request: Request, db: Session = Depends(get_db)):
    try:
        print("WORLD")
        token = await oauth.auth0.authorize_access_token(request)
        user_info = token.get("userinfo")
        print("DATA", user_info)
        user = db.query(users_model.User).filter((user_info["email"] == users_model.User.email)).first()

        if not user:
            user = users_model.User(
                name = user_info["name"],
                phone = None,
                email = user_info["email"],
                password = None,
                gender = None,
                location = None
            )

            db.add(user)
            db.commit()
            db.refresh(user)
        jwt = create_access_token(
            {
                "sub": str[user.id],
                "email": user.email,
                "user_id": str(user.id)
            }
        )

        return {
            "access_token": jwt,
            "email": user.email,
            "id": user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Auth Error: Failed to generate token.33333333 {e}"
        )
    except pymysql.DataError as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"DATABASE Error: {e}"
        )


@router.get("/logout")
def logout(request: Request):
    return_url = "http://localhost:8000"

    logout_url = (
        f"https://{AUTH0_DOMAIN}/v2/logout?"
        f"client_id={AUTH0_CLIENT_ID}&"
        f"returnTo={return_url}"
    )

    return RedirectResponse(url=logout_url)