import os
import datetime
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
from models.user import User
from passlib.context import CryptContext
from database import get_db
from models.authUser import UserCreate, UserLogin

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash the password
def hash_password(password: str):
    return pwd_context.hash(password)


# Create access token
def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Login Route
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user is None or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": db_user.username})
    db.commit()

    return {"access_token": access_token, "token_type": "bearer"}


# User Registration Route
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = UserCreate.get_user(user.username, db)
    existing_mail = UserCreate.get_user_from_email(user.email, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    if existing_mail:
        raise HTTPException(status_code=400, detail="Mail id already registered")

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}


@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    """
    Invalidate the token on the client-side by clearing it.
    This API doesn't do much on the server-side since JWT tokens are stateless.
    """
    return {"message": "Logged out successfully. Please go to the homepage."}
