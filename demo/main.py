import requests
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s %(funcName)s - %(message)s",
)

logger = logging.getLogger(__name__)

TELECOM_API = "http://api.telecom.172.19.0.20.nip.io/api/v1/"
PSP_CORE_PUBLIC_FACING_API = "http://api.psp.172.19.0.18.nip.io/api/v1/"
PSP_CRYPTO_PUBLIC_FACING_API = "http://crypto.psp.172.19.0.19.nip.io/api/v1/"
PSP_CARD_PUBLIC_FACING_API = "http://card.psp.172.19.0.12.nip.io/api/v1/"

PSP_CRYPTO_INTERNAL_HOST = "psp-crypto-handler-backend"
PSP_CRYPTO_INTERNAL_PORT = 9000


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


def login_merchant(username: str) -> str:
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
    return access_token


def merchant_get_own_config(token: str):
    logger.info("Getting own configuration...")

    response = requests.get(
        PSP_CORE_PUBLIC_FACING_API + "payment-methods/config",
        cookies={"access_token": token},
    )

    logger.info("\n" + response.json()["yaml"])


def admin_list_payment_methods():
    logger.info("Listing payment methods...")

    response = requests.get(
        PSP_CORE_PUBLIC_FACING_API + "payment-methods",
        cookies={"access_token": "hey_its_admin"},
    )
    logger.info(response.json())


def admin_add_payment_method_bitcoin():
    logger.info("Adding bitcoin payment method...")

    payload = {
        "host": PSP_CRYPTO_INTERNAL_HOST,
        "port": PSP_CRYPTO_INTERNAL_PORT,
        "name": "bitcoin",
    }

    response = requests.post(
        PSP_CORE_PUBLIC_FACING_API + "payment-methods",
        json=payload,
        cookies={"access_token": "hey_its_admin"},
    )

    logger.info(response.json())


def merchant_update_own_config(token: str):
    logger.info("Updating own configuration...")

    yaml = """
urls:
    success: https://example.com/success
    fail: https://example.com/failure
    error: https://example.com/error
    callback: https://example.com/callback

payment_methods:
    - name: bitcoin
      config:
        deposit_addresses:
          - "address1"
          - "address2"
          - "address3"
          - "address4"
"""

    payload = {"yaml": yaml}

    response = requests.post(
        PSP_CORE_PUBLIC_FACING_API + "payment-methods/config",
        json=payload,
        cookies={"access_token": token},
    )

    logger.info(response.text)


if __name__ == "__main__":
    merchant_username = "merchant5"

    register_merchant(merchant_username)
    token = login_merchant(merchant_username)
    merchant_get_own_config(token)
    admin_list_payment_methods()
    admin_add_payment_method_bitcoin()
    merchant_update_own_config(token)
    merchant_get_own_config(token)
