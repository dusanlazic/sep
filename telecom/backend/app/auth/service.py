import jwt
from fastapi import HTTPException, Response
from passlib.context import CryptContext
from pydantic import SecretStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..config import config
from .models import *
from .schemas import (
    UserBriefDataResponse,
    UserLoginRequest,
    UserRegistrationRequest,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register(db: Session, user: UserRegistrationRequest) -> UserBriefDataResponse:
    """
    Registers a new user.

    :param db: Database session.
    :param user: User registration request data.
    :return: User brief data response.
    """
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists.")

    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        username=user.username,
        full_name=user.full_name,
        password_hash=hashed_password,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error while creating the user.")

    return UserBriefDataResponse(
        username=new_user.username,
        full_name=new_user.full_name
    )

def login(db: Session, creds: UserLoginRequest, response: Response) -> UserBriefDataResponse:
    """
    Logs a user in.

    :param db: Database session.
    :param creds: User login request data.
    :param response: Response object to set cookies.
    :return: User brief data response.
    """
    user = db.query(User).filter(User.username == creds.username).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    if not pwd_context.verify(creds.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    token: SecretStr = jwt.encode(
        {"id": str(user.id), "username": user.username},
        key=config.jwt_secret,
        algorithm="HS256"
    )

    response.set_cookie(key="access_token", value=token, httponly=True)

    return UserBriefDataResponse(
        username=user.username,
        full_name=user.full_name
    )

def get_current_user(db: Session, user_id: UUID) -> UserBriefDataResponse:
    """
    Retrieve the current user's data.

    :param db: Database session.
    :param current_user_id: User ID.
    :return: User brief data response.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
  
    return UserBriefDataResponse(
        username=user.username,
        full_name=user.full_name
    )
