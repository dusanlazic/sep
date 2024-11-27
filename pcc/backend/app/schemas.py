from pydantic import UUID4, AwareDatetime, BaseModel


class PaymentRequest(BaseModel):
    amount: float
    acquirer_order_id: UUID4
    acquirer_timestamp: AwareDatetime
    card_number: str
    card_expiration: str
    card_cvv: str
    card_holder: str
