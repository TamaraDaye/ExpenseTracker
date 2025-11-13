from typing import Annotated
from fastapi import APIRouter, Body, Depends, Form, Path
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


@router.get("/user/me", tags=["users"])
async def read_current_user(
    current_user: Annotated[models.User, Depends(Oauth2.get_current_user)],
):
    pass


@router.post("/signup/", tags=["users"], response_model=schemas.UserResponse)
async def create_user(data: Annotated[schemas.UserCreate, Form()], session: SessionDep):
    data.password = get_password_hash(data.password)
    user = models.User(**data.model_dump())
    session.add(user)
    session.flush()
    session.commit()
    return user


@router.post(
    "/users/expenses", tags=["expenses"], response_model=schemas.ExpenseResponse
)
async def create_expense(
    current_user: Annotated[models.User, Depends(Oauth2.get_current_user)],
    expense: Annotated[schemas.ExpenseCreate, Body()],
    session: SessionDep,
):
    result = models.Expense(**expense.model_dump(), user=current_user)
    session.add(result)
    session.flush()
    session.commit()
    return result
