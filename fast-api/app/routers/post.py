
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from .. database import get_db

router = APIRouter(prefix="/posts")


@router.get("/")
def get_all_posts(db: Session = Depends(get_db), response_model=schemas.PostAllResponses):
    posts = db.query(models.Post).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.dict())

    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_posts(id: int, db: Session = Depends(get_db)):
    result_data = db.query(models.Post).filter(models.Post.id == id).first()
    # print(result_data.title)
    # print(result_data.id)
    # print(result_data.content)

    return result_data


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate,  db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} doesn't exists")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You're Not Authorized to perform the requested operation ")

    # post_query.update({"title": "This is my updated title",
        #                   "content": "updated content"}, synchronize_session=False)

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post


@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_result_set = post_query.first()
    print(post_result_set)
    if post_result_set == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="page not found with given id")
    if post_result_set.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You're Not Authorized to perform the requested operation ")
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
