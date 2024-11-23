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

    deposit_addresses: Mapped[list["DepositAddress"]] = relationship(
        "DepositAddress",
        back_populates="merchant",
        cascade="all, delete-orphan",
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="merchant",
        cascade="all, delete-orphan",
    )


class DepositAddress(Base):
    __tablename__ = "deposit_addresses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    address: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    balance: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    merchant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(Merchant.id), nullable=False
    )
    merchant: Mapped[Merchant] = relationship(
        "Merchant",
        back_populates="deposit_addresses",
    )

    transaction: Mapped["Transaction"] = relationship(
        "Transaction",
        back_populates="deposit_address",
        uselist=False,
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    psp_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    merchant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(Merchant.id), nullable=False
    )
    deposit_address_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(DepositAddress.id),
        nullable=False,
        unique=True,  # Enforce one-to-one mapping
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
    deposit_address: Mapped["DepositAddress"] = relationship(
        "DepositAddress",
        back_populates="transaction",
    )
