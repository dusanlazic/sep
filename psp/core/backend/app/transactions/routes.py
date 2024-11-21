from fastapi import APIRouter, Depends

from ..auth.dependencies import get_current_merchant
from . import service
from .schemas import (
    TransactionCreateRequest,
    TransactionCreateResponse,
    TransactionProceedRequest,
    TransactionProceedResponse,
)

router = APIRouter(prefix="/transactions")


@router.post(
    "/",
    dependencies=[Depends(get_current_merchant)],
    response_model=TransactionCreateResponse,
    tags=["Merchant Client App"],
)
def create_transaction(new_transaction: TransactionCreateRequest):
    """
    Initialize a new transaction. Called by the merchant client application.
    Uses transaction ID (included in proceed_url) to redirect the user to the
    PSP page for choosing the payment method.

    Merchant client app should handle the transaction internally.
    """
    pass


@router.get(
    "/{transaction_id}",
    response_model=TransactionCreateResponse,
    tags=["Customer"],
)
def get_transaction(transaction_id: str):
    """
    Retrieve the details of a transaction to display to the user.
    Includes the supported payment methods so the user can choose one.
    """
    pass


@router.post(
    "/{transaction_id}/proceed",
    response_model=TransactionProceedResponse,
    tags=["Customer"],
)
def proceed_to_payment(transaction_id: str, proceed_request: TransactionProceedRequest):
    """
    Request to proceed with the transaction using the selected payment method.
    """
    pass
    # TODO: PSP Core
