from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth.dependencies import get_current_merchant_manager_id, is_admin
from ..database import get_db
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
def get_payment_methods(db: Session = Depends(get_db)):
    """
    Retrieve all payment methods supported by the PSP.
    """
    return service.get_payment_methods(db)


@router.post(
    "/",
    dependencies=[Depends(is_admin)],
    response_model=PaymentMethodResponse,
    tags=["PSP Admin"],
)
def add_payment_method(
    new_payment_method: PaymentMethodCreateRequest,
    db: Session = Depends(get_db),
):
    """
    Introduce a new payment method.
    """
    return service.add_payment_method(
        db,
        new_payment_method.name,
        new_payment_method.service_name,
    )


@router.get(
    "/config",
    dependencies=[Depends(get_current_merchant_manager_id)],
    response_model=MerchantPaymentMethodConfigurationResponse,
    tags=["Merchant Manager"],
)
def get_merchant_payment_methods_configuration(
    current_user_id: UUID = Depends(get_current_merchant_manager_id),
    db: Session = Depends(get_db),
):
    """
    Retrieve configurations for each payment methods enabled for the current merchant.
    """
    config, yaml_string = service.get_merchant_payment_methods_configuration(
        db, current_user_id
    )

    return MerchantPaymentMethodConfigurationResponse(
        config=config,
        yaml=yaml_string,
    )


@router.post(
    "/config",
    dependencies=[Depends(get_current_merchant_manager_id)],
    response_model=MerchantPaymentMethodConfigurationResponse,
    tags=["Merchant Manager"],
)
def set_merchant_payment_method_configuration(
    new_configuration: MerchantPaymentMethodConfigurationRequest,
    current_user_id: UUID = Depends(get_current_merchant_manager_id),
    db: Session = Depends(get_db),
):
    """
    Configure all payment methods for the current merchant.
    """
    updated_config, updated_yaml_string = (
        service.apply_merchant_payment_methods_configuration(
            db,
            new_configuration.yaml,
            current_user_id,
        )
    )

    if updated_config and updated_yaml_string:
        return MerchantPaymentMethodConfigurationResponse(
            config=updated_config,
            yaml=updated_yaml_string,
        )
