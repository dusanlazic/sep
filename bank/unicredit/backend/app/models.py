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
    password: Mapped[str] = mapped_column(String, nullable=False)

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


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    card_number: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    card_holder_name: Mapped[str] = mapped_column(String, nullable=False)
    expiration_date: Mapped[str] = mapped_column(String, nullable=False)
    cvv: Mapped[str] = mapped_column(String, nullable=False)
    balance: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
