from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi import Form

from backend.database import get_db
from backend.models import User, UserRole, Payment
from backend.routers.auth import require_role
from backend.auth.security import hash_password


router = APIRouter()


@router.get("", response_class=HTMLResponse)
def admin_index(_: User = Depends(require_role(UserRole.admin)), db: Session = Depends(get_db)):
    users = db.query(User).all()
    payments = db.query(Payment).order_by(Payment.created_at.desc()).limit(50).all()
    # Simple HTML to keep dependencies minimal
    rows = "".join(
        f"<tr><td>{u.id}</td><td>{u.email}</td><td>{u.role}</td><td>{u.is_active}</td><td>{u.subscription_expires_at}</td></tr>"
        for u in users
    )
    pay_rows = "".join(
        f"<tr><td>{p.id}</td><td>{p.user_id}</td><td>{p.plan}</td><td>{p.amount} {p.currency}</td><td>{p.status}</td><td>{p.created_at}</td></tr>"
        for p in payments
    )
    html = f"""
    <html>
      <head>
        <title>Admin Dashboard</title>
        <style>
          body {{ font-family: Arial, sans-serif; padding: 20px; }}
          table, th, td {{ border: 1px solid #ccc; border-collapse: collapse; padding: 6px; }}
          table {{ width: 100%; margin-bottom: 24px; }}
        </style>
      </head>
      <body>
        <h1>Admin Dashboard</h1>
        <h2>Create User</h2>
        <form method="post" action="/admin/create-user">
          <input type="email" name="email" placeholder="email" required />
          <input type="password" name="password" placeholder="password" required />
          <select name="role">
            <option value="free">free</option>
            <option value="premium">premium</option>
            <option value="admin">admin</option>
          </select>
          <button type="submit">Create</button>
        </form>
        <h2>Users</h2>
        <table>
          <thead><tr><th>ID</th><th>Email</th><th>Role</th><th>Active</th><th>Expires</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
        <h2>Payments</h2>
        <table>
          <thead><tr><th>ID</th><th>User</th><th>Plan</th><th>Amount</th><th>Status</th><th>At</th></tr></thead>
          <tbody>{pay_rows}</tbody>
        </table>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


@router.post("/create-user")
def admin_create_user(
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form("free"),
    _: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    exists = db.query(User).filter(User.email == email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already exists")
    user = User(email=email, password_hash=hash_password(password), role=UserRole(role))
    db.add(user)
    db.commit()
    return {"status": "created", "user_id": user.id}


@router.post("/toggle-active/{user_id}")
def toggle_active(user_id: int, _: User = Depends(require_role(UserRole.admin)), db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    u.is_active = not u.is_active
    db.commit()
    return {"status": "ok", "is_active": u.is_active}


@router.post("/set-role/{user_id}")
def set_role(user_id: int, role: str, _: User = Depends(require_role(UserRole.admin)), db: Session = Depends(get_db)):
    if role not in ("free", "premium", "admin"):
        raise HTTPException(status_code=400, detail="Invalid role")
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    u.role = UserRole(role)
    db.commit()
    return {"status": "ok", "role": u.role}

