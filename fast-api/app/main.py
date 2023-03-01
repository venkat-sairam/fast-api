import psycopg2
from typing import Optional, List

from fastapi import FastAPI, Response, status, HTTPException, Depends

from . import models, schemas
from .database import engine,  get_db, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/get_all_posts")
def get_all_posts(db: Session = Depends(get_db), response_model=schemas.PostAllResponses):
    posts = db.query(models.Post).all()

    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(title=post.title, content=post.content,
                           published=post.published)

    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_posts(id: int, db: Session = Depends(get_db)):
    result_data = db.query(models.Post).filter(models.Post.id == id).first()
    # print(result_data.title)
    # print(result_data.id)
    # print(result_data.content)

    return {result_data}


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate,  db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} doesn't exists")

    # post_query.update({"title": "This is my updated title",
        #                   "content": "updated content"}, synchronize_session=False)

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()


@app.delete("/posts_del/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):

    result_data = db.query(models.Post).filter(models.Post.id == id)

    if result_data.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="page not found with given id")
    result_data.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ===========================================================================
# User Registration
# ===========================================================================


@app.post("/users")
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


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
