from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth.dependencies import get_current_user
from ..database import get_db
from . import service
from .schemas import (
    OfferResponse,
    PaymentInitiatedResponse,
    SubscriptionRequest,
    SubscriptionResponse,
)

router = APIRouter(prefix="/offers", tags=["Offers"])


@router.get("/", response_model=list[OfferResponse])
def get_offers(db: Annotated[Session, Depends(get_db)]) -> list[OfferResponse]:
    """
    List all available offers.
    """
    return service.get_offers(db)


@router.get("/subscriptions", response_model=list[SubscriptionResponse])
def get_subscriptions(
    db: Annotated[Session, Depends(get_db)],
    current_user_id: UUID = Depends(get_current_user),
) -> list[SubscriptionResponse]:
    """
    List all subscriptions for the current user.
    """
    return service.get_subscriptions(db, current_user_id)


@router.post("/subscriptions", response_model=PaymentInitiatedResponse)
def subscribe_to_offer(
    db: Annotated[Session, Depends(get_db)],
    subscription_request: SubscriptionRequest,
    current_user_id: UUID = Depends(get_current_user),
) -> PaymentInitiatedResponse:
    """
    Subscribe to an offer.
    """
    return service.subscribe_to_offer(db, subscription_request, current_user_id)
    
