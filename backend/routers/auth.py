from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User, UserRole
from backend.schemas import UserCreate, UserLogin, UserOut, TokenOut
from backend.auth.security import hash_password, verify_password, create_access_token, decode_access_token


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", auto_error=False)


def _extract_bearer_from_request(request: Request) -> str | None:
    auth = request.headers.get("Authorization")
    if auth and auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1]
    cookie = request.cookies.get("access_token")
    if cookie and cookie.lower().startswith("bearer "):
        return cookie.split(" ", 1)[1]
    return None


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = _extract_bearer_from_request(request)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive or missing user")
    return user


def get_optional_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    try:
        token = _extract_bearer_from_request(request)
        if not token:
            return None
        payload = decode_access_token(token)
        email = payload.get("sub")
        if not email:
            return None
        user = db.query(User).filter(User.email == email).first()
        if not user or not user.is_active:
            return None
        return user
    except Exception:
        return None


def require_role(required: UserRole):
    def _inner(user: User = Depends(get_current_user)) -> User:
        if required == UserRole.admin and user.role != UserRole.admin:
            raise HTTPException(status_code=403, detail="Admins only")
        if required == UserRole.premium and user.role not in (UserRole.premium, UserRole.admin):
            raise HTTPException(status_code=403, detail="Premium required")
        return user
    return _inner


@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=payload.email, password_hash=hash_password(payload.password), role=UserRole.free)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenOut)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(subject=user.email)
    # HttpOnly cookie for browser flows
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True, samesite="lax")
    return TokenOut(access_token=token)

