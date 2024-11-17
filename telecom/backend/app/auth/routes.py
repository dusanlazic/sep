from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from ..database import get_db
from . import service
from .dependencies import get_current_user
from .schemas import (
    UserBriefDataResponse,
    UserLoginRequest,
    UserRegistrationRequest,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register", summary="Register a new user", response_model=UserBriefDataResponse
)
def register(db: Annotated[Session, Depends(get_db)], user: UserRegistrationRequest) -> UserBriefDataResponse:
    """
    Registers a new user.
    """
    return service.register(db, user)


@router.post("/login", response_model=UserBriefDataResponse)
def login(db: Annotated[Session, Depends(get_db)], creds: UserLoginRequest, response: Response) -> UserBriefDataResponse:
    """
    Issues an access token cookie to the user.
    """
    return service.login(db, creds, response)


@router.post("/logout")
def logout(response: Response) -> dict[str, str]:
    """
    Unset the user's access token cookie.
    """
    response.delete_cookie("access_token")
    return {"detail": "Logged out."}


@router.get("/me", response_model=UserBriefDataResponse)
def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    current_user_id: UUID = Depends(get_current_user),
) -> UserBriefDataResponse:
    """
    Retrieve the current user's data.
    """
    return service.get_current_user(db, current_user_id)
