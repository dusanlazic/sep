from pydantic import AwareDatetime, BaseModel, HttpUrl, PositiveFloat, PositiveInt


class OfferResponse(BaseModel):
    identifier: str
    title: str
    description: str
    price: PositiveFloat


class SubscriptionResponse(BaseModel):
    offer_identifier: str
    title: str
    description: str
    price: PositiveFloat
    start_date: AwareDatetime
    end_date: AwareDatetime
    auto_renew: bool


class PaymentInitiatedResponse(BaseModel):
    payment_url: HttpUrl


class SubscriptionRequest(BaseModel):
    offer_identifier: str
    duration_in_years: PositiveInt
    auto_renew: bool
