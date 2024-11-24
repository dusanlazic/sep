from .database import get_db_session
from .models import Merchant


def create_merchants():
    with get_db_session() as db:
        merchant = (
            db.query(Merchant)
            .filter(Merchant.id == "bc26c127-8670-4814-9e13-0e120d838e80")
            .first()
        )
        if merchant:
            print("Merchants already exist.")
            return
            # bc26c127-8670-4814-9e13-0e120d838e80
            # 8Nl574GES1jmQjUvBqpDBhuhOLvU5QZ

        merchant = Merchant(
            id="bc26c127-8670-4814-9e13-0e120d838e80",
            password="8Nl574GES1jmQjUvBqpDBhuhOLvU5QZ",
        )

        db.add_all([merchant])
        db.commit()

    print("Merchants created successfully.")
