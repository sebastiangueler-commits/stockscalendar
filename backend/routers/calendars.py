import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import UserRole, User
from backend.routers.auth import require_role
from backend.services.ml import train_historical_calendar


router = APIRouter()


@router.get("/historical")
def get_historical_calendar(_: User = Depends(require_role(UserRole.premium))):
    try:
        with open("calendar_historical.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Historical calendar not found")


@router.get("/fundamental")
def get_fundamental_calendar(_: User = Depends(require_role(UserRole.premium))):
    try:
        with open("calendar_fundamental.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Fundamental calendar not found")


 


@router.post("/train")
def retrain(_: User = Depends(require_role(UserRole.admin))):
    res = train_historical_calendar()
    return res

