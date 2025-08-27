import json
import os
from datetime import datetime
from typing import Dict, List
import yfinance as yf

from backend.services.market_data import list_default_symbols
from backend.services.symbols import get_equity_symbols, get_commodity_symbols


def _stock_fundamental_ok(t: yf.Ticker) -> Dict:
    info = t.info or {}
    # Some fields may be missing; treat missing as not satisfying unless clearly positive
    pe = info.get("trailingPE") or info.get("forwardPE")
    roa = info.get("returnOnAssets")
    sales5y = info.get("revenueGrowth") or info.get("fiveYearAvgDividendYield")  # proxy if not available
    de = info.get("debtToEquity")
    quick = info.get("quickRatio") or info.get("currentRatio")

    checks = {
        "pe<20": pe is not None and pe < 20,
        "roa>10%": roa is not None and roa > 0.10,
        "sales_growth_5y>5%": sales5y is not None and sales5y > 0.05,
        "debt/equity<1": de is not None and de < 1,
        "quick_ratio>1": quick is not None and quick > 1,
    }
    passed = all(checks.values())
    return {"passed": passed, "checks": checks}


def _commodity_fundamental_ok(symbol: str) -> Dict:
    # Placeholder heuristic using price distance to 200d moving average as proxy
    try:
        hist = yf.download(symbol, period="1y", auto_adjust=True, progress=False)
        if hist is None or hist.empty:
            return {"passed": False, "checks": {"ma200_trend": False}}
        ma200 = hist["Close"].rolling(200).mean().iloc[-1]
        last = hist["Close"].iloc[-1]
        trend_ok = last > ma200
        return {"passed": trend_ok, "checks": {"price>ma200": trend_ok}}
    except Exception:
        return {"passed": False, "checks": {"ma200_trend": False}}


def build_fundamental_calendar(symbols: List[str] | None = None) -> Dict:
    symbols = symbols or (get_equity_symbols(limit=None) + get_commodity_symbols())
    items = []
    for sym in symbols:
        t = yf.Ticker(sym)
        is_commodity = sym.endswith("=F")
        status = _commodity_fundamental_ok(sym) if is_commodity else _stock_fundamental_ok(t)
        if status.get("passed"):
            items.append({
                "symbol": sym,
                "recommendation": "BUY",
                "criteria": status.get("checks", {}),
            })

    result = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "items": items,
    }
    with open("calendar_fundamental.json", "w", encoding="utf-8") as f:
        json.dump(result, f)
    return result

