import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
from models import Base, User

CONNECTION_STRING = os.getenv("DATABASE_CONNECTION")

print(CONNECTION_STRING)

try:
    engine = create_engine(CONNECTION_STRING, echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)
except Exception as error:
    print(f"{error} couldn't connect to database")


with Session(engine) as session:
    stmt = select(User).where(User.username.in_(["danni", "tamara"]))

    for user in session.scalars(stmt):
        print(user)
