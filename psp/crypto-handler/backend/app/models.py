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

    psp_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    deposit_addresses: Mapped[list["DepositAddress"]] = relationship(
        "DepositAddress",
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
    address: Mapped[String] = mapped_column(String, nullable=False, unique=True)
    balance: Mapped[Float] = mapped_column(Float, nullable=False, default=0.0)

    merchant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(Merchant.psp_id), primary_key=True
    )
    merchant: Mapped[Merchant] = relationship(
        "Merchant",
        back_populates="deposit_addresses",
    )


class Transaction(Base):
    __tablename__ = "transactions"

    psp_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    amount: Mapped[Float] = mapped_column(Float, nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus, native_enum=True), nullable=False
    )
    deposit_address_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(DepositAddress.id), nullable=False
    )
    deposit_address: Mapped[DepositAddress] = relationship(
        "DepositAddress",
        back_populates="transactions",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
