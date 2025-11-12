from sqlalchemy import String, ForeignKey, DateTime, func
from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import enum
from datetime import datetime


class ExpenseType(enum.Enum):
    groceries = "groceries"
    leisure = "leisure"
    electronics = "electronics"
    utilities = "utilities"
    clothing = "clothing"
    health = "health"
    others = "others"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(50))
    expenses: Mapped[List["Expense"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User({self.username}, {self.id})"


class Expense(Base):
    __tablename__ = "expenses"
    id: Mapped[int] = mapped_column(primary_key=True)
    expense_type: Mapped[ExpenseType]
    amount: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )
    user: Mapped["User"] = relationship(back_populates="expenses")

    def __repr__(self) -> str:
        return f"Expense({self.id},{self.expense_type},{self.amount},{self.user})"
