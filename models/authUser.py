from pydantic import BaseModel
from fastapi import Depends
from sqlalchemy.orm import Session
from models.user import User
from database import get_db


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    def get_user(username: str, db: Session = Depends(get_db)):
        return db.query(User).filter(User.username == username).first()

    def get_user_from_email(email: str, db: Session = Depends(get_db)):
        return db.query(User).filter(User.email == email).first()


class UserLogin(BaseModel):
    username: str
    password: str
