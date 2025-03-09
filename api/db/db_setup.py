from os import environ

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv()
POSTGRESQL_URI = environ.get("POSTGRESQL_URI")

engine = create_engine(POSTGRESQL_URI, future=True, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
