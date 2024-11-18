from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from .models import *
from .schemas import OrderStatusUpdateRequest


def update_transaction_status(db: Session, statusUpdate: OrderStatusUpdateRequest):
    try:
        transaction = db.query(Transaction).filter_by(psp_order_id=statusUpdate.psp_order_id).one()

        transaction.status = TransactionStatus[statusUpdate.status.upper()]
        db.commit()
    except NoResultFound:
        print(
            f"Transaction with PSP Order ID {statusUpdate.psp_order_id} not found."
        )
    except KeyError:
        print(
            f"Invalid status '{statusUpdate.status}' provided for PSP Order ID {statusUpdate.psp_order_id}."
        )
    except Exception:
        db.rollback()
        print(
            f"An error occurred while updating the transaction for PSP Order ID {statusUpdate.psp_order_id}."
        )
