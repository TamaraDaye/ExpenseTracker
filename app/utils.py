from datetime import datetime
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


async def filter_expenses(current_date: datetime, expenses, filter: str | None = None):
    number = 1

    result = []

    if filter is None:
        return expenses

    if len(filter.split()) > 1:
        number = int(filter.split()[0])

    days = 7
    for expense in expenses:
        if filter == "month":
            days = 31
        timerange = current_date - expenses.created_at
        if timerange.timedelta <= days * number:
            result.append(expense)

    return result
