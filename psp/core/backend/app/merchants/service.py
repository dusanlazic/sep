from secrets import token_hex

import jwt
from bcrypt import checkpw, gensalt, hashpw
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..config import config
from .models import Merchant
from .schemas import MerchantRegistrationRequest


def hash_password(password: str) -> str:
    """
    Hashes the password using bcrypt.
    """
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")


def register_merchant(
    db: Session, new_merchant: MerchantRegistrationRequest
) -> Merchant:
    """
    Registers a new merchant.
    """
    merchant = Merchant(
        username=new_merchant.username,
        password_hash=hash_password(new_merchant.password),
        title=new_merchant.title,
        api_key="psp_" + token_hex(20),
        configuration_json={
            "urls": {
                "success": new_merchant.payment_success_url.unicode_string(),
                "fail": new_merchant.payment_failure_url.unicode_string(),
                "error": new_merchant.payment_error_url.unicode_string(),
                "callback": new_merchant.payment_callback_url.unicode_string(),
            },
            "payment_methods": [],  # Initially no payment methods configured
        },
    )

    try:
        db.add(merchant)
        return merchant
    except IntegrityError:
        db.rollback()
        raise ValueError("Username already exists.")


def login_merchant(
    db: Session,
    username: str,
    password: str,
) -> str | None:
    """
    Validates the merchant's credentials and issues an access token.
    """
    merchant = db.query(Merchant).filter(Merchant.username == username).first()
    if not merchant or not checkpw(
        password.encode("utf-8"), merchant.password_hash.encode("utf-8")
    ):
        return None

    return jwt.encode(
        {"sub": str(merchant.id)},
        config.secret_key,
        algorithm="HS256",
    )


def get_merchant_by_id(db: Session, merchant_id: str) -> Merchant:
    """
    Retrieves the merchant by ID.
    """
    return db.query(Merchant).get(merchant_id)
