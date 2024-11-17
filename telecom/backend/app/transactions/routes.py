from uuid import UUID

from fastapi import APIRouter

from . import service
from .schemas import OrderStatusUpdateRequest

router = APIRouter(prefix="/psp", tags=["PSP Integration"])


@router.post("/callback")
def update_transaction_status(OrderStatusUpdateRequest: OrderStatusUpdateRequest):
    """
    Update the status of a transaction.

    Note: This endpoint is called by the PSP to update the status of a transaction. Currently,
    it lacks mechanisms to authenticate the PSP (e.g., API keys, signatures, etc.).
    """
    return {"detail": "Status updated."}
