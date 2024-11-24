from pydantic import AwareDatetime, BaseModel, HttpUrl, PositiveFloat


class TransactionCreateRequest(BaseModel):
    merchant_id: str
    merchant_password: str
    amount: PositiveFloat
    merchant_order_id: str
    merchant_timestamp: AwareDatetime
    success_url: HttpUrl
    failure_url: HttpUrl
    error_url: HttpUrl


class PaymentInstructionsResponse(BaseModel):
    payment_id: str
    payment_url: HttpUrl


class PaymentRequest(BaseModel):
    card_number: str
    card_expiration: str
    card_cvv: str
    card_holder: str
