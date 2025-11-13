from sqlalchemy import select
from . import Oauth2
from ..database import models
from ..database.database import SessionDep
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import utils

router = APIRouter()


@router.post("/login/")
async def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
):
    """
    Endpoint to log a user in and retrieve jwt token to be stored by front end
    """
    stmt = select(models.User).where(models.User.email == user_credentials.username)

    user = session.scalar(stmt)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials "
        )
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )
    access_token = Oauth2.create_access_token(data={"user_id": user.id})

    return access_token
