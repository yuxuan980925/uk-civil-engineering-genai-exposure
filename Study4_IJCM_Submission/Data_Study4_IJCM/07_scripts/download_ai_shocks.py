#!/usr/bin/env python3
"""Download additional official AI-shock series. Never interpolate missing cells."""
from __future__ import annotations

import io
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

UA = "Study4-civil-engineering-research/1.0 (academic; eurostat/oecd/imf retrieval)"
GEOS = [
    "EU27_2020",
    "DE",
    "FR",
    "NL",
    "PL",
    "RO",
    "IT",
    "ES",
    "IE",
    "BE",
    "AT",
    "SE",
    "DK",
    "PT",
    "CZ",
    "HU",
    "FI",
    "EL",
]
NACES_EXTRA = ["C", "J", "K", "N"]  # manufacturing, ICT, finance, admin — placebos
INDICS = ["E_AI_TANY", "E_AI_TNLG", "E_AI_TML", "E_AI_TTM", "E_AI_TIR", "E_AI_TPVSG"]
YEARS = [2021, 2023, 2024, 2025]


def get(url: str, timeout: int = 60) -> bytes | None:
    req = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urlopen(req, timeout=timeout) as r:
            return r.read()
    except (HTTPError, URLError, TimeoutError, OSError) as e:
        print("FAIL", getattr(e, "code", ""), url[:140], str(e)[:80])
        return None


def eurostat_json(dataset: str, params: dict) -> dict | None:
    q = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{dataset}?format=JSON&lang=EN&{q}"
    raw = get(url)
    if not raw:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError:
        print("JSON fail", dataset, params)
        return None


def parse_eurostat(js: dict, extra: dict) -> list[dict]:
    if not js or "value" not in js:
        return []
    dim = js.get("dimension") or {}
    ids = js.get("id") or list(dim.keys())
    sizes = js.get("size") or [len(dim[k]["category"]["index"]) for k in ids]
    index_maps = []
    for k in ids:
        cat = dim[k]["category"]["index"]
        labels = dim[k]["category"].get("label", {})
        inv = {int(v): (kk, labels.get(kk, kk)) for kk, v in cat.items()}
        index_maps.append(inv)
    rows = []
    for pos, val in js["value"].items():
        pos = int(pos)
        coords = []
        rem = pos
        for s in reversed(sizes):
            coords.append(rem % s)
            rem //= s
        coords = list(reversed(coords))
        rec = dict(extra)
        rec["value"] = val
        for k, c in zip(ids, coords):
            code, lab = index_maps[ids.index(k)][c]
            rec[k] = code
            rec[f"{k}_label"] = lab
        rows.append(rec)
    return rows


def fetch_eurostat_nace_placebos():
    rows = []
    for nace in NACES_EXTRA:
        for indic in INDICS:
            js = eurostat_json(
                "isoc_eb_ain2",
                {
                    "size_emp": "GE10",
                    "nace_r2": nace,
                    "indic_is": indic,
                    "unit": "PC_ENT",
                },
            )
            recs = parse_eurostat(js, {"dataset": "isoc_eb_ain2"})
            keep = 0
            for r in recs:
                geo = r.get("geo")
                if geo not in GEOS:
                    continue
                time = r.get("time")
                try:
                    y = int(str(time)[:4])
                except (TypeError, ValueError):
                    continue
                if y not in YEARS:
                    continue
                rows.append(
                    {
                        "dataset": "isoc_eb_ain2",
                        "nace": nace,
                        "indic": indic,
                        "geo": geo,
                        "year": y,
                        "value": r["value"],
                        "unit": r.get("unit", "PC_ENT"),
                        "size_emp": "GE10",
                    }
                )
                keep += 1
            print("eurostat", nace, indic, "kept", keep, "raw", len(recs))
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.drop_duplicates(["nace", "indic", "geo", "year"])
        df.to_csv(DATA / "eurostat_ai_nace_placebos.csv", index=False)
    print("nace placebos", df.shape)
    return df


def fetch_owid():
    urls = [
        "https://ourworldindata.org/grapher/number-of-chatgpt-users.csv?v=1",
        "https://ourworldindata.org/grapher/chatgpt-monthly-users.csv?v=1",
        "https://catalog.ourworldindata.org/garden/artificial-intelligence/latest/ai_adoption/ai_adoption.csv",
        "https://catalog.ourworldindata.org/garden/technology/latest/artificial_intelligence/artificial_intelligence.csv",
        "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Artificial%20intelligence%20-%20AI%20Index%20Report/Artificial%20intelligence%20-%20AI%20Index%20Report.csv",
    ]
    notes = []
    for u in urls:
        raw = get(u, timeout=40)
        if not raw:
            notes.append({"url": u, "status": "fail"})
            continue
        text = raw.decode("utf-8", errors="replace")
        if text.lstrip().startswith("<") or "404" in text[:80].lower():
            notes.append({"url": u, "status": "html_or_404", "bytes": len(raw)})
            continue
        name = u.split("/")[-1].split("?")[0]
        if not name.endswith(".csv"):
            name = name + ".csv"
        path = DATA / f"owid_{name}"
        path.write_bytes(raw)
        notes.append({"url": u, "status": "ok", "file": path.name, "bytes": len(raw)})
        print("OWID saved", path, len(raw))
    pd.DataFrame(notes).to_csv(DATA / "owid_fetch_log.csv", index=False)


def fetch_imf_aipi():
    urls = [
        "https://www.imf.org/external/datamapper/api/v1/AIPI",
        "https://www.imf.org/external/datamapper/api/v1/AI_PREPAREDNESS",
        "https://www.imf.org/external/datamapper/datasets/AIPI",
    ]
    log = []
    for u in urls:
        raw = get(u, timeout=40)
        if not raw:
            log.append({"url": u, "status": "fail"})
            continue
        text = raw.decode("utf-8", errors="replace")
        if text.strip().startswith("{"):
            (DATA / "imf_aipi_raw.json").write_text(text)
            try:
                js = json.loads(text)
                (DATA / "imf_aipi_raw.json").write_text(json.dumps(js)[:20] and text)
            except json.JSONDecodeError:
                pass
            log.append({"url": u, "status": "ok_json", "bytes": len(raw)})
            print("IMF json", len(raw))
            break
        log.append({"url": u, "status": "not_json", "bytes": len(raw)})
    pd.DataFrame(log).to_csv(DATA / "imf_aipi_fetch_log.csv", index=False)


def fetch_oecd_ict_ai():
    """OECD ICT Access and Usage by Businesses — AI-related if published."""
    urls = [
        "https://sdmx.oecd.org/public/rest/data/OECD.STI.PIE,DSD_ICT_BUS@DF_ICT_BUS/..........AIBUS....?format=csvfilewithlabels",
        "https://sdmx.oecd.org/public/rest/data/OECD.STI.PIE,DSD_ICT_BUS@DF_ICT_BUS?format=csvfilewithlabels&startPeriod=2018&endPeriod=2024",
        "https://stats.oecd.org/SDMX-JSON/data/ICT_BUS/AIBUS+AIUSE.ENT.ALL.PC.A/all?contentType=csv",
    ]
    log = []
    for u in urls:
        raw = get(u, timeout=90)
        if not raw:
            log.append({"url": u[:180], "status": "fail"})
            continue
        if raw[:20].lstrip().startswith(b"<") or b"Error" in raw[:200]:
            log.append({"url": u[:180], "status": "xml_or_error", "bytes": len(raw)})
            continue
        try:
            df = pd.read_csv(io.BytesIO(raw))
        except Exception as e:
            log.append({"url": u[:180], "status": f"parse:{e}", "bytes": len(raw)})
            continue
        cols = " ".join(map(str, df.columns)).lower()
        # keep only if AI-related columns/values exist
        sample = df.head(400).astype(str).to_csv(index=False).lower()
        if "ai" not in cols and "artificial" not in sample and "aibus" not in sample:
            log.append({"url": u[:180], "status": "csv_no_ai_keyword", "rows": len(df)})
            continue
        out = DATA / "oecd_ict_bus_ai.csv"
        df.to_csv(out, index=False)
        log.append({"url": u[:180], "status": "ok", "rows": len(df), "file": out.name})
        print("OECD saved", df.shape)
        break
    pd.DataFrame(log).to_csv(DATA / "oecd_ict_fetch_log.csv", index=False)


def fetch_worldbank_digital():
    indicators = [
        "IT.NET.USER.ZS",  # internet users — context, not GenAI
        "IT.NET.BBND.P2",
        "GB.XPD.RSDV.GD.ZS",
    ]
    log = []
    for ind in indicators:
        url = f"https://api.worldbank.org/v2/country/all/indicator/{ind}?format=json&per_page=20000&date=2015:2025"
        raw = get(url, timeout=60)
        if not raw:
            log.append({"indicator": ind, "status": "fail"})
            continue
        try:
            js = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            log.append({"indicator": ind, "status": "not_json"})
            continue
        if not isinstance(js, list) or len(js) < 2:
            log.append({"indicator": ind, "status": "unexpected", "head": str(js)[:120]})
            continue
        rows = []
        for rec in js[1] or []:
            if rec.get("value") is None:
                continue
            rows.append(
                {
                    "indicator": ind,
                    "iso3": rec.get("countryiso3code"),
                    "country": (rec.get("country") or {}).get("value"),
                    "year": rec.get("date"),
                    "value": rec.get("value"),
                }
            )
        df = pd.DataFrame(rows)
        df.to_csv(DATA / f"wb_{ind.replace('.', '_')}.csv", index=False)
        log.append({"indicator": ind, "status": "ok", "rows": len(df)})
        print("WB", ind, df.shape)
    pd.DataFrame(log).to_csv(DATA / "wb_digital_fetch_log.csv", index=False)


def main():
    print("=== Eurostat extra NACE AI (C/J/K/N) ===")
    fetch_eurostat_nace_placebos()
    print("=== OWID ===")
    fetch_owid()
    print("=== IMF AIPI ===")
    fetch_imf_aipi()
    print("=== OECD ICT ===")
    fetch_oecd_ict_ai()
    print("=== World Bank digital context ===")
    fetch_worldbank_digital()
    print("done")


if __name__ == "__main__":
    main()
