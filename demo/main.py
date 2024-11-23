from urllib.parse import urlparse
import requests
import logging
import sys


logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s %(funcName)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Copy this from run.py output
TELECOM_WEB_APP = "http://telecom.172.19.0.20.nip.io/"
TELECOM_API = "http://api.telecom.172.19.0.20.nip.io/api/v1/"
PSP_FRONTEND = "http://psp.172.19.0.19.nip.io/"
PSP_PUBLIC_FACING_API = "http://api.psp.172.19.0.19.nip.io/api/v1/"
PSP_INTERNAL_API = "http://psp-core-backend:9000/"
PSP_CRYPTO_PAYMENT_PAGE = "http://crypto.psp.172.19.0.18.nip.io/"
PSP_CRYPTO_PUBLIC_FACING_API = "http://crypto.psp.172.19.0.18.nip.io/api/v1/"
PSP_CRYPTO_INTERNAL_API = "http://psp-crypto-handler-backend:9000/"
PSP_CARD_INTERNAL_API = "http://psp-card-handler-backend:9000/"


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

    response = requests.post(PSP_PUBLIC_FACING_API + "merchants/register", json=payload)
    logger.info(response.text)


def login_merchant(username: str) -> str:
    logger.info("Logging in merchant...")

    payload = {"username": username, "password": "securepassword123"}

    response = requests.post(PSP_PUBLIC_FACING_API + "merchants/login", json=payload)

    logger.info(response.text)

    access_token = response.cookies["access_token"]

    response = requests.get(
        PSP_PUBLIC_FACING_API + "merchants/me",
        cookies={"access_token": access_token},
    )

    logger.info(response.text)
    return access_token


def merchant_get_own_config(token: str):
    logger.info("Getting own configuration...")

    response = requests.get(
        PSP_PUBLIC_FACING_API + "payment-methods/config",
        cookies={"access_token": token},
    )

    logger.info("\n" + response.json()["yaml"])


def merchant_set_own_api_key(token: str):
    logger.info("Setting own API key...")

    env_file = "../telecom/backend/.env.example"

    response = requests.get(
        PSP_PUBLIC_FACING_API + "merchants/me",
        cookies={"access_token": token},
    )

    api_key: str = response.json()["api_key"]

    with open(env_file, "r") as file:
        lines = file.readlines()

    updated = False
    with open(env_file, "w") as file:
        for line in lines:
            if line.startswith("PSP_API_KEY="):
                file.write(f"PSP_API_KEY={api_key}\n")
                updated = True
            else:
                file.write(line)

        if not updated:
            file.write(f"PSP_API_KEY={api_key}\n")

    return api_key


def admin_list_payment_methods():
    logger.info("Listing payment methods...")

    response = requests.get(
        PSP_PUBLIC_FACING_API + "payment-methods",
        cookies={"access_token": "hey_its_admin"},
    )
    logger.info(response.json())


def admin_add_payment_method_bitcoin():
    logger.info("Adding bitcoin payment method...")

    parsed_url = urlparse(PSP_CRYPTO_INTERNAL_API)

    payload = {
        "host": parsed_url.hostname,
        "port": parsed_url.port,
        "name": "bitcoin",
    }

    response = requests.post(
        PSP_PUBLIC_FACING_API + "payment-methods",
        json=payload,
        cookies={"access_token": "hey_its_admin"},
    )

    logger.info(response.text)


def merchant_update_own_config(token: str):
    logger.info("Updating own configuration...")

    yaml = """
urls:
    success: https://example.com/success
    failure: https://example.com/failure
    error: https://example.com/error
    callback: https://example.com/callback

payment_methods:
    - name: bitcoin
      config:
        deposit_addresses:
          - "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
          - "1BoatSLRHtKNngkdXEeobR76b53LETtpyT"
          - "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy"
          - "bc1qw508d6qe40j0qxr3rplgpqq8gc4xtqf"
          - "3Ai1JZ8pdJb2ksieUV8FsxSNVJCpoPi8W6"
          - "1QLbGuc3WGCC9H7dmkVctgkM7vsm9ZZRJy"
          - "bc1qrp33g0q5c6qrchyqdcfgxv5hrpxxpu9"
          - "bc1qqqrrzpyrvlmj7y0wjkcqq5rw22zgstj"
          - "1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ"
          - "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkf"
          - "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo"
"""

    payload = {"yaml": yaml}

    response = requests.post(
        PSP_PUBLIC_FACING_API + "payment-methods/config",
        json=payload,
        cookies={"access_token": token},
    )

    logger.info(response.text)


def merchant_app_initiate_transaction(api_key: str):
    logger.info("Initiating transaction...")

    payload = {
        "amount": 10.0,
        "subject": "Payment for service",
        "description": "Payment for service A B C",
    }

    response = requests.post(
        PSP_PUBLIC_FACING_API + "transactions",
        json=payload,
        headers={"X-API-Key": api_key},
    )

    logger.info(response.text)


if __name__ == "__main__":
    merchant_username = "merchant5"

    register_merchant(merchant_username)
    token = login_merchant(merchant_username)
    merchant_get_own_config(token)
    api_key = merchant_set_own_api_key(token)

    admin_list_payment_methods()
    admin_add_payment_method_bitcoin()

    merchant_update_own_config(token)
    merchant_get_own_config(token)

    merchant_app_initiate_transaction(api_key)
