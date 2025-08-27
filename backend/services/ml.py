import json
import os
from datetime import datetime
from typing import Dict, List
import numpy as np
import pandas as pd
try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False
from joblib import dump, load

from backend.services.market_data import fetch_price_history, compute_daily_returns, seasonal_stats, list_default_symbols


MODEL_PATH = os.path.abspath("./data_cache/rf_model.joblib")


def train_historical_calendar(symbols: List[str] | None = None) -> Dict:
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    symbols = symbols or list_default_symbols()

    features = []
    labels = []

    for sym in symbols:
        df = fetch_price_history(sym)
        df = compute_daily_returns(df)
        if df.empty:
            continue
        # Label: next-day up/down
        df["Target"] = (df["Return"].shift(-1) > 0).astype(int)
        df = df.dropna()
        X = df[["DayOfYear", "Month", "Week", "Quarter"]].values
        y = df["Target"].values
        features.append(X)
        labels.append(y)

    if not features:
        return {"status": "no_data"}

    X_all = np.vstack(features)
    y_all = np.concatenate(labels)

    if SKLEARN_AVAILABLE:
        X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.2, random_state=42)
        clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        acc = float(accuracy_score(y_test, y_pred))
        dump(clf, MODEL_PATH)
    else:
        # Fallback heuristic when scikit-learn wheels are unavailable: use average by day-of-year
        acc = None
        clf = None

    # Build calendar by day-of-year signal using model probabilities
    calendar = {}
    if SKLEARN_AVAILABLE:
        for day in range(1, 367):
            sample = np.array([[day, 1 + (day % 12), 1 + (day % 52), 1 + (day % 4)]])
            proba = clf.predict_proba(sample)[0][1]
            signal = "BUY" if proba >= 0.53 else ("SELL" if proba <= 0.47 else "HOLD")
            calendar[str(day)] = {"signal": signal, "up_probability": round(proba, 4)}
    else:
        # Heuristic: BUY if average return for day-of-year across symbols > 0
        doy_returns: dict[int, list[float]] = {}
        for sym in symbols:
            df = compute_daily_returns(fetch_price_history(sym))
            for _, row in df.iterrows():
                d = int(row["DayOfYear"]) if "DayOfYear" in row else None
                r = float(row["Return"]) if "Return" in row else 0.0
                if not d:
                    continue
                doy_returns.setdefault(d, []).append(r)
        for day in range(1, 367):
            arr = doy_returns.get(day, [])
            avg = float(np.mean(arr)) if arr else 0.0
            proba = 0.55 if avg > 0 else 0.45 if avg < 0 else 0.5
            signal = "BUY" if proba >= 0.53 else ("SELL" if proba <= 0.47 else "HOLD")
            calendar[str(day)] = {"signal": signal, "up_probability": round(proba, 4)}

    result = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "model_accuracy": acc,
        "calendar_by_dayofyear": calendar,
    }
    with open("calendar_historical.json", "w", encoding="utf-8") as f:
        json.dump(result, f)
    return result


def load_model():
    if os.path.exists(MODEL_PATH):
        return load(MODEL_PATH)
    return None

