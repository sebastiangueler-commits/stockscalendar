import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from backend.services.fundamentals import build_fundamental_calendar
from backend.services.symbols import get_equity_symbols, get_commodity_symbols
from backend.config import settings


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
    # Bootstrap shortly after startup with a limited symbol set for quick availability
    def _bootstrap():
        try:
            limit = settings.FUNDAMENTAL_BOOTSTRAP_LIMIT or 200
            syms = get_equity_symbols(limit=limit) + get_commodity_symbols()
            build_fundamental_calendar(symbols=syms)
        except Exception as e:
            print(f"[scheduler] bootstrap build failed: {e}")

    _scheduler.add_job(_bootstrap, "date", run_date=datetime.utcnow() + timedelta(seconds=3))
    _scheduler.start()

