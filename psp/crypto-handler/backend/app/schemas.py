from pydantic import UUID4, BaseModel, HttpUrl, PositiveFloat


class TransactionProceedRequest(BaseModel):
    class NextUrls(BaseModel):
        success: HttpUrl
        failure: HttpUrl
        error: HttpUrl

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
    deposit_addresses: list[str]


class ConfigureMerchantRequest(BaseModel):
    merchant_id: UUID4
    configuration: MerchantConfiguration
