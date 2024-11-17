from sqlalchemy.orm import Session

from .models import *
from .schemas import OfferResponse, SubscriptionResponse


def get_offers(db: Session) -> list[OfferResponse]:
    offers = db.query(Offer).all()
    return [OfferResponse(identifier=o.identifier, title=o.title, description=o.description, price=o.price) for o in offers]

def get_subscriptions(db: Session, user_id: UUID) -> list[SubscriptionResponse]:
    user = db.query(User).filter(User.id == user_id).first()
    return [SubscriptionResponse(offer_identifier=s.identifier,) for s in user.subscriptions]
