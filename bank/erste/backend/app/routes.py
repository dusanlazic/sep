import uuid
from datetime import datetime
from urllib.parse import urlencode, urlunparse
from zoneinfo import ZoneInfo

import requests
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from .config import config
from .database import get_db
from .models import Account, Merchant, Transaction, TransactionStatus
from .schemas import (
    PaymentInstructionsResponse,
    PaymentRequest,
    PaymentResultResponse,
    PccPaymentRequest,
    PccPaymentResponse,
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
    response_model=PaymentResultResponse,
    tags=["Customer"],
)
def pay_transaction(
    transaction_id: str,
    card_info: PaymentRequest,
    db: Session = Depends(get_db),
):
    """
    Pay for the transaction.
    """
    transaction = db.query(Transaction).filter_by(id=transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")

    pcc_response = requests.post(
        f"{config.pcc_api_base_url}/request-payment",
        json={
            "amount": transaction.amount,
            "card_number": card_info.card_number,
            "card_expiration": card_info.card_expiration,
            "card_cvv": card_info.card_cvv,
            "card_holder": card_info.card_holder,
            "acquirer_order_id": str(uuid.uuid4()),
            "acquirer_timestamp": datetime.now().astimezone().isoformat(),
        },
    )

    if pcc_response.json()["status"] == "success":
        requests.put(
            f"{config.psp_api_base_url}/transactions/{transaction_id}/status",
            json={"status": "completed"},
        )

        return PaymentResultResponse(
            detail="Payment successful.",
            next_url=transaction.success_url,
        )
    else:
        requests.put(
            f"{config.psp_api_base_url}/transactions/{transaction_id}/status",
            json={"status": "failed"},
        )

        return PaymentResultResponse(
            detail=pcc_response.json()["msg"],
            next_url=transaction.failure_url,
        )


@router.post(
    "/pcc/request-payment",
    response_model=PccPaymentResponse,
    tags=["PCC"],
)
def process_pcc_request(
    payment_request: PccPaymentRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    account = (
        db.query(Account)
        .filter_by(
            card_number=payment_request.card_number.replace(" ", ""),
            expiration_date=payment_request.card_expiration,
            cvv=payment_request.card_cvv,
            card_holder_name=payment_request.card_holder,
        )
        .first()
    )

    issuer_order_id = str(uuid.uuid4())
    issuer_timestamp = datetime.now().astimezone().isoformat()

    if not account:
        response.status_code = 400
        return PccPaymentResponse(
            acquirer_order_id=payment_request.acquirer_order_id,
            acquirer_timestamp=payment_request.acquirer_timestamp,
            issuer_order_id=issuer_order_id,
            issuer_timestamp=issuer_timestamp,
            status="error",
            msg="Payment details invalid.",
        )

    if account.balance < payment_request.amount:
        response.status_code = 400
        return PccPaymentResponse(
            acquirer_order_id=payment_request.acquirer_order_id,
            acquirer_timestamp=payment_request.acquirer_timestamp,
            issuer_order_id=issuer_order_id,
            issuer_timestamp=issuer_timestamp,
            status="error",
            msg="Insufficient funds.",
        )

    account.balance -= payment_request.amount
    db.commit()

    return PccPaymentResponse(
        acquirer_order_id=payment_request.acquirer_order_id,
        acquirer_timestamp=payment_request.acquirer_timestamp,
        issuer_order_id=issuer_order_id,
        issuer_timestamp=issuer_timestamp,
        status="success",
        msg="Payment successful.",
    )
