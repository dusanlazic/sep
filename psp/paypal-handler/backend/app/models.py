import enum
import uuid
from datetime import datetime

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime, Float, UUID
from sqlalchemy.sql import func

from .database import Base


class Merchant(Base):
    __tablename__ = "merchants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    psp_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    paypal_merchant_email: Mapped[str] = mapped_column(String, nullable=False)

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="merchant",
        cascade="all, delete-orphan",
    )


class TransactionStatus(enum.Enum):
    COMPLETED = "completed"
    PENDING = "pending"
    FAILED = "failed"


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    psp_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    paypal_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    merchant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(Merchant.id), nullable=False
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus, native_enum=True), nullable=False
    )
    success_url: Mapped[str] = mapped_column(String, nullable=False)
    failure_url: Mapped[str] = mapped_column(String, nullable=False)
    error_url: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    merchant: Mapped["Merchant"] = relationship(
        "Merchant",
        back_populates="transactions",
    )
