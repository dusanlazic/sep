import requests
from fastapi import APIRouter

from .models import Bank
from .schemas import PaymentRequest

router = APIRouter()


banks = [
    Bank(
        api_base_url="http://unicredit-bank-backend:9000/",
        bank_identification_number="438131",
    ),
    Bank(
        api_base_url="http://erste-bank-backend:9000/",
        bank_identification_number="402636",
    ),
]


def get_bank_based_on_card_number(card_number: str) -> Bank | None:
    card_number = card_number.replace(" ", "")

    for bank in banks:
        if card_number.startswith(bank.bank_identification_number):
            return bank
    return None


@router.post("/request-payment")
def request_payment(payment_request: PaymentRequest):
    # TODO: evidentiraj zahtev, proveri zahtev

    issuer_bank = get_bank_based_on_card_number(payment_request.card_number)
    issuer_bank_response = requests.post(
        f"{issuer_bank.api_base_url}/pcc/request-payment",
        json=payment_request.model_dump(mode="json"),
    )

    print("ISSUER BANK RESPONSE")
    print(issuer_bank_response.text)

    # vrati odgovor banci prodavca
    return issuer_bank_response.json()
