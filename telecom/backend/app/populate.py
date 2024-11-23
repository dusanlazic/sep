from .database import get_db_session
from .offers.models import Offer


def create_offers():
    with get_db_session() as db:
        offer = db.query(Offer).filter(Offer.identifier == "net-only").first()
        if offer:
            print("Offers already exist.")
            return

        offer_1 = Offer(
            identifier="net-only",
            title="Net Only",
            description="Basic coaxial internet connection. Speeds up to 100Mbps download and 10Mbps upload. Enough for daily use.",
            price=350.0,
        )

        offer_2 = Offer(
            identifier="tv-only",
            title="TV Only",
            description="Basic TV Box connection. Get 120 channels including entertainment, sports, and more! HD channels are limited to a select few.",
            price=250.0,
        )

        offer_3 = Offer(
            identifier="data-only",
            title="Data Only",
            description="Basic data plan to fulfill your daily needs. 7GB per month, unlimited speed. Carry up to 10GB into the following month.",
            price=150.0,
        )

        offer_4 = Offer(
            identifier="net-plus-data",
            title="Net+Data",
            description="Stay online 24/7 with better internet and better data. 150Mbps download and 15Mbps upload, with 10GB per month data package.",
            price=420.0,
        )

        offer_5 = Offer(
            identifier="tv-plus-data",
            title="TV+Data",
            description="Online only when it's necessary, and that's okay! 150 HD channels with 10GB per month data package.",
            price=340.0,
        )

        offer_6 = Offer(
            identifier="full-suite",
            title="Full Suite",
            description="The best of everything. Top-of-the-line fibreoptic connection with 300Mbps download and 45Mbps upload. 15GB of data. 200 premium HD channels including a selection of 4k channels to provide the best viewing experience.",
            price=700.0,
        )

        db.add_all([offer_1, offer_2, offer_3, offer_4, offer_5, offer_6])
        db.commit()

    print("Offers created successfully.")
