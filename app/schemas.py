from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr


class UserLogin(UserCreate):
    pass


class ExpenseCreate(BaseModel):
    amount: int
    Expense: str


class ExpenseUpdate(ExpenseCreate):
    pass
