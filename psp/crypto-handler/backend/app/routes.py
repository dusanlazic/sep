import uuid
from urllib.parse import urlencode, urlunparse

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .config import config
from .database import get_db
from .models import DepositAddress, Merchant, Transaction, TransactionStatus
from .schemas import (
    ConfigureMerchantRequest,
    HandlerConfigurationSchemaResponse,
    MerchantConfiguration,
    TransactionDetailsResponse,
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
        title="Pay With Bitcoin",
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
        deposit_addresses=[
            DepositAddress(address=address)
            for address in merchant_create_request.configuration.deposit_addresses
        ],
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

    free_deposit_address = (
        db.query(DepositAddress).filter_by(used=False, merchant_id=merchant.id).first()
    )

    new_transaction = Transaction(
        psp_id=transaction_proceed_request.id,
        merchant_id=merchant.id,
        deposit_address_id=free_deposit_address.id,
        amount=transaction_proceed_request.amount,
        status=TransactionStatus.PENDING,
        success_url=transaction_proceed_request.next_urls.success.unicode_string(),
        failure_url=transaction_proceed_request.next_urls.failure.unicode_string(),
        error_url=transaction_proceed_request.next_urls.error.unicode_string(),
    )
    try:
        db.add(new_transaction)
        free_deposit_address.used = True
        db.flush()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="There was an error when creating the transaction: " + str(e),
        )

    payment_url = urlunparse(
        (
            "http",
            config.frontend_host,
            "/payment",
            "",
            urlencode({"id": new_transaction.id}),
            "",
        )
    )

    return TransactionProceedResponse(payment_url=payment_url)


@router.get(
    "/transactions/{transaction_id}",
    response_model=TransactionDetailsResponse,
    tags=["Handler Frontend"],
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
        deposit_address=transaction.deposit_address.address,
        amount=transaction.amount,
        urls={
            "success": transaction.success_url,
            "failure": transaction.failure_url,
            "error": transaction.error_url,
        },
        status=transaction.status.value,
    )


@router.put(
    "/transactions/{transaction_id}/status",
    tags=["Handler Frontend"],
)
def update_transaction_status(
    transaction_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """
    Update the status of a transaction to COMPLETED.
    """
    transaction = db.query(Transaction).filter_by(id=transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")

    if transaction.status == TransactionStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Transaction is already completed.")

    transaction.status = TransactionStatus.COMPLETED
    db.commit()

    return {"message": "Transaction status updated to COMPLETED."}
