from typing import Annotated

from pydantic import UUID4, BaseModel, HttpUrl, PositiveFloat


class TransactionCreateRequest(BaseModel):
    amount: PositiveFloat
    subject: str
    description: str


class TransactionCreateResponse(BaseModel):
    id: UUID4
    amount: PositiveFloat
    subject: str
    description: str
    payment_methods: list[str]


class TransactionProceedRequest(BaseModel):
    payment_method: str


class TransactionProceedResponse(BaseModel):
    payment_url: HttpUrl
