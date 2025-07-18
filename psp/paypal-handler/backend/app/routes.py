import uuid 
import time
import base64
import requests

from .config import config
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from .schemas import (
    BarResponse,
    FooRequest,
    TransactionDetailsResponse,
    TransactionProceedRequest,
    TransactionProceedResponse,
    ConfigureMerchantRequest,
    MerchantConfiguration,
    HandlerConfigurationSchemaResponse,
)
from .database import get_db
from .models import Merchant, Transaction, TransactionStatus

_token_cache: dict[str, tuple[str, float]] = {}  # { "sandbox": (token, exp_ts) }


def _get_cached_token() -> str:
    """
    Fetch or refresh a bearer token for the sandbox environment.
    Synchronous flavour because your endpoint is sync.
    """
    now  = time.time()
    env  = "sandbox"

    if env in _token_cache and _token_cache[env][1] > now:
        return _token_cache[env][0]

    client_id = config.paypal_client_id.strip()
    client_secret = config.paypal_client_secret.strip()
    
    credentials = f"{client_id}:{client_secret}"
    auth_hdr = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    try:
        r = requests.post(
            f"{config.paypal_api_base}/v1/oauth2/token",
            headers={
                "Authorization": f"Basic {auth_hdr}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={"grant_type": "client_credentials"},
            timeout=10,
        )
        r.raise_for_status()
    except requests.RequestException as exc:
        if hasattr(exc, 'response') and exc.response is not None:
            raise HTTPException(502, f"PayPal auth failed: {exc.response.text!s}")
        else:
            raise HTTPException(502, f"PayPal auth failed: {str(exc)}")

    data = r.json()
    _token_cache[env] = (data["access_token"], now + data["expires_in"] - 60)
    return _token_cache[env][0]


def _create_paypal_order(amount: float, merchant_email: str, success: str, cancel: str) -> tuple[str, str]:
    """
    Returns (order_id, approve_url)
    """
    token = _get_cached_token()

    order_body = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "EUR",
                    "value": f"{amount:.2f}",
                },
                "payee": {
                    "email_address": merchant_email,
                }
            }
        ],
        "payment_source": {
            "paypal": {
                "experience_context": {
                    "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                    "user_action": "PAY_NOW",
                    "return_url": str(success),
                    "cancel_url": str(cancel),
                }
            }
        }
    }

    try:
        r = requests.post(
            f"{config.paypal_api_base}/v2/checkout/orders",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json=order_body,
            timeout=10,
        )
        r.raise_for_status()
    except requests.RequestException as exc:
        if hasattr(exc, 'response') and exc.response is not None:
            raise HTTPException(502, f"Order creation failed: {exc.response.text!s}")
        else:
            raise HTTPException(502, f"Order creation failed: {str(exc)}")

    data = r.json()

    approve = next(
        (l["href"] for l in data["links"] if l["rel"] in ("approve", "payer-action")),
        None
    )
    if not approve:
        raise HTTPException(500, "PayPal response missing approve/payer-action link")

    return data["id"], approve


router = APIRouter()


@router.post("/merchants", tags=["PSP Core"])
def add_new_merchant(
    merchant_create_request: ConfigureMerchantRequest,
    db: Session = Depends(get_db),
):
    """
    Add a new merchant to the handler and configure it.
    """
    merchant = (
        db.query(Merchant)
        .filter_by(psp_id=str(merchant_create_request.merchant_id))
        .first()
    )
    if merchant:
        raise HTTPException(status_code=409, detail="Merchant already exists.")

    new_merchant = Merchant(
        psp_id=merchant_create_request.merchant_id,
        paypal_merchant_email=merchant_create_request.configuration.paypal_merchant_email,
    )
    db.add(new_merchant)
    db.commit()

    return {"message": "Merchant added successfully."}


@router.post(
    "/transactions",
    response_model=TransactionProceedResponse,
    tags=["PSP Core"],
)
def proceed_with_transaction(
    transaction_proceed_request: TransactionProceedRequest,
    db: Session = Depends(get_db),
):
    """
    Initiate a sandbox PayPal transaction and
    receive PAYMENT_URL to redirect the customers to.
    """
    # Find the merchant by merchant_id (psp_id in our DB)
    merchant = (
        db.query(Merchant)
        .filter_by(psp_id=str(transaction_proceed_request.merchant_id))
        .first()
    )
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found.")
    
    try:
        order_id, approve_url = _create_paypal_order(
            amount=transaction_proceed_request.amount,
            merchant_email = merchant.paypal_merchant_email,
            success=transaction_proceed_request.next_urls.success,
            cancel=transaction_proceed_request.next_urls.failure,
        )
    except HTTPException:
        # Bubble up with proper error codes.
        raise

    new_txn = Transaction(
        psp_id=str(transaction_proceed_request.id),
        paypal_id=order_id,
        merchant_id=merchant.id,
        amount=transaction_proceed_request.amount,
        status=TransactionStatus.PENDING,
        success_url=str(transaction_proceed_request.next_urls.success),
        failure_url=str(transaction_proceed_request.next_urls.failure),
        error_url=str(transaction_proceed_request.next_urls.error),
    )
    try:
        db.add(new_txn)
        db.commit()         # write + release row‑level locks
    except Exception as e:
        db.rollback()
        raise HTTPException(
            500, f"There was an error when storing the transaction: {e!s}"
        )

    return TransactionProceedResponse(payment_url=approve_url)


@router.get(
    "/transactions/{transaction_id}",
    response_model=TransactionDetailsResponse,
    tags=["PSP Core"],
)
def get_transaction(transaction_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Get information about the transaction. Used by the handler frontend to
    display the amount and QR code to the customer, and to check the status
    of the transaction in order to redirect the customer to the correct page.

    This endpoint can be called repeatably to check the status of the transaction.
    """
    transaction = db.query(Transaction).filter_by(id=transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")

    return TransactionDetailsResponse(
        amount=transaction.amount,
        urls={
            "success": transaction.success_url,
            "failure": transaction.failure_url,
            "error": transaction.error_url,
        },
        status=transaction.status.value,
    )


@router.post("/transactions/events")
async def paypal_webhook(request: Request, db: Session = Depends(get_db)):
    """
    PayPal Webhook endpoint. Updates Transaction status based on PayPal events.
    """
    payload = await request.json()
    event_type = payload.get("event_type")
    resource = payload.get("resource", {})
    order_id = None

    # For PAYMENT.CAPTURE.COMPLETED and similar, the order ID is in resource["supplementary_data"]["related_ids"]["order_id"]
    # For CHECKOUT.ORDER.APPROVED, it's resource["id"]
    if event_type.startswith("PAYMENT.CAPTURE."):
        order_id = (
            resource.get("supplementary_data", {})
            .get("related_ids", {})
            .get("order_id")
        )
    elif event_type.startswith("CHECKOUT.ORDER."):
        order_id = resource.get("id")

    if not order_id:
        print(f"[PayPal Webhook] Could not extract order_id from event: {event_type}")
        return {"status": "ignored", "reason": "no order_id"}

    txn = db.query(Transaction).filter_by(paypal_id=order_id).first()
    if not txn:
        print(f"[PayPal Webhook] No Transaction found for PayPal order_id: {order_id}")
        return {"status": "ignored", "reason": "no transaction"}

    if event_type == "PAYMENT.CAPTURE.COMPLETED":
        txn.status = TransactionStatus.COMPLETED
    elif event_type == "PAYMENT.CAPTURE.DENIED":
        txn.status = TransactionStatus.FAILED
    elif event_type == "CHECKOUT.ORDER.APPROVED":
        txn.status = TransactionStatus.PENDING
    else:
        print(f"[PayPal Webhook] Unhandled event type: {event_type}")
        return {"status": "ignored", "reason": "unhandled event"}

    if txn.status == TransactionStatus.COMPLETED:
        requests.put(
            f"{config.psp_api_base_url}/transactions/{txn.psp_id}/status",
            json={"status": "completed"},
        )
    else:
        requests.put(
            f"{config.psp_api_base_url}/transactions/{txn.psp_id}/status",
            json={"status": "failed"},
        )

    db.commit()
    return {"status": "updated", "order_id": order_id, "new_status": txn.status.value}


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
        title="Pay With PayPal",
        configuration_schema=MerchantConfiguration.model_json_schema(),
    )
