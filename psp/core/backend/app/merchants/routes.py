from uuid import UUID

from fastapi import APIRouter, Depends, Response

from ..auth.dependencies import get_current_merchant_manager
from . import service
from .schemas import (
    MerchantBriefDataResponse,
    MerchantLoginRequest,
    MerchantRegistrationRequest,
)

router = APIRouter(prefix="/merchants", tags=["Merchant Management"])


@router.post("/register")
def register(new_merchant: MerchantRegistrationRequest):
    """
    Registers a new merchant.
    """
    return {"detail": "Merchant registered."}


@router.post("/login", response_model=MerchantBriefDataResponse)
def login(creds: MerchantLoginRequest) -> MerchantBriefDataResponse:
    """
    Issues an access token cookie to the merchant.
    """
    pass


@router.post("/logout")
def logout(response: Response) -> dict[str, str]:
    """
    Unset the merchant's access token cookie.
    """
    response.delete_cookie("access_token")
    return {"detail": "Logged out."}


@router.get(
    "/me",
    response_model=MerchantBriefDataResponse,
    dependencies=[Depends(get_current_merchant_manager)],
)
def get_current_merchant_manager(
    current_user_id: UUID = Depends(get_current_merchant_manager),
) -> MerchantBriefDataResponse:
    """
    Retrieve the current merchant's data.
    """
    pass


@router.get(
    "/me/api-key",
    response_model=MerchantBriefDataResponse,
    dependencies=[Depends(get_current_merchant_manager)],
)
def get_api_key(
    current_user_id: UUID = Depends(get_current_merchant_manager),
) -> str:
    """
    Retrieve the current merchant's API key.
    """
    pass
