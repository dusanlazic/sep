from datetime import datetime, timedelta
from uuid import uuid4

import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..config import config
from ..transactions.models import Transaction, TransactionStatus
from .models import *
from .schemas import (
    PaymentInitiatedResponse,
    SubscriptionRequest,
)


def get_offers(db: Session) -> list[Offer]:
    offers = db.query(Offer).all()
    return offers


def get_subscriptions(db: Session, user_id: UUID) -> list[Subscription]:
    user = db.query(User).filter(User.id == user_id).first()
    return user.subscriptions


def subscribe_to_offer(
    db: Session, subscription_request: SubscriptionRequest, user_id: UUID
) -> list[Subscription]:
    active_subscription = (
        db.query(Subscription)
        .filter(
            Subscription.user_id == user_id,
            Subscription.end_date > datetime.now(),
        )
        .first()
    )

    if active_subscription:
        raise HTTPException(
            status_code=400,
            detail="User already has an active subscription for this offer.",
        )

    start_date = datetime.now()
    end_date = start_date + timedelta(days=subscription_request.duration_in_years * 365)

    offer = (
        db.query(Offer)
        .filter(Offer.identifier == subscription_request.offer_identifier)
        .first()
    )

    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found.")

    transaction_payload = {
        "amount": offer.price * subscription_request.duration_in_years,
        "subject": offer.title,
        "description": offer.description,
    }

    try:
        response = requests.post(
            f"{config.psp_api_base_url}/transactions",
            json=transaction_payload,
            headers={"X-API-Key": config.psp_api_key},
        )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to initialise payment.")
    except Exception as e:
        print(f"Error communicating with PSP: {e}")
        raise HTTPException(status_code=500, detail="Failed to initialise payment.")

    payment_data = response.json()
    payment_url = payment_data.get("proceed_url")
    psp_order_id = payment_data.get("transaction_id")

    if not payment_url or not psp_order_id:
        raise HTTPException(status_code=500, detail="Failed to initialise payment.")

    subscription_id = uuid4()
    subscription = Subscription(
        id=subscription_id,
        user_id=user_id,
        offer_id=offer.id,
        start_date=start_date,
        end_date=end_date,
        duration_in_years=subscription_request.duration_in_years,
        auto_renew=subscription_request.auto_renew,
    )
    db.add(subscription)

    transaction = Transaction(
        psp_order_id=psp_order_id,
        subscription_id=subscription_id,
        amount=offer.price * subscription_request.duration_in_years,
        status=TransactionStatus.PENDING,
        created_at=datetime.now(),
    )
    db.add(transaction)
    db.commit()

    return PaymentInitiatedResponse(payment_url=payment_url)
