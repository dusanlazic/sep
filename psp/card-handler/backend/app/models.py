import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class TransactionStatus(enum.Enum):
    COMPLETED = "completed"
    PENDING = "pending"
    FAILED = "failed"


class Merchant(Base):
    __tablename__ = "merchants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    psp_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    bank_merchant_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    bank_merchant_password: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="merchant",
        cascade="all, delete-orphan",
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    psp_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    bank_payment_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    merchant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(Merchant.id), nullable=False
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus, native_enum=True), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    merchant: Mapped["Merchant"] = relationship(
        "Merchant",
        back_populates="transactions",
    )
