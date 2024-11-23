from pydantic import (
    AliasPath,
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    PositiveFloat,
    PositiveInt,
)


class OfferResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    identifier: str
    title: str
    description: str
    price: PositiveFloat


class SubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    offer_identifier: str = Field(alias=AliasPath("offer", "identifier"))
    title: str = Field(alias=AliasPath("offer", "title"))
    description: str = Field(alias=AliasPath("offer", "description"))
    price: PositiveFloat = Field(alias=AliasPath("offer", "price"))
    duration_in_years: PositiveInt
    start_date: AwareDatetime
    end_date: AwareDatetime
    auto_renew: bool


class PaymentInitiatedResponse(BaseModel):
    payment_url: HttpUrl


class SubscriptionRequest(BaseModel):
    offer_identifier: str
    duration_in_years: PositiveInt
    auto_renew: bool
