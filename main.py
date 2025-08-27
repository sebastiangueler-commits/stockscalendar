import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from backend.config import settings
from backend.database import init_db
from backend.routers import auth as auth_router
from backend.routers import calendars as calendars_router
from backend.routers import admin as admin_router
from backend.routers import stripe as stripe_router
from backend.routers import search as search_router
from backend.routers import signals as signals_router
from backend.routers import ops as ops_router
from backend.services.scheduler import scheduler_start
from backend.services.bootstrap import ensure_admin_user, ensure_seed_files


load_dotenv()

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and templates for admin dashboard
app.mount("/static", StaticFiles(directory="backend/static"), name="static")
templates = Jinja2Templates(directory="backend/templates")


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    ensure_seed_files()
    ensure_admin_user()
    scheduler_start()


# Routers
app.include_router(auth_router.router, prefix="", tags=["auth"]) 
app.include_router(calendars_router.router, prefix="/calendar", tags=["calendar"]) 
app.include_router(search_router.router, prefix="", tags=["search"]) 
app.include_router(signals_router.router, prefix="", tags=["signals"]) 
app.include_router(stripe_router.router, prefix="/stripe", tags=["stripe"]) 
app.include_router(admin_router.router, prefix="/admin", tags=["admin"]) 
app.include_router(ops_router.router, prefix="", tags=["ops"]) 


@app.get("/frontend-data")
def frontend_data():
    return {
        "app": settings.APP_NAME,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "endpoints": [
            "/calendar/historical",
            "/calendar/fundamental",
            "/signals/{date}",
            "/search/{symbol}",
        ],
    }

