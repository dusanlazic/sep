from fastapi import APIRouter, Depends

from ..auth.dependencies import get_current_merchant
from . import service
from .schemas import (
    TransactionCreateRequest,
    TransactionCreateResponse,
    TransactionProceedRequest,
    TransactionProceedResponse,
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post(
    "/",
    dependencies=[Depends(get_current_merchant)],
    response_model=TransactionCreateResponse,
)
def create_transaction(new_transaction: TransactionCreateRequest):
    """
    Initialize a new transaction.
    """
    pass


@router.get(
    "/{transaction_id}",
    response_model=TransactionCreateResponse,
)
def get_transaction(transaction_id: str):
    """
    Retrieve the details of a transaction to display to the user.
    Includes the supported payment methods.
    """
    pass


@router.post(
    "/{transaction_id}/proceed",
    response_model=TransactionProceedResponse,
)
def pay_transaction(transaction_id: str):
    """
    Request to proceed with the transaction.
    """
    pass
    # TODO: PSP Core
