from datetime import datetime
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str


class UserResponse(BaseModel):
    id: int
    username: str


class UserLogin(UserCreate):
    pass


class ExpenseCreate(BaseModel):
    amount: int
    expense_type: str


class ExpenseResponse(ExpenseCreate):
    id: int
    created_at: datetime
