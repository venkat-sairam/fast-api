from typing import List

from fastapi import APIRouter, HTTPException, Path, Response, status
from pydantic import ValidationError
from sqlmodel import Session, select

from api.db.db_setup import engine
from api.db.models.user import User
from api.db.schemas import User_request, User_response
from api.db.utils import get_password_hash

router = APIRouter(
    tags=["user Routes"],
)

# ========================================================================
#                      CREATE USER ROUTE
# ========================================================================


@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=User_response)
def create_user(user: User_request):
    with Session(engine) as db:
        try:
            selected_user = db.exec(select(User).where(User.email == user.email)).first()
            if selected_user:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

            user_obj = User(**user.model_dump())
            # '''
            # convert User_request -> User(ORM model) because database operations are performed on ORM models.
            # so, we need to convert the User_request to User(ORM model) before performing any database operations.
            # we can use the model_validate method to convert the User_request to User(ORM model)
            # Example: user_obj = User.model_validate(user)
            # '''
            # try:
            #     user_obj = User.model_validate(user)
            # except ValidationError:
            #     raise HTTPException(
            #         status_code=status.HTTP_400_BAD_REQUEST,
            #         detail="Invalid input data. Please check your request parameters.",
            #     ) from ValidationError
            # Hash the password before storing it in the database
            user_obj.password_hash = get_password_hash(user.password)
            db.add(user_obj)
            db.commit()
            db.refresh(user_obj)
            return user_obj

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


# ========================================================================
#                      Retrieve USER ROUTE
# ========================================================================


@router.get("/users", response_model=List[User_response], status_code=status.HTTP_200_OK)
def get_user():
    with Session(engine) as db:
        try:
            users = db.exec(select(User)).all()
            if not users:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
            return users
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


# ========================================================================
#                      Retrieve USER BY ID
# ========================================================================


@router.get("/user/{user_id}", response_model=User_response, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int = Path(description="The ID of the user to get", gt=0)):
    with Session(engine) as db:
        try:
            user = db.exec(select(User).where(User.id == user_id)).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return user
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


# ========================================================================
#                      UPDATE USER ROUTE
# ========================================================================


@router.put(
    "/user",
    status_code=status.HTTP_200_OK,
    response_model=User_response,
    description="Update the user details by providing the user Email and the other details",
)
def update_user(new_user_details: User_request):
    with Session(engine) as db:
        try:
            user = db.exec(select(User).where(User.email == new_user_details.email)).all()
            if not user:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

            user.sqlmodel_update(new_user_details.model_dump(exclude_unset=True))

            db.add(user)
            db.commit()
            db.refresh(user)

            return user
        except HTTPException as e:
            raise e

        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid input data. Please check your request parameters.",
            ) from ValidationError


# ========================================================================
#                      DELETE USER ROUTE
# ========================================================================


@router.delete("/user/{user_email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_email: str = Path(description="The Email id of the user to delete", min_length=1)):
    with Session(engine) as db:
        try:
            user = db.exec(select(User).where(User.email == user_email)).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User email {user_email} not found")

            db.delete(user)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
