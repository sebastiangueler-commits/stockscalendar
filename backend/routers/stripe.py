import os
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from backend.config import settings
from backend.database import get_db
from backend.models import User, UserRole, Payment
from backend.routers.auth import require_role, get_current_user


router = APIRouter()


def _stripe_client():
    import stripe
    if not settings.STRIPE_API_KEY:
        raise HTTPException(status_code=503, detail="Stripe not configured")
    stripe.api_key = settings.STRIPE_API_KEY
    return stripe


@router.post("/checkout")
def create_checkout_session(plan: str, user: User = Depends(get_current_user)):
    stripe = _stripe_client()
    price_id = settings.STRIPE_PRICE_MONTHLY if plan == "monthly" else settings.STRIPE_PRICE_ANNUAL if plan == "annual" else None
    if not price_id:
        raise HTTPException(status_code=400, detail="Invalid plan")
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
        customer_email=user.email,
    )
    return {"checkout_url": session.url}


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    import stripe
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    if not settings.STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=503, detail="Stripe webhook not configured")
    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event["type"] in ("checkout.session.completed", "invoice.payment_succeeded"):
        data = event["data"]["object"]
        email = data.get("customer_email") or data.get("customer_details", {}).get("email")
        if email:
            user = db.query(User).filter(User.email == email).first()
            if user:
                plan = "annual" if data.get("lines", {}).get("data", [{}])[0].get("price", {}).get("recurring", {}).get("interval") == "year" else "monthly"
                amount = (data.get("amount_total") or data.get("amount_paid") or 0) / 100.0
                user.role = UserRole.premium
                user.subscription_expires_at = datetime.utcnow() + timedelta(days=365 if plan == "annual" else 30)
                payment = Payment(user_id=user.id, amount=amount, currency="usd", plan=plan, stripe_event_id=event.get("id"), status="succeeded")
                db.add(payment)
                db.commit()

    return {"status": "ok"}

