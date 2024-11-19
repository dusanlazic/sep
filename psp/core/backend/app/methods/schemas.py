from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, StringConstraints


class PaymentMethodResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    config_schema: dict


class PaymentMethodCreateRequest(BaseModel):
    host: str = Field(description="Host of the payment method")
    port: int = Field(description="Port of the payment method", ge=1, le=65535)
    # TODO: Replace host and port with Consul service name maybe?


class MerchantPaymentMethodConfigurationResponse(BaseModel):
    configuration_yaml: str


class MerchantPaymentMethodConfigurationRequest(BaseModel):
    configuration_yaml: str
