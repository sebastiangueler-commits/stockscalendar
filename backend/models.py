from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from backend.database import Base
import enum


class UserRole(str, enum.Enum):
    free = "free"
    premium = "premium"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.free, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    subscription_expires_at = Column(DateTime, nullable=True)

    stripe_customer_id = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="usd")
    plan = Column(String, nullable=False)  # monthly or annual
    stripe_event_id = Column(String, nullable=True)
    status = Column(String, default="succeeded")

    user = relationship("User", backref="payments")


class CalendarFile(Base):
    __tablename__ = "calendar_files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # historical or fundamental
    path = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)

