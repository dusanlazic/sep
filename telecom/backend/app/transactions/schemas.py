from typing import Literal

from pydantic import UUID4, BaseModel


class OrderStatusUpdateRequest(BaseModel):
    transaction_id: UUID4
    status: Literal["completed", "failed"]
