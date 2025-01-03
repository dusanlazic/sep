from typing import Annotated, Literal

from pydantic import UUID4, BaseModel, ConfigDict, Field, HttpUrl, PositiveFloat


class TransactionStatusUpdateRequest(BaseModel):
    status: Literal["completed", "failed"]


class TransactionCreateRequest(BaseModel):
    amount: PositiveFloat
    subject: str
    description: str


class TransactionCreateResponse(BaseModel):
    transaction_id: UUID4
    proceed_url: HttpUrl = Field(
        examples=["http://frontend.psp.local/transactions/{uuid}"]
    )


class TransactionProceedRequest(BaseModel):
    payment_method_name: str


class TransactionDetailsResponse(BaseModel):
    id: UUID4
    amount: PositiveFloat
    subject: str
    description: str
    payment_methods: list[str]


class TransactionProceedResponse(BaseModel):
    payment_url: HttpUrl = Field(
        examples=[
            "http://frontend.external-service.local/transactions/{integer} OR http://frontend.internal-btc-handler.psp.local/transactions/{base64}",
        ]
    )
