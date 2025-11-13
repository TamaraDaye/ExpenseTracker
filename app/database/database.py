import os
from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
from .models import Base

CONNECTION_STRING = os.getenv("DATABASE_CONNECTION")

try:
    engine = create_engine(CONNECTION_STRING)
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)
except Exception as error:
    print(f"{error} couldn't connect to database")


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
