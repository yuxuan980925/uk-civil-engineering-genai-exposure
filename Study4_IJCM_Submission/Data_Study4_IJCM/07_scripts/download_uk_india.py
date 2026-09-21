#!/usr/bin/env python3
"""Re-collect official UK–India series only. Never interpolate missing cells.

Sources
-------
- OECD–WTO BaTIS: GBR↔IND for SJ3, SE, SI, SJ1, SJ2; adjustments B and N.
- BaTIS world counterpart `W` for UK and Indian totals (import shares).
- World Bank WDI: GDP, services share, industry share (context, not the shock).
- ONS Pink Book API is decommissioned in this environment (logged, not filled).
"""
from __future__ import annotations

import io
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "10_uk_india"
OUT.mkdir(exist_ok=True)
UA = "Study4-uk-india/1.0 (academic; oecd/worldbank retrieval)"
BASE = "https://sdmx.oecd.org/public/rest/v1/data/OECD.SDD.TPS,DSD_BATIS@DF_BATIS,1.0/"
PAIRS = [("GBR", "IND"), ("IND", "GBR"), ("GBR", "W"), ("IND", "W")]
SERVICES = ["SJ3", "SE", "SI", "SJ1", "SJ2"]
ADJUST = ["B", "N"]


def get(url: str, accept: str = "*/*", timeout: int = 60) -> bytes | None:
    req = Request(url, headers={"User-Agent": UA, "Accept": accept})
    try:
        with urlopen(req, timeout=timeout) as r:
            return r.read()
    except (HTTPError, URLError, TimeoutError, OSError) as e:
        print("FAIL", getattr(e, "code", ""), url[-90:], str(e)[:70])
        return None


def fetch_batis():
    log, frames = [], []
    for ref, cpt in PAIRS:
        for svc in SERVICES:
            for adj in ADJUST:
                key = f"{ref}.{cpt}.M.S.{svc}.A.USD_EXC.{adj}"
                url = BASE + key + "?startPeriod=2015&endPeriod=2024"
                raw = get(url, accept="text/csv")
                if not raw or raw.lstrip().startswith(b"<") or raw.lstrip().startswith(b"No"):
                    log.append({"key": key, "status": "fail_or_empty", "bytes": 0 if not raw else len(raw)})
                    print("BaTIS miss", key)
                    continue
                try:
                    df = pd.read_csv(io.BytesIO(raw))
                except Exception as e:
                    log.append({"key": key, "status": f"parse:{e}", "bytes": len(raw)})
                    continue
                if df.empty:
                    log.append({"key": key, "status": "empty_csv"})
                    continue
                df["source_key"] = key
                frames.append(df)
                log.append({"key": key, "status": "ok", "rows": len(df)})
                print("BaTIS", key, len(df))
    out = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if not out.empty:
        keep = [c for c in [
            "REF_AREA", "COUNTERPART_AREA", "TRADE_FLOW", "SERVICE",
            "TIME_PERIOD", "OBS_VALUE", "ADJUSTMENT", "UNIT_MEASURE",
            "OBS_STATUS", "source_key",
        ] if c in out.columns]
        out = out[keep].sort_values(
            ["ADJUSTMENT", "REF_AREA", "COUNTERPART_AREA", "SERVICE", "TIME_PERIOD"]
        )
        out.to_csv(OUT / "batis_uk_india.csv", index=False)
    pd.DataFrame(log).to_csv(OUT / "batis_uk_india_fetch_log.csv", index=False)
    print("BaTIS saved", out.shape)
    return out


def fetch_wb():
    inds = [
        "NY.GDP.MKTP.CD",
        "NV.SRV.TOTL.ZS",
        "NV.IND.TOTL.ZS",
        "GB.XPD.RSDV.GD.ZS",
        "NE.EXP.GNFS.ZS",
    ]
    log, rows = [], []
    for ind in inds:
        url = (
            f"https://api.worldbank.org/v2/country/GBR;IND/indicator/{ind}"
            f"?format=json&per_page=200&date=2015:2025"
        )
        raw = get(url, timeout=50)
        if not raw:
            log.append({"indicator": ind, "status": "fail"})
            continue
        try:
            js = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            log.append({"indicator": ind, "status": "not_json"})
            continue
        recs = js[1] if isinstance(js, list) and len(js) > 1 else []
        n = 0
        for rec in recs or []:
            if rec.get("value") is None:
                continue
            rows.append({
                "indicator": ind,
                "iso3": rec.get("countryiso3code"),
                "country": (rec.get("country") or {}).get("value"),
                "year": int(rec["date"]) if str(rec.get("date", "")).isdigit() else rec.get("date"),
                "value": rec.get("value"),
            })
            n += 1
        log.append({"indicator": ind, "status": "ok", "rows": n})
        print("WB", ind, n)
    df = pd.DataFrame(rows)
    if not df.empty:
        df.to_csv(OUT / "wb_uk_india.csv", index=False)
    pd.DataFrame(log).to_csv(OUT / "wb_uk_india_fetch_log.csv", index=False)
    return df


def log_ons():
    url = "https://api.ons.gov.uk/search?q=pink%20book"
    raw = get(url, timeout=20)
    status = "decommissioned_or_fail"
    head = ""
    if raw:
        head = raw[:180].decode("utf-8", errors="replace")
        if "decommissioned" in head.lower():
            status = "decommissioned"
        elif raw[:1] == b"{":
            status = "json"
    pd.DataFrame([{"url": url, "status": status, "head": head}]).to_csv(
        OUT / "ons_pinkbook_fetch_log.csv", index=False
    )
    print("ONS", status)


def main():
    print("=== BaTIS UK–India ===")
    fetch_batis()
    print("=== World Bank UK–India ===")
    fetch_wb()
    print("=== ONS ===")
    log_ons()
    print("done")


if __name__ == "__main__":
    main()
