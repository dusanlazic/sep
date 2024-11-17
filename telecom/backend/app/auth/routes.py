from uuid import UUID

from fastapi import APIRouter, Depends, Response

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
def register(user: UserRegistrationRequest) -> UserBriefDataResponse:
    pass


@router.post("/login", response_model=UserBriefDataResponse)
def login(creds: UserLoginRequest) -> UserBriefDataResponse:
    """
    Issues an access token cookie to the user.
    """
    pass


@router.post("/logout")
def logout(response: Response) -> dict[str, str]:
    """
    Unset the user's access token cookie.
    """
    response.delete_cookie("access_token")
    return {"detail": "Logged out."}


@router.get("/me", response_model=UserBriefDataResponse)
def get_current_user(
    current_user_id: UUID = Depends(get_current_user),
) -> UserBriefDataResponse:
    """
    Retrieve the current user's data.
    """
    pass
