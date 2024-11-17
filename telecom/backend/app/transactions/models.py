import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from ..offers.models import Subscription


class TransactionStatus(enum.Enum):
    COMPLETED = "completed"
    PENDING = "pending"
    FAILED = "failed"


class Transaction(Base):
    __tablename__ = "transactions"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    psp_order_id = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
    )
    subscription_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(Subscription.id), nullable=False
    )
    subscription: Mapped[Subscription] = relationship(
        Subscription,
        foreign_keys=[subscription_id],
    )
    amount = mapped_column(Float, nullable=False)
    status = mapped_column(Enum(TransactionStatus, native_enum=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
