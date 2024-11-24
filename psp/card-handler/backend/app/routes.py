from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .config import config
from .database import get_db
from .models import Merchant, Transaction, TransactionStatus
from .schemas import (
    ConfigureMerchantRequest,
    HandlerConfigurationSchemaResponse,
    MerchantConfiguration,
    TransactionProceedRequest,
    TransactionProceedResponse,
)

router = APIRouter()


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
        title="Pay With Card",
        configuration_schema=MerchantConfiguration.model_json_schema(),
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
        bank_merchant_id=merchant_create_request.configuration.bank_merchant_id,
        bank_merchant_password=merchant_create_request.configuration.bank_merchant_password,
    )
    db.add(new_merchant)
    db.commit()

    return {"message": "Merchant added successfully."}


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
    Provide handler information to proceed with the transaction and
    receive PAYMENT_URL to redirect the customers to.
    """
    merchant = (
        db.query(Merchant)
        .filter_by(psp_id=str(transaction_proceed_request.merchant_id))
        .first()
    )

    try:
        payload = {
            "merchant_id": merchant.bank_merchant_id,
            "merchant_password": merchant.bank_merchant_password,
            "amount": transaction_proceed_request.amount,
            "merchant_order_id": str(transaction_proceed_request.id),
            "merchant_timestamp": datetime.now().astimezone().isoformat(),
            "success_url": transaction_proceed_request.next_urls.success.unicode_string(),
            "failure_url": transaction_proceed_request.next_urls.failure.unicode_string(),
            "error_url": transaction_proceed_request.next_urls.error.unicode_string(),
        }

        print(payload)

        bank_response = requests.post(
            config.bank_api_url + "transactions",
            json=payload,
        )
        bank_response.raise_for_status()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="There was an error in Card Payment Handler when creating the transaction: "
            + str(e),
        )

    bank_payment_id: str = bank_response.json()["payment_id"]

    new_transaction = Transaction(
        psp_id=transaction_proceed_request.id,
        merchant_id=merchant.id,
        bank_payment_id=bank_payment_id,
        amount=transaction_proceed_request.amount,
        status=TransactionStatus.PENDING,
    )
    try:
        db.add(new_transaction)
        db.flush()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="There was an error when creating the transaction: " + str(e),
        )

    payment_url: str = bank_response.json()["payment_url"]

    return TransactionProceedResponse(payment_url=payment_url)
