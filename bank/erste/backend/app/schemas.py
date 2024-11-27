from typing import Literal

from pydantic import UUID4, AwareDatetime, BaseModel, HttpUrl, PositiveFloat


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


class PaymentResultResponse(BaseModel):
    detail: str
    next_url: HttpUrl


class PaymentRequest(BaseModel):
    card_number: str
    card_expiration: str
    card_cvv: str
    card_holder: str


class PccPaymentRequest(BaseModel):
    amount: PositiveFloat
    acquirer_order_id: UUID4
    acquirer_timestamp: AwareDatetime
    card_number: str
    card_expiration: str
    card_cvv: str
    card_holder: str


class PccPaymentResponse(BaseModel):
    acquirer_order_id: UUID4
    acquirer_timestamp: AwareDatetime
    issuer_order_id: UUID4
    issuer_timestamp: AwareDatetime
    status: Literal["success", "error"]
    msg: str
