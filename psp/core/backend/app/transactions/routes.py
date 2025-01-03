from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth.dependencies import get_current_merchant
from ..database import get_db
from ..merchants.models import Merchant
from . import service
from .schemas import (
    TransactionCreateRequest,
    TransactionCreateResponse,
    TransactionDetailsResponse,
    TransactionProceedRequest,
    TransactionProceedResponse,
    TransactionStatusUpdateRequest,
)

router = APIRouter(prefix="/transactions")


@router.post(
    "/",
    response_model=TransactionCreateResponse,
    tags=["Merchant Client App"],
)
def create_transaction(
    transaction_creation_request: TransactionCreateRequest,
    db: Session = Depends(get_db),
    merchant: Merchant = Depends(get_current_merchant),
):
    """
    Initialize a new transaction. Called by the merchant client application.
    Uses transaction ID (included in proceed_url) to redirect the user to the
    PSP page for choosing the payment method.

    Merchant client app should handle the transaction internally.
    """
    transaction = service.create_transaction(
        db,
        merchant,
        transaction_creation_request.amount,
        transaction_creation_request.subject,
        transaction_creation_request.description,
    )
    proceed_url = service.generate_proceed_url(transaction.id)

    return TransactionCreateResponse(
        transaction_id=transaction.id,
        proceed_url=proceed_url,
    )


@router.get(
    "/{transaction_id}",
    response_model=TransactionDetailsResponse,
    tags=["Customer"],
)
def get_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Retrieve the details of a transaction to display to the user.
    Includes the supported payment methods so the user can choose one.
    """
    transaction = service.get_transaction(db, transaction_id)
    return TransactionDetailsResponse(
        id=transaction.id,
        amount=transaction.amount,
        subject=transaction.subject,
        description=transaction.description,
        payment_methods=transaction.merchant.get_supported_payment_method_names(),
    )


@router.post(
    "/{transaction_id}/proceed",
    response_model=TransactionProceedResponse,
    tags=["Customer"],
)
def proceed_to_payment(
    transaction_id: UUID,
    proceed_request: TransactionProceedRequest,
    db: Session = Depends(get_db),
):
    """
    Request to proceed with the transaction using the selected payment method.
    """
    payment_url = service.get_payment_url(
        db, transaction_id, proceed_request.payment_method_name
    )
    return TransactionProceedResponse(payment_url=payment_url)


@router.put(
    "/{transaction_id}/status",
    tags=["Handler"],
)
def update_transaction_status(
    transaction_id: UUID,
    status: TransactionStatusUpdateRequest,
    db: Session = Depends(get_db),
):
    """
    Update the transaction status after the payment has been processed by the handler.
    """
    service.update_transaction_status(db, transaction_id, status.status)
    return {"detail": "Status update instruction received."}
