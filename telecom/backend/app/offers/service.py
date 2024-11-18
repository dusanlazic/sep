from sqlalchemy.orm import Session

from .models import *


def get_offers(db: Session) -> list[Offer]:
    offers = db.query(Offer).all()
    return offers

def get_subscriptions(db: Session, user_id: UUID) -> list[Subscription]:
    user = db.query(User).filter(User.id == user_id).first()
    return user.subscriptions
