from uuid import UUID

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from ..auth.dependencies import get_current_merchant_manager_id
from ..database import get_db
from . import service
from .schemas import (
    MerchantBriefDataResponse,
    MerchantLoginRequest,
    MerchantRegistrationRequest,
)

router = APIRouter(prefix="/merchants")


@router.post("/register", tags=["Merchant Manager"])
def register(
    new_merchant: MerchantRegistrationRequest,
    db: Session = Depends(get_db),
):
    """
    Registers a new merchant.
    """
    service.register_merchant(db, new_merchant)
    return {"detail": "Merchant registered."}


@router.post("/login", tags=["Merchant Manager"])
def login(
    creds: MerchantLoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    """
    Issues an access token cookie to the merchant.
    """
    token: str | None = service.login_merchant(db, creds.username, creds.password)
    if token:
        response.set_cookie("access_token", token, httponly=True)
        return {"detail": "Logged in."}
    return {"detail": "Invalid credentials."}


@router.post("/logout", tags=["Merchant Manager"])
def logout(response: Response):
    """
    Unset the merchant's access token cookie.
    """
    response.delete_cookie("access_token")
    return {"detail": "Logged out."}


@router.get(
    "/me",
    response_model=MerchantBriefDataResponse,
    dependencies=[Depends(get_current_merchant_manager_id)],
    tags=["Merchant Manager"],
)
def get_current_merchant_manager(
    current_user_id: UUID = Depends(get_current_merchant_manager_id),
    db: Session = Depends(get_db),
) -> MerchantBriefDataResponse:
    """
    Retrieve the current merchant's data.
    """
    return service.get_merchant_by_id(db, current_user_id)
