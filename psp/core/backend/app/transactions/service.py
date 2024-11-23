from urllib.parse import urlencode, urlunparse
from uuid import UUID

import requests
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..config import config
from ..merchants.models import Merchant
from ..methods.models import PaymentMethod
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


def generate_proceed_url(transaction_id: UUID) -> str:
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


def get_transaction(db: Session, transaction_id: UUID) -> Transaction:
    transaction = db.query(Transaction).filter_by(id=transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")
    return transaction


def get_payment_url(db: Session, transaction_id: UUID, payment_method_name: str) -> str:
    transaction = get_transaction(db, transaction_id)
    if (
        payment_method_name
        not in transaction.merchant.get_supported_payment_method_names()
    ):
        raise HTTPException(status_code=400, detail="Payment method not supported.")

    payment_method = db.query(PaymentMethod).filter_by(name=payment_method_name).first()
    if not payment_method:
        raise HTTPException(status_code=404, detail="Payment method not supported.")

    try:
        response = requests.post(
            f"http://{payment_method.host}:{payment_method.port}/transactions",
            json={
                "id": str(transaction.id),
                "merchant_id": str(transaction.merchant_id),
                "amount": transaction.amount,
                "next_urls": {
                    "success": transaction.merchant.get_urls()["success"],
                    "failure": transaction.merchant.get_urls()["failure"],
                    "error": transaction.merchant.get_urls()["error"],
                },
            },
        )
        response.raise_for_status()
    except Exception:
        raise HTTPException(
            status_code=500, detail="Payment failed when calling the handler."
        )

    return response.json()["payment_url"]


def update_transaction_status(db: Session, transaction_id: UUID, status: str) -> None:
    transaction = get_transaction(db, transaction_id)
    transaction.status = status
    try:
        db.flush()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Transaction status update failed.")

    try:
        requests.post(
            f"http://{transaction.merchant.get_urls()['callback']}",
            json={
                "transaction_id": str(transaction_id),
                "status": status,
            },
        )
    except Exception:
        pass
