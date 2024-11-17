import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..auth.models import User
from ..database import Base


class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    identifier: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(User.id), nullable=False)
    user: Mapped[User] = relationship(
        User,
        back_populates="subscriptions",
        foreign_keys=[user_id],
    )
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(Offer.id), nullable=False)
    offer: Mapped[Offer] = relationship(Offer, foreign_keys=[offer_id])
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_in_years: Mapped[int] = mapped_column(Integer, nullable=False)
    auto_renew: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # If the start_date is not provided, it means the subscription has not started yet.
