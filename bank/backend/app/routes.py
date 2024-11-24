from urllib.parse import urlencode, urlunparse

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from .config import config
from .database import get_db
from .models import Merchant, Transaction, TransactionStatus
from .schemas import (
    PaymentInstructionsResponse,
    PaymentRequest,
    TransactionCreateRequest,
)

router = APIRouter()


@router.post(
    "/transactions", response_model=PaymentInstructionsResponse, tags=["PSP Core"]
)
def create_transaction(
    new_transaction: TransactionCreateRequest,
    db: Session = Depends(get_db),
):
    """
    Create a new transaction.
    """
    merchant = db.query(Merchant).filter_by(id=new_transaction.merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found.")

    if not merchant.password == new_transaction.merchant_password:
        raise HTTPException(status_code=401, detail="Invalid password.")

    transaction = Transaction(
        merchant_id=new_transaction.merchant_id,
        amount=new_transaction.amount,
        status=TransactionStatus.PENDING,
        success_url=new_transaction.success_url.unicode_string(),
        failure_url=new_transaction.failure_url.unicode_string(),
        error_url=new_transaction.error_url.unicode_string(),
        created_at=new_transaction.merchant_timestamp,
    )
    db.add(transaction)
    db.commit()

    payment_url = urlunparse(
        (
            "http",
            config.frontend_host,
            "/payment",
            "",
            urlencode({"payment_id": str(transaction.id)}),
            "",
        )
    )

    return PaymentInstructionsResponse(
        payment_id=str(transaction.id),
        payment_url=payment_url,
    )


@router.post(
    "/transactions/{transaction_id}/pay",
)
def pay_transaction(
    transaction_id: str,
    card_info: PaymentRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    """
    Pay for the transaction.
    """
    transaction = db.query(Transaction).filter_by(id=transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")

    payment_details_correct = True

    if not payment_details_correct:
        response.status_code = 400
        return {
            "error": "Payment details are incorrect.",
            "next_url": transaction.error_url,
        }
    else:
        transaction.status = TransactionStatus.COMPLETED
        db.commit()
        return {
            "details": "Payment successful.",
            "next_url": transaction.success_url,
        }
