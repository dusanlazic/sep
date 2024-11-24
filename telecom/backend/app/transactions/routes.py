from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from . import service
from .schemas import OrderStatusUpdateRequest

router = APIRouter(prefix="/psp", tags=["PSP Integration"])


@router.post("/callback")
def update_transaction_status(
    db: Annotated[Session, Depends(get_db)],
    orderStatusUpdateRequest: OrderStatusUpdateRequest,
):
    """
    Update the status of a transaction.

    Note: This endpoint is called by the PSP to update the status of a transaction. Currently,
    it lacks mechanisms to authenticate the PSP (e.g., API keys, signatures, etc.).
    """

    service.update_transaction_status(db, orderStatusUpdateRequest)
    return {"detail": "Status update received."}
