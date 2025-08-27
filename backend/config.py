import os
from pydantic import BaseModel


class Settings(BaseModel):
    APP_NAME: str = os.getenv("APP_NAME", "Financial Calendars App")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "43200"))

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@example.com")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "ChangeThisAdminPassword123!")

    STRIPE_API_KEY: str | None = os.getenv("STRIPE_API_KEY")
    STRIPE_WEBHOOK_SECRET: str | None = os.getenv("STRIPE_WEBHOOK_SECRET")
    STRIPE_PRICE_MONTHLY: str | None = os.getenv("STRIPE_PRICE_MONTHLY")
    STRIPE_PRICE_ANNUAL: str | None = os.getenv("STRIPE_PRICE_ANNUAL")

    DATA_CACHE_DIR: str = os.getenv("DATA_CACHE_DIR", "./data_cache")
    HISTORICAL_START: str = os.getenv("HISTORICAL_START", "2010-01-01")
    FUNDAMENTAL_BOOTSTRAP_LIMIT: int | None = (
        int(os.getenv("FUNDAMENTAL_BOOTSTRAP_LIMIT")) if os.getenv("FUNDAMENTAL_BOOTSTRAP_LIMIT") else None
    )


settings = Settings()

