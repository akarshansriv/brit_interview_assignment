import os
import datetime
from fastapi import HTTPException, Header
from dotenv import load_dotenv
from jose import jwt, JWTError

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def get_authorization_header(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        token = authorization.split()[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check token expiry
        exp_timestamp = payload.get("exp")
        if exp_timestamp is None:
            raise HTTPException(status_code=401, detail="Invalid token format")

        expiration = datetime.datetime.fromtimestamp(exp_timestamp, tz=datetime.timezone.utc)
        if datetime.datetime.now(datetime.timezone.utc) > expiration:
            raise HTTPException(
                status_code=401, detail="Token expired, please log in again"
            )

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return token