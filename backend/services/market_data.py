import os
from datetime import datetime
from typing import List, Dict
import pandas as pd
import yfinance as yf
from backend.config import settings


def fetch_price_history(symbol: str, start: str | None = None) -> pd.DataFrame:
    start = start or settings.HISTORICAL_START
    df = yf.download(symbol, start=start, progress=False, auto_adjust=True)
    if not isinstance(df, pd.DataFrame) or df.empty:
        return pd.DataFrame(columns=["Date", "Close"])  # fallback
    df = df.reset_index()
    return df[["Date", "Close"]]


def list_default_symbols() -> List[str]:
    # Minimal seed set; can be expanded with public symbol dumps
    equities = ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "TSLA", "META"]
    commodities = ["GC=F", "SI=F", "CL=F", "NG=F", "HG=F", "ZW=F", "ZC=F"]
    return equities + commodities


def compute_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    df["Return"] = df["Close"].pct_change()
    df["DayOfYear"] = pd.to_datetime(df["Date"]).dt.dayofyear
    df["Month"] = pd.to_datetime(df["Date"]).dt.month
    df["Day"] = pd.to_datetime(df["Date"]).dt.day
    df["Week"] = pd.to_datetime(df["Date"]).dt.isocalendar().week.astype(int)
    df["Quarter"] = pd.to_datetime(df["Date"]).dt.quarter
    return df.dropna()


def seasonal_stats(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "Return" not in df.columns:
        return pd.DataFrame(columns=["DayOfYear", "WinRate", "AvgReturn"])  # fallback
    grouped = df.groupby("DayOfYear")["Return"]
    stats = pd.DataFrame(
        {
            "DayOfYear": grouped.mean().index,
            "WinRate": (grouped.apply(lambda x: (x > 0).mean())).values,
            "AvgReturn": grouped.mean().values,
        }
    )
    return stats

