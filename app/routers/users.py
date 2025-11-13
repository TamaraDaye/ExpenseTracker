from typing import Annotated
from fastapi import APIRouter, Depends, Form, Path
from sqlalchemy import select, delete, update, insert
from sqlalchemy_utils.types import password
from app import schemas
from app.database import models
from app.database.database import SessionDep
from app.routers import Oauth2
from app.utils import get_password_hash


router = APIRouter()


@router.get("/users/", tags=["users"], response_model=list[schemas.UserResponse])
async def get_users(session: SessionDep):
    users = session.scalars(select(models.User))
    return users


@router.get("/users/{id}", tags=["users"], response_model=schemas.UserResponse)
async def get_user(id: Annotated[int, Path()], session: SessionDep):
    user = session.get(models.User, id)
    return user


@router.post("/users/", tags=["users"], response_model=schemas.UserResponse)
async def create_user(data: Annotated[schemas.UserCreate, Form()], session: SessionDep):
    data.password = get_password_hash(data.password)
    user = models.User(**data.model_dump())
    session.add(user)
    session.flush()
    session.commit()
    return user


@router.get("/users/me")
async def read_current_user(
    current_user: Annotated[models.User, Depends(Oauth2.get_current_user)],
):
    return [{"item_id": "foo", "owner": current_user.username}]
