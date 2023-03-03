from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # user_credentials: schemas.CreateUser

    # username = Email address from form data in POSTMAN
    # user_result = Verify Whether the user is registered or not
    user_result = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    # When the user is not registered.......
    if not user_result:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"verify your login credentials....")

    # If user, then verify the provided password against the hashed password.
    if not utils.verifyPassword(user_credentials.password, user_result.password):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    # create a token based on the user_id stored in the DB(primary key for the Users Table).
    access_token = oauth2.create_access_token(data={"user_id": user_result.id})
    # Return the token
    return {"access_token": access_token, "token_type": "bearer"}
