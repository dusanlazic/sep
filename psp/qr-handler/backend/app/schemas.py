from pydantic import BaseModel, UUID4, HttpUrl, PositiveFloat


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


class TransactionDetailsResponse(BaseModel):
    deposit_address: str
    amount: PositiveFloat
    urls: NextUrls
    status: str
    

class MerchantConfiguration(BaseModel):
    merchant_name: str
    merchant_account_number: int


class ConfigureMerchantRequest(BaseModel):
    merchant_id: UUID4
    configuration: MerchantConfiguration


class HandlerConfigurationSchemaResponse(BaseModel):
    title: str
    configuration_schema: dict
