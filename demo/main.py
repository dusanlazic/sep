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
PSP_FRONTEND = "http://psp.172.19.0.18.nip.io/"
PSP_PUBLIC_FACING_API = "http://api.psp.172.19.0.18.nip.io/api/v1/"
PSP_INTERNAL_API = "http://psp-core-backend:9000/"
PSP_CRYPTO_PAYMENT_PAGE = "http://crypto.psp.172.19.0.19.nip.io/"
PSP_CRYPTO_PUBLIC_FACING_API = "http://crypto.psp.172.19.0.19.nip.io/api/v1/"
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

    logger.info(response.json())


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
          - "1L8meBQvKaGWZAHYMYDbrsWN2KpKh9dmxE"
          - "1KoZ4BZmzFdW89p7A6EfCX8pSYH4mgSWWv"
          - "bc1qaaygfhkrlwyzhgr68c25mr7nwyl9sw8"
          - "3Cbq7aT1tY8kMxWLbitaG7yT6bPbKChq64"
          - "3MynU1hEoA4VXtPofMzFR9GxVFTpPa2GLo"
          - "1Afmr1cZ7cVCPLxYGFboE4xUyThExZBYXG"
          - "bc1qypd9hf7dj7zhzksjfyc0gkqzue5wfqy"
          - "1BKcCHpkMi6PF9V62FbA2J4poCNnJHgr3Y"
          - "3HKNt5aq7Gdeiqm12m1hRGqsddEtk4HrMt"
          - "1Fd3Aj9T3tbZZphUtebcKCB3X9VJVQTe6j"
          - "1LQPoG4yS9QymXBc89zkgy5KDRpTfY7G5L"
          - "3QJmnhTMuGV3yy2vRGVmXMQmo1GhaPNXLy"
          - "1F1miYFQWTzdLiCBxtHHnHozP7ziv45C2z"
          - "bc1qvq3vsnvw4k62r7hhg9w9p5x6vxru9cc"
          - "1Nd5XSGGhZtmdF1wgFoPNw2ch8YH1ddPQS"
          - "3JAGAYSkKKMVexYTGv43zTAXRxF1GvSMq3"
          - "1PZDkbU5Yok6cEKGn57Q4BniDfYHPscDeT"
          - "1Hg2PmP1L6PLxn4mPQrfX1EQPBvAoUPZKn"
          - "3LXY1cS3L6VxTYzPQbvRpoQvYE5KNzP4Mw"
"""

    payload = {"yaml": yaml}

    response = requests.post(
        PSP_PUBLIC_FACING_API + "payment-methods/config",
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
