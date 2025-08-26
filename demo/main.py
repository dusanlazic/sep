import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse
from rich import print_json
import requests
import logging
import sys

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s %(funcName)s - %(message)s",
)

logger = logging.getLogger(__name__)

TELECOM_FRONTEND = os.getenv("TELECOM_FRONTEND")
TELECOM_API = os.getenv("TELECOM_API")
PSP_FRONTEND = os.getenv("PSP_FRONTEND")
PSP_PUBLIC_FACING_API = os.getenv("PSP_PUBLIC_FACING_API")
PSP_INTERNAL_API = os.getenv("PSP_INTERNAL_API")
PSP_CRYPTO_PAYMENT_PAGE = os.getenv("PSP_CRYPTO_PAYMENT_PAGE")
PSP_CRYPTO_PUBLIC_FACING_API = os.getenv("PSP_CRYPTO_PUBLIC_FACING_API")
PSP_CRYPTO_INTERNAL_API = os.getenv("PSP_CRYPTO_INTERNAL_API")
PSP_CARD_INTERNAL_API = os.getenv("PSP_CARD_INTERNAL_API")
PSP_PAYPAL_INTERNAL_API = os.getenv("PSP_PAYPAL_INTERNAL_API")
PSP_QR_INTERNAL_API = os.getenv("PSP_QR_INTERNAL_API")
BANK_PAYMENT_PAGE = os.getenv("BANK_PAYMENT_PAGE")
BANK_API = os.getenv("BANK_API")


def register_merchant(username: str):
    logger.info("Registering merchant...")

    payload = {
        "username": username,
        "password": "securepassword123",
        "title": "Random Merchant 3",
        "payment_success_url": f"{TELECOM_FRONTEND}payments/success",
        "payment_failure_url": f"{TELECOM_FRONTEND}payments/failure",
        "payment_error_url": f"{TELECOM_FRONTEND}payments/error",
        "payment_callback_url": f"{TELECOM_API}psp/callback",
    }

    response = requests.post(PSP_PUBLIC_FACING_API + "merchants/register", json=payload)
    print_json(data=response.json())


def login_merchant(username: str) -> str:
    logger.info("Logging in merchant...")

    payload = {"username": username, "password": "securepassword123"}

    response = requests.post(PSP_PUBLIC_FACING_API + "merchants/login", json=payload)

    print_json(data=response.json())

    access_token = response.cookies["access_token"]

    response = requests.get(
        PSP_PUBLIC_FACING_API + "merchants/me",
        cookies={"access_token": access_token},
    )

    print_json(data=response.json())
    return access_token


def merchant_get_own_config(token: str):
    logger.info("Getting own configuration...")

    response = requests.get(
        PSP_PUBLIC_FACING_API + "payment-methods/config",
        cookies={"access_token": token},
    )

    print_json(data=response.json())
    print("\n" + response.json()["yaml"])


def merchant_set_own_api_key(token: str):
    logger.info("Setting own API key...")

    env_file = "../telecom/backend/.env"

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

    Path("../telecom/backend/app/main.py").touch()

    return api_key


def admin_list_payment_methods():
    logger.info("Listing payment methods...")

    response = requests.get(
        PSP_PUBLIC_FACING_API + "payment-methods",
        cookies={"access_token": "hey_its_admin"},
    )
    print_json(data=response.json())


def admin_add_payment_method_bitcoin():
    logger.info("Adding bitcoin payment method...")

    parsed_url = urlparse(PSP_CRYPTO_INTERNAL_API)

    payload = {
        "name": "bitcoin",
        "service_name": parsed_url.hostname,
    }

    response = requests.post(
        PSP_PUBLIC_FACING_API + "payment-methods",
        json=payload,
        cookies={"access_token": "hey_its_admin"},
    )

    print_json(data=response.json())


def admin_add_payment_method_card():
    logger.info("Adding card payment method...")

    parsed_url = urlparse(PSP_CARD_INTERNAL_API)

    payload = {
        "name": "card",
        "service_name": parsed_url.hostname,
    }

    response = requests.post(
        PSP_PUBLIC_FACING_API + "payment-methods",
        json=payload,
        cookies={"access_token": "hey_its_admin"},
    )

    print_json(data=response.json())


def admin_add_payment_method_paypal():
    logger.info("Adding paypal payment method...")

    parsed_url = urlparse(PSP_PAYPAL_INTERNAL_API)

    payload = {
        "name": "paypal",
        "service_name": parsed_url.hostname,
    }

    response = requests.post(
        PSP_PUBLIC_FACING_API + "payment-methods",
        json=payload,
        cookies={"access_token": "hey_its_admin"},
    )

    print_json(data=response.json())


def admin_add_payment_method_qr():
    logger.info("Adding qr payment method...")

    parsed_url = urlparse(PSP_QR_INTERNAL_API)

    payload = {
        "host": parsed_url.hostname,
        "port": parsed_url.port,
        "name": "qr",
    }

    response = requests.post(
        PSP_PUBLIC_FACING_API + "payment-methods",
        json=payload,
        cookies={"access_token": "hey_its_admin"},
    )

    print_json(data=response.json())


def merchant_update_own_config(token: str):
    logger.info("Updating own configuration...")

    yaml = f"""
urls:
    success: {TELECOM_FRONTEND}payments/success
    failure: {TELECOM_FRONTEND}payments/failure
    error: {TELECOM_FRONTEND}payments/error
    callback: {TELECOM_API}psp/callback

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

    - name: card
      config:
        bank_name: unicredit
        bank_merchant_id: bc26c127-8670-4814-9e13-0e120d838e80
        bank_merchant_password: 8Nl574GES1jmQjUvBqpDBhuhOLvU5QZ

    - name: paypal
      config:
        paypal_merchant_email: sb-kwmoi32116156@business.example.com

    - name: qr
      config:
        merchant_name: Telekom Srbija
        merchant_account_number: 845000000040484987
"""

    payload = {"yaml": yaml}

    response = requests.post(
        PSP_PUBLIC_FACING_API + "payment-methods/config",
        json=payload,
        cookies={"access_token": token},
    )

    print_json(data=response.json())


def merchant_app_initiate_transaction(api_key: str) -> str:
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

    print_json(data=response.json())

    return response.json()["transaction_id"]


def customer_gets_transaction_information(transaction_id: str):
    logger.info("Getting transaction information...")
    response = requests.get(PSP_PUBLIC_FACING_API + f"transactions/{transaction_id}")
    print_json(data=response.json())


def customer_proceeds_with_transaction(transaction_id: str, payment_method: str) -> str:
    logger.info("Proceeding with transaction...")

    payload = {"payment_method_name": payment_method}

    response = requests.post(
        PSP_PUBLIC_FACING_API + f"transactions/{transaction_id}/proceed",
        json=payload,
    )

    print_json(data=response.json())
    return response.json()["payment_url"]


def customer_gets_transaction_information_from_bitcoin_handler(transaction_id: str):
    logger.info("Getting transaction information from bitcoin handler API...")

    response = requests.get(
        PSP_CRYPTO_PUBLIC_FACING_API + f"transactions/{transaction_id}"
    )

    print_json(data=response.json())


if __name__ == "__main__":
    merchant_username = "merchant5"

    # Register a new merchant
    register_merchant(merchant_username)
    token = login_merchant(merchant_username)
    merchant_get_own_config(token)
    api_key = merchant_set_own_api_key(token)

    # Adding payment methods
    admin_list_payment_methods()
    admin_add_payment_method_bitcoin()
    admin_add_payment_method_card()
    admin_add_payment_method_paypal()
    admin_add_payment_method_qr()
    admin_list_payment_methods()

    # Configure new merchant
    merchant_get_own_config(token)
    merchant_update_own_config(token)
    merchant_get_own_config(token)

    # replace this with the customer that initiates transaction on merchant app
    exit()
    transaction_id = merchant_app_initiate_transaction(api_key)

    customer_gets_transaction_information(transaction_id)

    # bitcoin payment
    # bitcoin_payment_url = customer_proceeds_with_transaction(transaction_id, "bitcoin")
    # bitcoin_transaction_id = bitcoin_payment_url.split("=")[-1]

    # customer_gets_transaction_information_from_bitcoin_handler(bitcoin_transaction_id)

    # card payment
    card_payment_url = customer_proceeds_with_transaction(transaction_id, "card")
    print(card_payment_url)
