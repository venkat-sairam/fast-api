from jose import JWTError, jwt
from datetime import datetime, timedelta
from json import JSONDecodeError, dumps
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# provide secret key
# Provide the Algorithm to be used
# Token Expiration Time

#
# import secrets
# secrets.token_hex(32)

SECRET_KEY = "46479369c15877a9051b7d96c13de883bcc6526dc8d686917a1eced55c86d606"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):

    to_encode = data.copy()

    """Setting the token Expiry time using the current time and expiry time in minutes"""

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Creates token based on the user_id, 32-bit secret key and HS256 Algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_Access_token(token: str, credentials_exception):
    """ 
        1.payload_data = Decodes the data based on Toekn, 32-bit Secret Key and the HS256 Algorithm
        2. Retrieves the user_id from the payload_data
        3. Return the user_id to the client.
    """
    try:
        payload_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        payload_id: str = payload_data.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=payload_id)
    except JWTError:
        raise credentials_exception
    return token_data


# Here tokenURL is the END POINT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate the credentials")
    token_data = verify_Access_token(token, credentials_exception)
    user_data = db.query(models.User.id == token_data.id).first()
    return user_data
