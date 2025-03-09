from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from api.db.db_setup import engine
from api.db.models.user import User
from api.db.schemas import User_login_response
from api.db.utils import verify_password

from .oauth import create_access_token

router = APIRouter(
    tags=["Login Route"],
)

# ========================================================================
#                      CREATE USER LOGIN ROUTE
# ========================================================================


@router.post("/login", status_code=status.HTTP_200_OK, response_model=User_login_response)
def login_user(user):
    with Session(engine) as db:
        try:
            selected_user = db.exec(select(User).where(User.email == user.username)).first()
            if not selected_user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

            if not verify_password(hashed_password=selected_user.password_hash, plain_password=user.password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

            return {"token": create_access_token(data={"id": user.username}), "token_type": "bearer"}

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
