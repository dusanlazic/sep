from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, StringConstraints


class MerchantRegistrationRequest(BaseModel):
    username: Annotated[str, StringConstraints(min_length=3, max_length=50)] = Field(
        description="Username must be between 3 and 50 characters"
    )
    password: Annotated[str, StringConstraints(min_length=8)] = Field(
        description="Password must be at least 8 characters long"
    )
    title: Annotated[str, StringConstraints(min_length=1, max_length=100)] = Field(
        description="Title must be between 1 and 100 characters"
    )
    payment_success_url: HttpUrl = Field(
        description="Merchant's web page URL to redirect the user on successful payment"
    )
    payment_failure_url: HttpUrl = Field(
        description="Merchant's web page URL to redirect the user on failed payment"
    )
    payment_error_url: HttpUrl = Field(
        description="Merchant's web page URL to redirect the user on payment errors"
    )
    payment_callback_url: HttpUrl = Field(
        description="Webshop API URL to notify the merchant on payment status update"
    )


class MerchantLoginRequest(BaseModel):
    username: str
    password: str


class MerchantBriefDataResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    title: str
    api_key: str
