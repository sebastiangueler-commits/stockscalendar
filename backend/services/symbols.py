import os
import csv
from typing import List
import httpx


DATA_DIR = os.path.abspath("./data_cache")
NASDAQ_URL = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
OTHER_URL = "https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt"


def _ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def fetch_nasdaq_symbols() -> List[str]:
    _ensure_dir()
    path = os.path.join(DATA_DIR, "nasdaqlisted.txt")
    try:
        with httpx.Client(timeout=30) as client:
            r = client.get(NASDAQ_URL)
            r.raise_for_status()
            content = r.text
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception:
        pass
    syms: List[str] = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if "|" in line and not line.startswith("Symbol"):
                    sym = line.split("|")[0].strip()
                    if sym and sym.isupper() and "$" not in sym and sym != "File Creation Time":
                        syms.append(sym)
    return syms


def fetch_other_symbols() -> List[str]:
    _ensure_dir()
    path = os.path.join(DATA_DIR, "otherlisted.txt")
    try:
        with httpx.Client(timeout=30) as client:
            r = client.get(OTHER_URL)
            r.raise_for_status()
            content = r.text
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception:
        pass
    syms: List[str] = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if "|" in line and not line.startswith("ACT Symbol"):
                    sym = line.split("|")[0].strip()
                    if sym and sym.isupper() and "$" not in sym and sym != "File Creation Time":
                        syms.append(sym)
    return syms


def get_equity_symbols(limit: int | None = None) -> List[str]:
    syms = fetch_nasdaq_symbols() + fetch_other_symbols()
    # Deduplicate while preserving order
    seen = set()
    uniq: List[str] = []
    for s in syms:
        if s not in seen:
            uniq.append(s)
            seen.add(s)
    if limit:
        return uniq[:limit]
    return uniq


def get_commodity_symbols() -> List[str]:
    # Yahoo Finance futures symbols
    return [
        "GC=F", # Gold
        "SI=F", # Silver
        "PL=F", # Platinum
        "HG=F", # Copper
        "CL=F", # Crude Oil WTI
        "BZ=F", # Brent
        "NG=F", # Natural Gas
        "ZC=F", # Corn
        "ZW=F", # Wheat
        "ZS=F", # Soybeans
        "KC=F", # Coffee
        "SB=F", # Sugar
        "CT=F", # Cotton
    ]

