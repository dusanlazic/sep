import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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


@router.post(
    "/transactions",
    response_model=TransactionProceedResponse,
    tags=["PSP Core"],
)
def proceed_with_transaction(transaction: TransactionProceedRequest):
    """
    Provide handler information to proceed with the transaction and
    receive PAYMENT_URL to redirect the customers to.
    """
    pass
    # TODO: Persist that transaction in handler database
    # Call the external service or internal method to get the next url (PAYMENT_URL)
    # and return it to redirect the customer.


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
        db.query(Merchant).filter_by(psp_id=merchant_create_request.merchant_id).first()
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


@router.get(
    "/transactions/{transaction_id}",
    response_model=TransactionDetailsResponse,
    tags=["Handler Frontend"],
)
def get_transaction(transaction_id: uuid.UUID):
    """
    Get information about the transaction. Used by the handler frontend to
    display the amount and QR code to the customer, and to check the status
    of the transaction in order to redirect the customer to the correct page.

    This endpoint can be called repeatably to check the status of the transaction.
    """
    pass
