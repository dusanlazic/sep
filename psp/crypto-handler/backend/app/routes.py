from fastapi import APIRouter

from .schemas import (
    ConfigureMerchantRequest,
    HandlerConfigurationSchemaResponse,
    MerchantConfiguration,
    TransactionProceedRequest,
    TransactionProceedResponse,
)

router = APIRouter()


@router.post(
    "/transactions",
    response_model=TransactionProceedResponse,
    tags=["PSP Core"],
)
def proceed_with_transaction(transaction: TransactionProceedRequest):
    """
    Provide handler information to proceed with the transaction and
    receive PAYMENT_URL to redirect the customers to.
    """
    pass
    # TODO: Persist that transaction in handler database
    # Call the external service or internal method to get the next url (PAYMENT_URL)
    # and return it to redirect the customer.


@router.get(
    "/schema",
    response_model=HandlerConfigurationSchemaResponse,
    tags=["PSP Core"],
)
def get_handler_configuration_schema():
    """
    Get information that describes the handler and how merchants
    should configure it.
    """
    return HandlerConfigurationSchemaResponse(
        title="Pay With Bitcoin",
        configuration_schema=MerchantConfiguration.model_json_schema(),
    )


@router.post("/merchants", tags=["PSP Core"])
def add_new_merchant(new_merchant: ConfigureMerchantRequest):
    """
    Add a new merchant to the handler and configure it.
    """
    # TODO: Persist the merchant configuration in the handler database
    return {"message": "Merchant added successfully."}
