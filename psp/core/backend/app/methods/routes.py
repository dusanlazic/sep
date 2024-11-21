from fastapi import APIRouter, Depends

from ..auth.dependencies import get_current_merchant_manager, is_admin
from . import service
from .schemas import (
    MerchantPaymentMethodConfigurationRequest,
    MerchantPaymentMethodConfigurationResponse,
    PaymentMethodCreateRequest,
    PaymentMethodResponse,
)

router = APIRouter(prefix="/payment-methods")


@router.get(
    "/",
    response_model=list[PaymentMethodResponse],
    tags=["PSP Admin", "Merchant Manager"],
)
def get_payment_methods():
    """
    Retrieve all payment methods supported by the PSP.
    """
    pass


@router.post(
    "/",
    dependencies=[Depends(is_admin)],
    response_model=PaymentMethodResponse,
    tags=["PSP Admin"],
)
def add_payment_method(new_payment_method: PaymentMethodCreateRequest):
    """
    Introduce a new payment method.
    """
    # TODO: PSP Core should request /schema from the handler to get
    # the configuration schema (jsonschema), and store it in the database.


@router.get(
    "/config",
    dependencies=[Depends(get_current_merchant_manager)],
    response_model=MerchantPaymentMethodConfigurationResponse,
    tags=["Merchant Manager"],
)
def get_merchant_payment_methods_configuration():
    """
    Retrieve configurations for each payment methods enabled for the current merchant.
    """
    pass


@router.post(
    "/config",
    dependencies=[Depends(get_current_merchant_manager)],
    response_model=MerchantPaymentMethodConfigurationResponse,
    tags=["Merchant Manager"],
)
def set_merchant_payment_method_configuration(
    new_configuration: MerchantPaymentMethodConfigurationRequest,
):
    """
    Configure all payment methods for the current merchant.
    """
    pass
    # TODO: PSP Core should sync the configuration across all the handlers.
    # Each handler should have an endpoint to receive the configuration.
