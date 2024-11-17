from typing import Literal

from pydantic import UUID4, BaseModel


class OrderStatusUpdateRequest(BaseModel):
    psp_order_id: UUID4
    status: Literal["completed", "failed"]
