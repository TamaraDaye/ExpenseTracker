from datetime import datetime
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    """
    function to verify hashed password in database
    """
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    creates a password hash
    """
    return password_hash.hash(password)


async def filter_expenses(current_date: datetime, expenses, filter: str | None = None):
    """
    filters expenses based on the dates created week, or months
    """
    number = 1

    result = []

    days = 7

    if filter is None:
        return expenses

    if len(filter.split()) > 1:
        number = int(filter.split()[0])

    print(filter)

    for expense in expenses:
        if filter == "month" or "months" in filter.split():
            days = 30
        timerange = current_date - expense.created_at
        if timerange.days <= days * number:
            result.append(expense)

    return expenses if result is None else result
