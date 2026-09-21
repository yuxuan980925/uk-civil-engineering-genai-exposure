#!/usr/bin/env python3
"""Re-collect official series that can corroborate the *association*
conclusion (Indian engineering services vs Chinese construction/engineering;
M71/M7112 employment not falling). Never interpolate missing cells.

New objects
-----------
1. Eurostat SBS NACE **M7112** engineering activities and related technical
   consultancy (tighter than M71). M7111 = architecture; M712 = testing.
2. Eurostat ITS SJ312 for **placebo partners** (US, UK, CH, JP) and extra-EU.
   If NLG also predicts US/UK engineering imports, the India result is not a
   supplier-mix shift.
3. Independent re-fetch of India / China-except-HK SJ312 (verify the prior pull).
4. Inward FATS (`fats_g1a_08`) M71 by controlling country. Ends in 2020
   (pre-ChatGPT); India unpublished. Documents that Mode-3 affiliate presence
   cannot be tested in the NLG window.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "09_relocation_probe"
OUT.mkdir(exist_ok=True)

UA = "Study4-corroboration/1.0 (academic; eurostat retrieval)"
GEOS = [
    "EU27_2020",
    "DE", "FR", "NL", "PL", "RO", "IT", "ES", "IE", "BE", "AT",
    "SE", "DK", "PT", "CZ", "HU", "FI", "EL", "UK",
]
YEARS = list(range(2015, 2025))
NACES = ["M7112", "M7111", "M711", "M712", "M71"]
SBS_KEEP = {
    "EMP_NR", "SAL_NR", "AV_MEUR", "VAL_OUT_MEUR", "WAGE_MEUR",
    "GOS_MEUR", "ENT_NR", "NETTUR_MEUR",
}


def get(url: str, timeout: int = 90) -> bytes | None:
    req = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urlopen(req, timeout=timeout) as r:
            return r.read()
    except (HTTPError, URLError, TimeoutError, OSError) as e:
        print("FAIL", getattr(e, "code", ""), url[:140], str(e)[:80])
        return None


def eurostat_json(dataset: str, params: dict) -> dict | None:
    q = "&".join(f"{k}={v}" for k, v in params.items())
    url = (
        f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
        f"{dataset}?format=JSON&lang=EN&{q}"
    )
    raw = get(url)
    if not raw:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError:
        print("JSON fail", dataset, params)
        return None


def parse_eurostat(js: dict) -> list[dict]:
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
        rec = {"value": val}
        for k, c in zip(ids, coords):
            code, lab = index_maps[ids.index(k)][c]
            rec[k] = code
            rec[f"{k}_label"] = lab
        rows.append(rec)
    return rows


def fetch_sbs_engineering():
    log, rows = [], []
    for dataset, extra in [
        ("sbs_ovw_act", {}),
        ("sbs_sc_ovw", {"size_emp": "TOTAL"}),
    ]:
        for nace in NACES:
            params = {"nace_r2": nace, **extra}
            js = eurostat_json(dataset, params)
            recs = parse_eurostat(js) if js else []
            keep = 0
            for r in recs:
                geo = r.get("geo")
                if geo not in GEOS:
                    continue
                indic = r.get("indic_sbs")
                if indic not in SBS_KEEP:
                    continue
                try:
                    y = int(str(r.get("time"))[:4])
                except (TypeError, ValueError):
                    continue
                if y < 2021:
                    continue
                rows.append(
                    {
                        "dataset": dataset,
                        "nace": r.get("nace_r2", nace),
                        "nace_label": r.get("nace_r2_label"),
                        "indic": indic,
                        "indic_label": r.get("indic_sbs_label"),
                        "geo": geo,
                        "year": y,
                        "value": r["value"],
                    }
                )
                keep += 1
            status = "ok" if recs else ("empty" if js else "fail")
            log.append({"dataset": dataset, "nace": nace, "status": status,
                        "raw": len(recs), "kept": keep})
            print("SBS", dataset, nace, status, "kept", keep, "raw", len(recs))
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.drop_duplicates(["dataset", "nace", "indic", "geo", "year"])
        df.to_csv(OUT / "eurostat_sbs_M7112_engineering.csv", index=False)
    pd.DataFrame(log).to_csv(OUT / "sbs_m7112_fetch_log.csv", index=False)
    print("SBS engineering saved", df.shape)
    return df


def fetch_its_partners(partners, outfile, logname):
    log, rows = [], []
    for partner in partners:
        for flow in ("DEB", "CRE"):
            js = eurostat_json(
                "bop_its6_det",
                {
                    "bop_item": "SJ312",
                    "stk_flow": flow,
                    "partner": partner,
                    "currency": "MIO_EUR",
                },
            )
            recs = parse_eurostat(js) if js else []
            keep = 0
            for r in recs:
                try:
                    y = int(str(r.get("time"))[:4])
                except (TypeError, ValueError):
                    continue
                if y not in YEARS or r.get("geo") not in GEOS:
                    continue
                rows.append(
                    {
                        "dataset": "bop_its6_det",
                        "bop_item": r.get("bop_item", "SJ312"),
                        "stk_flow": r.get("stk_flow", flow),
                        "partner": r.get("partner", partner),
                        "geo": r.get("geo"),
                        "year": y,
                        "currency": r.get("currency", "MIO_EUR"),
                        "value": r["value"],
                    }
                )
                keep += 1
            status = "ok" if recs else ("empty" if js else "fail")
            log.append({"partner": partner, "stk_flow": flow, "status": status,
                        "raw": len(recs), "kept": keep})
            print("ITS SJ312", partner, flow, status, "kept", keep, "raw", len(recs))
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.drop_duplicates(["bop_item", "stk_flow", "partner", "geo", "year"])
        df.to_csv(OUT / outfile, index=False)
    pd.DataFrame(log).to_csv(OUT / logname, index=False)
    print("ITS saved", outfile, df.shape)
    return df


def fetch_fats():
    log, rows = [], []
    for ctrl in ["IN", "CN_X_HK", "US", "WORLD", "WRL_X_REP", "EXT_EU27_2020"]:
        for indic in ["V16110", "V12110", "V11110"]:
            js = eurostat_json(
                "fats_g1a_08",
                {"nace_r2": "M71", "c_ctrl": ctrl, "indic_sb": indic},
            )
            recs = parse_eurostat(js) if js else []
            keep = 0
            for r in recs:
                geo = r.get("geo")
                if geo not in GEOS and geo not in {"EU27_2020", "EU28"}:
                    continue
                try:
                    y = int(str(r.get("time"))[:4])
                except (TypeError, ValueError):
                    continue
                rows.append(
                    {
                        "dataset": "fats_g1a_08",
                        "nace": r.get("nace_r2", "M71"),
                        "indic": r.get("indic_sb", indic),
                        "indic_label": r.get("indic_sb_label"),
                        "c_ctrl": r.get("c_ctrl", ctrl),
                        "c_ctrl_label": r.get("c_ctrl_label"),
                        "geo": geo,
                        "year": y,
                        "value": r["value"],
                    }
                )
                keep += 1
            status = "ok" if recs else ("empty" if js else "fail")
            log.append({"c_ctrl": ctrl, "indic": indic, "status": status,
                        "raw": len(recs), "kept": keep,
                        "max_year": max((r.get("year") for r in rows if r.get("c_ctrl") == ctrl), default=None)})
            print("FATS", ctrl, indic, status, "kept", keep, "raw", len(recs))
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.drop_duplicates(["nace", "indic", "c_ctrl", "geo", "year"])
        df.to_csv(OUT / "eurostat_fats_M71.csv", index=False)
    pd.DataFrame(log).to_csv(OUT / "fats_m71_fetch_log.csv", index=False)
    print("FATS saved", df.shape)
    return df


def main():
    print("=== SBS M7112 engineering consultancy ===")
    fetch_sbs_engineering()
    print("=== ITS SJ312 re-fetch IN / CN_X_HK ===")
    fetch_its_partners(
        ["IN", "CN_X_HK"],
        "eurostat_its_sj312_refetch.csv",
        "its_sj312_refetch_log.csv",
    )
    print("=== ITS SJ312 placebo partners ===")
    fetch_its_partners(
        ["US", "UK", "CH", "JP", "EXT_EU27_2020"],
        "eurostat_its_sj312_placebos.csv",
        "its_sj312_placebo_log.csv",
    )
    print("=== FATS inward M71 by controlling country ===")
    fetch_fats()
    print("done")


if __name__ == "__main__":
    main()
