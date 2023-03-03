

from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from .. database import get_db, SessionLocal

router = APIRouter(prefix="/users")


"""
Pydanic type checking with schemas.CreateUser ensures that the user provides
correct input attributes 
"""


@router.post("/", response_model=schemas.ResponseToUser)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    # Hash the password at first by calling the hashing function
    hashed_password = utils.hashPWD(user.password)
    user.password = hashed_password
    # unpacks the dicionary into individual attributes K: V
    new_user = models.User(**user.dict())

    # checking if the user is already registered or not
    try:
        temp = db.query(models.User).filter(
            models.User.email == new_user.email)
        temp_result = temp.first()
        if temp_result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Email id is already Registered.....!")
    except HTTPException as error:
        return {"message": error.detail}

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)):

    user_result = db.query(models.User).filter(models.User.id == id).first()
    if not user_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} doesn't exist.....!")

    return user_result
