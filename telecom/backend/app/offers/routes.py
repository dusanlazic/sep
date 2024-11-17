from uuid import UUID

from fastapi import APIRouter, Depends

from ..auth.dependencies import get_current_user
from . import service
from .schemas import OfferResponse, SubscriptionRequest, SubscriptionResponse

router = APIRouter(prefix="/offers", tags=["Offers"])


@router.get("/", response_model=list[OfferResponse])
def get_offers() -> list[OfferResponse]:
    """
    List all available offers.
    """
    pass


@router.get("/subscriptions", response_model=list[SubscriptionResponse])
def get_subscriptions(
    current_user_id: UUID = Depends(get_current_user),
) -> list[SubscriptionResponse]:
    """
    List all subscriptions for the current user.
    """
    pass


@router.post("/subscriptions", response_model=SubscriptionResponse)
def subscribe_to_offer(
    subscription_request: SubscriptionRequest,
    current_user_id: UUID = Depends(get_current_user),
) -> SubscriptionResponse:
    """
    Subscribe to an offer.
    """
    pass