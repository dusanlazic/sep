from pydantic import UUID4, BaseModel, HttpUrl, PositiveFloat


class NextUrls(BaseModel):
    success: HttpUrl
    failure: HttpUrl
    error: HttpUrl


class TransactionProceedRequest(BaseModel):
    id: UUID4
    merchant_id: UUID4
    amount: PositiveFloat
    next_urls: NextUrls


class TransactionProceedResponse(BaseModel):
    payment_url: HttpUrl


class HandlerConfigurationSchemaResponse(BaseModel):
    title: str
    configuration_schema: dict


class MerchantConfiguration(BaseModel):
    bank_merchant_id: str
    bank_merchant_password: str


class ConfigureMerchantRequest(BaseModel):
    merchant_id: UUID4
    configuration: MerchantConfiguration
