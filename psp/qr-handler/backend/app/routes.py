import uuid
import time
import base64
import requests

from urllib.parse import urlencode, urlunparse
from .config import config
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from .schemas import (
    TransactionDetailsResponse,
    TransactionProceedRequest,
    TransactionProceedResponse,
    ConfigureMerchantRequest,
    MerchantConfiguration,
    HandlerConfigurationSchemaResponse,
)
from .database import get_db
from .models import Merchant, Transaction, TransactionStatus


router = APIRouter()


@router.post(
    "/transactions",
    response_model=TransactionProceedResponse,
    tags=["PSP Core"],
)
def proceed_with_transaction(
    transaction_proceed_request: TransactionProceedRequest,
    db: Session = Depends(get_db),
):
    """
    Initiate a QR transaction and
    receive string to be encoded into a QR code.
    """
    # Find the merchant by merchant_id (psp_id in our DB)
    merchant = (
        db.query(Merchant)
        .filter_by(psp_id=str(transaction_proceed_request.merchant_id))
        .first()
    )
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found.")

    new_txn = Transaction(
        psp_id=str(transaction_proceed_request.id),
        merchant_id=merchant.id,
        amount=transaction_proceed_request.amount,
        status=TransactionStatus.PENDING,
        success_url=str(transaction_proceed_request.next_urls.success),
        failure_url=str(transaction_proceed_request.next_urls.failure),
        error_url=str(transaction_proceed_request.next_urls.error),
    )
    try:
        db.add(new_txn)
        db.commit()         # write + release row‑level locks
    except Exception as e:
        db.rollback()
        raise HTTPException(
            500, f"There was an error when storing the transaction: {e!s}"
        )
    
    ips_data = f'K:PR|V:01|C:1|R:{merchant.merchant_account_number}|N:{merchant.merchant_name}|I:RSD{str(transaction_proceed_request.amount).replace(".", ",")}|SF:289|S:Service Payment'

    payment_url = urlunparse(
        (
            "http",
            config.frontend_host,
            "/payment",
            "",
            urlencode({"data": ips_data}),
            "",
        )
    )

    return TransactionProceedResponse(payment_url=payment_url)


@router.get(
    "/transactions/{transaction_id}",
    response_model=TransactionDetailsResponse,
    tags=["PSP Core"],
)
def get_transaction(transaction_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Get information about the transaction. Used by the handler frontend to
    display the amount and QR code to the customer, and to check the status
    of the transaction in order to redirect the customer to the correct page.

    This endpoint can be called repeatably to check the status of the transaction.
    """
    transaction = db.query(Transaction).filter_by(id=transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")

    return TransactionDetailsResponse(
        amount=transaction.amount,
        urls={
            "success": transaction.success_url,
            "failure": transaction.failure_url,
            "error": transaction.error_url,
        },
        status=transaction.status.value,
    )


@router.post("/merchants", tags=["PSP Core"])
def add_new_merchant(
    merchant_create_request: ConfigureMerchantRequest,
    db: Session = Depends(get_db),
):
    """
    Add a new merchant to the handler and configure it.
    """
    merchant = (
        db.query(Merchant)
        .filter_by(psp_id=str(merchant_create_request.merchant_id))
        .first()
    )
    if merchant:
        raise HTTPException(status_code=409, detail="Merchant already exists.")

    new_merchant = Merchant(
        psp_id=merchant_create_request.merchant_id,
        merchant_name=merchant_create_request.configuration.merchant_name,
        merchant_account_number=str(merchant_create_request.configuration.merchant_account_number),
    )
    db.add(new_merchant)
    db.commit()

    return {"message": "Merchant added successfully."}


@router.get(
    "/schema",
    response_model=HandlerConfigurationSchemaResponse,
    tags=["PSP Core"],
)
def get_handler_configuration_schema():
    """
    Get information that describes the handler and how merchants
    should configure it.
    """
    return HandlerConfigurationSchemaResponse(
        title="Pay With QR",
        configuration_schema=MerchantConfiguration.model_json_schema(),
    )
