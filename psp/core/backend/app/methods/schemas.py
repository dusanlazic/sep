from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, StringConstraints


class PaymentMethodResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    configuration_schema: dict


class PaymentMethodCreateRequest(BaseModel):
    name: str = Field(description="Name of the payment method")
    service_name: str = Field(description="Consul service name of the payment method")


class MerchantPaymentMethodConfigurationResponse(BaseModel):
    config: dict
    yaml: str


class MerchantPaymentMethodConfigurationRequest(BaseModel):
    yaml: str
