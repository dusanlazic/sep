from .database import get_db_session
from .offers.models import Offer


def create_offers():
    with get_db_session() as db:
        offer = db.query(Offer).filter(Offer.identifier == "basic").first()
        if offer:
            print("Offers already exist.")
            return

        offer_1 = Offer(
            identifier="basic",
            title="Basic Subscription",
            description="Basic subscription with limited features.",
            price=500.0,
        )

        offer_2 = Offer(
            identifier="premium",
            title="Premium Subscription",
            description="Premium subscription with all features.",
            price=1000.0,
        )

        offer_3 = Offer(
            identifier="enterprise",
            title="Enterprise Subscription",
            description="Enterprise subscription with all features and priority support.",
            price=2000.0,
        )

        db.add_all([offer_1, offer_2, offer_3])
        db.commit()

    print("Offers created successfully.")
