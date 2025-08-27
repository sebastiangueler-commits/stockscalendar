from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    subscription_expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SearchResult(BaseModel):
    symbol: str
    best_buy_dates: List[str]
    best_sell_dates: List[str]
    historical_stats: Dict[str, Any] = Field(default_factory=dict)
    fundamental_status: Dict[str, Any] = Field(default_factory=dict)


class PaymentOut(BaseModel):
    id: int
    user_id: int
    amount: float
    currency: str
    plan: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

