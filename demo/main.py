import requests
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s %(funcName)s - %(message)s",
)

logger = logging.getLogger(__name__)

TELECOM_API = "http://api.telecom.172.19.0.19.nip.io/api/v1/"
PSP_CORE_PUBLIC_FACING_API = "http://api.psp.172.19.0.20.nip.io/api/v1/"
PSP_CRYPTO_PUBLIC_FACING_API = "http://crypto.psp.172.19.0.18.nip.io/api/v1/"
PSP_CARD_PUBLIC_FACING_API = "http://card.psp.172.19.0.16.nip.io/api/v1/"


def register_merchant(username: str):
    logger.info("Registering merchant...")

    payload = {
        "username": username,
        "password": "securepassword123",
        "title": "Random Merchant 3",
        "payment_success_url": "https://example.com/success",
        "payment_failure_url": "https://example.com/failure",
        "payment_error_url": "https://example.com/error",
        "payment_callback_url": "https://example.com/callback",
    }

    response = requests.post(
        PSP_CORE_PUBLIC_FACING_API + "merchants/register", json=payload
    )
    logger.info(response.text)


def login_merchant(username: str):
    logger.info("Logging in merchant...")

    payload = {"username": username, "password": "securepassword123"}

    response = requests.post(
        PSP_CORE_PUBLIC_FACING_API + "merchants/login", json=payload
    )

    logger.info(response.text)

    access_token = response.cookies["access_token"]

    response = requests.get(
        PSP_CORE_PUBLIC_FACING_API + "merchants/me",
        cookies={"access_token": access_token},
    )

    logger.info(response.text)


if __name__ == "__main__":
    merchant_username = "merchant5"

    register_merchant(merchant_username)
    login_merchant(merchant_username)
