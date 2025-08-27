import json
import os
from datetime import datetime
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import User, UserRole, CalendarFile
from backend.auth.security import hash_password


HISTORICAL_PATH = os.path.abspath("calendar_historical.json")
FUNDAMENTAL_PATH = os.path.abspath("calendar_fundamental.json")


def ensure_seed_files() -> None:
    if not os.path.exists(HISTORICAL_PATH):
        with open(HISTORICAL_PATH, "w", encoding="utf-8") as f:
            json.dump({"status": "seed", "generated_at": datetime.utcnow().isoformat() + "Z", "items": []}, f)
    if not os.path.exists(FUNDAMENTAL_PATH):
        with open(FUNDAMENTAL_PATH, "w", encoding="utf-8") as f:
            json.dump({"status": "seed", "generated_at": datetime.utcnow().isoformat() + "Z", "items": []}, f)
    with SessionLocal() as db:
        upsert_calendar_file(db, "historical", HISTORICAL_PATH)
        upsert_calendar_file(db, "fundamental", FUNDAMENTAL_PATH)


def upsert_calendar_file(db: Session, name: str, path: str) -> None:
    record = db.query(CalendarFile).filter_by(name=name).first()
    if record:
        record.path = path
        record.updated_at = datetime.utcnow()
    else:
        record = CalendarFile(name=name, path=path, updated_at=datetime.utcnow())
        db.add(record)
    db.commit()


def ensure_admin_user() -> None:
    from backend.config import settings

    with SessionLocal() as db:
        existing = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if existing:
            return
        admin = User(
            email=settings.ADMIN_EMAIL,
            password_hash=hash_password(settings.ADMIN_PASSWORD),
            role=UserRole.admin,
            is_active=True,
        )
        db.add(admin)
        db.commit()

