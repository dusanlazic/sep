from .database import get_db_session
from .models import Account, Merchant


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

        merchant = Merchant(
            id="bc26c127-8670-4814-9e13-0e120d838e80",
            password="8Nl574GES1jmQjUvBqpDBhuhOLvU5QZ",
        )

        db.add_all([merchant])
        db.commit()

    print("Merchants created successfully.")


def create_accounts():
    with get_db_session() as db:
        account = (
            db.query(Account).filter(Account.card_number == "4381131213121312").first()
        )
        if account:
            print("Accounts already exist.")
            return

        account_1 = Account(
            card_number="4381131213121312",
            card_holder_name="John Doe",
            expiration_date="01/26",
            cvv="123",
            balance=2000,
        )

        account_2 = Account(
            card_number="4381133713371337",
            card_holder_name="Jane Doe",
            expiration_date="01/26",
            cvv="123",
            balance=50,
        )

        db.add_all([account_1, account_2])
