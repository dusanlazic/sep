from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, StringConstraints


class PaymentMethodResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    configuration_schema: dict


class PaymentMethodCreateRequest(BaseModel):
    name: str = Field(description="Name of the payment method")
    host: str = Field(description="Host of the payment method")
    port: int = Field(description="Port of the payment method", ge=1, le=65535)
    # TODO: Replace host and port with Consul service name maybe?


class MerchantPaymentMethodConfigurationResponse(BaseModel):
    config: dict
    yaml: str


class MerchantPaymentMethodConfigurationRequest(BaseModel):
    yaml: str
