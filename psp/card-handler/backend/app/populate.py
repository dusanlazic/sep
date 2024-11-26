from .database import get_db_session
from .models import Bank


def create_banks():
    with get_db_session() as db:
        bank = db.query(Bank).filter(Bank.name == "unicredit").first()
        if bank:
            print("Banks already exist.")
            return

        bank_api_urls = []
        with open(".env") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("POPULATE_"):
                    bank_api_urls.append(line.split("=")[1].strip())

        bank_1 = Bank(
            name="unicredit",
            api_base_url=bank_api_urls[0],
        )

        bank_2 = Bank(
            name="erste",
            api_base_url=bank_api_urls[1],
        )

        db.add_all([bank_1, bank_2])
        db.commit()

    print("Merchants created successfully.")
