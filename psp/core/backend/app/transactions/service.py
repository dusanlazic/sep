from urllib.parse import urlencode, urlunparse

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..config import config
from ..merchants.models import Merchant
from .models import Transaction, TransactionStatus


def create_transaction(
    db: Session,
    merchant: Merchant,
    amount: float,
    subject: str,
    description: str,
) -> Transaction:
    new_transaction = Transaction(
        merchant_id=merchant.id,
        amount=amount,
        status=TransactionStatus.PENDING,
        subject=subject,
        description=description,
    )

    try:
        db.add(new_transaction)
        db.flush()
        return new_transaction
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Transaction creation failed.")


def generate_proceed_url(transaction_id: int) -> str:
    return urlunparse(
        (
            "http",
            config.frontend_host,
            "/payment",
            "",
            urlencode({"transaction_id": transaction_id}),
            "",
        )
    )


def get_transaction(db: Session, transaction_id: int) -> Transaction:
    transaction = db.query(Transaction).filter_by(id=transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")
    return transaction
