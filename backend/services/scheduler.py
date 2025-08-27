import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from backend.services.fundamentals import build_fundamental_calendar


_scheduler: BackgroundScheduler | None = None


def _daily_job():
    try:
        build_fundamental_calendar()
    except Exception as e:
        # In production, use proper logging
        print(f"[scheduler] daily fundamental build failed: {e}")


def scheduler_start() -> None:
    global _scheduler
    if _scheduler is not None:
        return
    _scheduler = BackgroundScheduler(timezone="UTC")
    _scheduler.add_job(_daily_job, "cron", hour=2, minute=0)  # daily at 02:00 UTC
    _scheduler.start()

