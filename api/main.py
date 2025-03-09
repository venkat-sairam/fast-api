from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, select

from api.db.db_setup import engine, get_session
from api.db.models.course import Course  # noqa: F401
from api.db.models.user import User
from api.routes.login import router as login_router
from api.routes.user import router as user_router

app = FastAPI(
    title="FastAPI LMS",
    description="This is a simple LMS API",
    version="0.0.1",
    contact={"name": "Venkat", "email": "yvsairam54@gmail.com"},
)


SessionDep = Annotated[Session, Depends(get_session)]

# Create the database engine and tables (if not available at the moment.)
# postgresql_url = "postgresql+psycopg2://postgres:postgres@localhost/db"
# engine = create_engine(postgresql_url, echo=True)


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)


data1 = User(id=2, email='absc@gmail.com', role='student')
data2 = User(id=3, email='test@gmail.com', role='teacher')


def test_db_connection():
    try:
        with Session(engine) as session:
            # Test the connection by executing a simple query
            result = session.exec(select(User)).first()
            print(result)
            session.add(data1)
            session.add(data2)
            session.commit()
            print("Committed the data")

            # If the query executes without errors, then print the result
            redult = session.exec(select(User)).all()
            print(redult)

            print("✅ Connection to the database successful!")
            return {"message": "✅ Connection to the database successful!"}
    except Exception as e:
        error_message = f"❌ Failed to connect to the database: {str(e)}"
        print(error_message)  # Print the error to the console
        return {"error": error_message}  # Return the error message


@app.get("/")
def get_user_root():
    return {"message": "Hello from Main page!"}


create_db_and_tables(engine=engine)
test_db_connection()
app.include_router(router=user_router)
# app.include_router(router=section_router)
# app.include_router(router=course_router)
app.include_router(router=login_router)
