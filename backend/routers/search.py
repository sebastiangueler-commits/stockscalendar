import json
from datetime import datetime
from typing import List
import pandas as pd
from fastapi import APIRouter, HTTPException
from backend.services.market_data import fetch_price_history, compute_daily_returns


router = APIRouter()


@router.get("/search/{symbol}")
def search_symbol(symbol: str):
    # Load historical calendar
    try:
        with open("calendar_historical.json", "r", encoding="utf-8") as f:
            hist = json.load(f)
    except FileNotFoundError:
        hist = {"calendar_by_dayofyear": {}}

    # Load fundamental calendar
    try:
        with open("calendar_fundamental.json", "r", encoding="utf-8") as f:
            fund = json.load(f)
    except FileNotFoundError:
        fund = {"items": []}

    df = compute_daily_returns(fetch_price_history(symbol))
    if df.empty:
        raise HTTPException(status_code=404, detail="No data for symbol")

    # Score days by up_probability for this year
    this_year = datetime.utcnow().year
    df_year = df[pd.to_datetime(df["Date"]).dt.year == this_year] if "Date" in df.columns else df
    candidates = []
    for _, row in df_year.iterrows():
        doy = int(row["DayOfYear"]) if "DayOfYear" in row else None
        if doy is None:
            continue
        item = hist.get("calendar_by_dayofyear", {}).get(str(doy))
        if not item:
            continue
        candidates.append((row["Date"], item.get("up_probability", 0.5)))

    candidates.sort(key=lambda x: x[1], reverse=True)
    best_buy = [str(d.date()) for d, _ in candidates[:5]]
    best_sell = [str(d.date()) for d, _ in sorted(candidates[:5], key=lambda x: x[1])]  # naive opposite

    fund_item = next((i for i in fund.get("items", []) if i.get("symbol") == symbol), None)

    return {
        "symbol": symbol,
        "best_buy_dates": best_buy,
        "best_sell_dates": best_sell,
        "historical_stats": {"source": "calendar_historical.json"},
        "fundamental_status": fund_item or {"recommendation": "HOLD"},
    }

