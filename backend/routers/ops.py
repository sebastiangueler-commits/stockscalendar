from fastapi import APIRouter, Depends
from backend.models import UserRole, User
from backend.routers.auth import require_role
from backend.services.ml import train_historical_calendar


router = APIRouter()


@router.post("/train")
def retrain(_: User = Depends(require_role(UserRole.admin))):
    res = train_historical_calendar()
    return res

