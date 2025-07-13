from pydantic import UUID4, BaseModel, HttpUrl, PositiveFloat


class NextUrls(BaseModel):
    success: HttpUrl
    failure: HttpUrl
    error: HttpUrl


class FooRequest(BaseModel):
    fizz: str


class BarResponse(BaseModel):
    buzz: int


class TransactionProceedRequest(BaseModel):
    id: UUID4
    merchant_id: UUID4
    amount: PositiveFloat
    next_urls: NextUrls


class TransactionProceedResponse(BaseModel):
    payment_url: HttpUrl


class TransactionDetailsResponse(BaseModel):
    deposit_address: str
    amount: PositiveFloat
    urls: NextUrls
    status: str


class MerchantConfiguration(BaseModel):
    paypal_merchant_email: str


class ConfigureMerchantRequest(BaseModel):
    merchant_id: UUID4
    configuration: MerchantConfiguration
