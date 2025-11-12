import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
from models import Base, Expense, User

CONNECTION_STRING = os.getenv("DATABASE_CONNECTION")

try:
    engine = create_engine(CONNECTION_STRING, echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)
except Exception as error:
    print(f"{error} couldn't connect to database")
