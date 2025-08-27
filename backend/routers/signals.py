import json
from datetime import datetime
from fastapi import APIRouter, HTTPException


router = APIRouter()


@router.get("/signals/{date}")
def signals_for_date(date: str):
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, expected YYYY-MM-DD")

    day = dt.timetuple().tm_yday
    try:
        with open("calendar_historical.json", "r", encoding="utf-8") as f:
            hist = json.load(f)
    except FileNotFoundError:
        hist = {"calendar_by_dayofyear": {}}

    try:
        with open("calendar_fundamental.json", "r", encoding="utf-8") as f:
            fund = json.load(f)
    except FileNotFoundError:
        fund = {"items": []}

    hist_signal = hist.get("calendar_by_dayofyear", {}).get(str(day), {})
    return {
        "date": date,
        "historical": hist_signal,
        "fundamental": fund.get("items", []),
    }

