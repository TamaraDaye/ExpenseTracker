from datetime import datetime, timezone
from secrets import token_bytes
from typing import Annotated
from fastapi import APIRouter, Body, Depends, Form, Query, HTTPException
from sqlalchemy import select
from .. import utils
from .. import schemas
from app.database import models
from app.database.database import SessionDep
from app.routers import Oauth2
from app.utils import get_password_hash


router = APIRouter()


@router.get("/users/", tags=["users"], response_model=list[schemas.UserResponse])
async def get_users(session: SessionDep):
    """
    function to return a list of users
    """
    users = session.scalars(select(models.User))
    return users


@router.get("/user/me", tags=["users"], response_model=list[schemas.ExpenseResponse])
async def read_current_user(
    session: SessionDep,
    current_user: Annotated[models.User, Depends(Oauth2.get_current_user)],
    filter: Annotated[str | None, Query()] = None,
):
    """
    This function returns the current user that is the user signed with the jwt tokens
    expenses asychronously
    """

    if filter is None:
        return current_user.expenses

    current_date = datetime.now(timezone.utc)

    result = await utils.filter_expenses(
        current_date, current_user.expenses, filter=filter
    )

    return result


@router.post("/signup/", tags=["users"], response_model=schemas.UserResponse)
async def create_user(data: Annotated[schemas.UserCreate, Form()], session: SessionDep):
    """
    Endpoint for creating new users
    """
    data.password = get_password_hash(data.password)
    db_user = models.User(**data.model_dump())
    session.add(db_user)
    session.flush()
    session.commit()
    return db_user


@router.post(
    "/users/expenses", tags=["expenses"], response_model=schemas.ExpenseResponse
)
async def create_expense(
    current_user: Annotated[models.User, Depends(Oauth2.get_current_user)],
    expense: Annotated[schemas.ExpenseCreate, Body()],
    session: SessionDep,
):
    """
    Endpoint for authenticated user to create an Expense
    """
    db_expense = models.Expense(**expense.model_dump(), user=current_user)
    session.add(db_expense)
    session.flush()
    session.commit()
    return db_expense


@router.patch(
    "/users/expenses",
    tags=["expenses"],
    response_model=schemas.ExpenseResponse,
)
async def update_expense(
    current_user: Annotated[models.User, Depends(Oauth2.get_current_user)],
    expense: Annotated[
        schemas.ExpenseUpdate, Body()
    ],  # must contain id + optional fields
    session: SessionDep,
):
    """
    Endpoint for updating a particular expense
    """

    db_expense = session.get(models.Expense, expense.id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    if db_expense.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if expense.amount is not None:
        db_expense.amount = expense.amount

    db_expense.updated_at = datetime.now(timezone.utc)

    session.flush()
    session.commit()
    return db_expense


@router.delete(
    "/users/expenses/{expense_id}",
    tags=["expenses"],
    status_code=204,
)
async def delete_expense(
    expense_id: int,
    current_user: Annotated[models.User, Depends(Oauth2.get_current_user)],
    session: SessionDep,
):
    """Endpoint to delete an Expense"""

    db_expense = session.get(models.Expense, expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    if db_expense.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    session.delete(db_expense)
    session.commit()
    return
