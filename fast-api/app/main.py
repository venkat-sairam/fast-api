import psycopg2
from typing import Optional, List

from fastapi import FastAPI, Response, status, HTTPException, Depends

from . import models, schemas, utils
from .database import engine,  get_db, SessionLocal
from sqlalchemy.orm import Session
from .routers import post, user, auth
app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Include posts Routers
app.include_router(post.router)

# ===========================================================================
# User Registration
# ===========================================================================
app.include_router(user.router)

# ===========================================================================
# Login Validation
# ===========================================================================

app.include_router(auth.router)


try:
   # conn = psycopg2.connect(host, database, user, password)
    pass
except Exception as e:
    print(e)


myposts = [
    {
        "title": "post 1 title",
        "content": "Welcome to the Fast API",
        "id": 1
    },
    {
        "title": "Favourite Ice-creams",
        "content": "Available flavours of ice-creams",
        "id": 2
    }
]


# def find_post(id):
#     for post in myposts:
#         if post["id"] == id:
#             return post


# @app.get("/posts/{id}")
# def get_posts(id: int, response: Response):
#     post = find_post(id)
#     # if not post:
#     #     response.status_code = status.HTTP_404_NOT_FOUND
#     # return {"Post_details are: ": post}

#     if not post:

#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} not found")
