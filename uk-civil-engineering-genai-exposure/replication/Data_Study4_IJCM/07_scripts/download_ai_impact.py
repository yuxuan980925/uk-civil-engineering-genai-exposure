#!/usr/bin/env python3
"""Retrieve official series for the redesigned AI-shock *impact* study.

Never interpolate missing cells. Empty cubes are logged.

New objects (on top of files already in 01–03 and 09)
----------------------------------------------------
1. Eurostat TNLG by enterprise size class (NACE M and F).
2. Job-vacancy rates by NACE (jvs_a_nace2).
3. National-accounts hours worked for M71/F/M (nama_10_a64_e).
4. Short-term turnover index for M71 if published.
5. Re-pull of EU-27 TNLG 2021–25 (shock description).
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "11_ai_shock_impact"
OUT.mkdir(exist_ok=True)

UA = "Study4-ai-impact/1.0 (academic; eurostat retrieval)"
GEOS = [
    "EU27_2020",
    "DE", "FR", "NL", "PL", "RO", "IT", "ES", "IE", "BE", "AT",
    "SE", "DK", "PT", "CZ", "HU", "FI", "EL",
]
NACES = ["M71", "F", "M", "M7112", "M7111"]
SIZE_CANDIDATES = [
    "GE10", "10TO49", "50TO249", "GE250",
    "FROM_10_TO_49", "FROM_50_TO_249", "FROM10TO49", "FROM50TO249",
]
YEARS_AI = [2021, 2023, 2024, 2025]


def get(url: str, timeout: int = 90) -> bytes | None:
    req = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urlopen(req, timeout=timeout) as r:
            return r.read()
    except (HTTPError, URLError, TimeoutError, OSError) as e:
        print("FAIL", getattr(e, "code", ""), url[-110:], str(e)[:70])
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


def year_of(rec) -> int | None:
    try:
        return int(str(rec.get("time"))[:4])
    except (TypeError, ValueError):
        return None


def fetch_tnlg_size():
    log, rows = [], []
    sizes_ok = []
    # Probe which size codes exist for NACE M, TNLG, one year.
    for size in SIZE_CANDIDATES:
        js = eurostat_json(
            "isoc_eb_ain2",
            {
                "size_emp": size,
                "nace_r2": "M",
                "indic_is": "E_AI_TNLG",
                "unit": "PC_ENT",
                "geo": "DE",
                "time": "2024",
            },
        )
        recs = parse_eurostat(js) if js else []
        if recs:
            sizes_ok.append(size)
            log.append({"object": "size_probe", "size_emp": size, "status": "ok", "n": len(recs)})
            print("size class exists", size)
        else:
            log.append({"object": "size_probe", "size_emp": size, "status": "empty"})
            print("size class empty", size)

    for size in sizes_ok:
        for nace in ["M", "F"]:
            for indic in ["E_AI_TNLG", "E_AI_TANY"]:
                js = eurostat_json(
                    "isoc_eb_ain2",
                    {
                        "size_emp": size,
                        "nace_r2": nace,
                        "indic_is": indic,
                        "unit": "PC_ENT",
                    },
                )
                recs = parse_eurostat(js) if js else []
                keep = 0
                for r in recs:
                    if r.get("geo") not in GEOS:
                        continue
                    y = year_of(r)
                    if y not in YEARS_AI:
                        continue
                    rows.append({
                        "dataset": "isoc_eb_ain2",
                        "nace": nace,
                        "indic": indic,
                        "size_emp": size,
                        "geo": r["geo"],
                        "year": y,
                        "value": r["value"],
                        "unit": r.get("unit", "PC_ENT"),
                    })
                    keep += 1
                log.append({
                    "object": "tnlg_size", "size_emp": size, "nace": nace,
                    "indic": indic, "status": "ok" if keep else "empty", "n": keep,
                })
                print("TNLG size", size, nace, indic, keep)

    df = pd.DataFrame(rows)
    if not df.empty:
        df.to_csv(OUT / "eurostat_tnlg_sizeclass.csv", index=False)
    pd.DataFrame(log).to_csv(OUT / "tnlg_sizeclass_fetch_log.csv", index=False)
    print("size-class saved", df.shape)
    return df


def fetch_vacancies():
    """Annual job-vacancy *rates* (jvs_a_rate_r2). M71 is unpublished; M and F exist."""
    log, rows = [], []
    for nace in ["M71", "M", "F", "M_N"]:
        js = eurostat_json(
            "jvs_a_rate_r2",
            {"nace_r2": nace, "sizeclas": "TOTAL", "unit": "AVG_A"},
        )
        recs = parse_eurostat(js) if js else []
        keep = 0
        for r in recs:
            if r.get("geo") not in GEOS:
                continue
            y = year_of(r)
            if y is None or y < 2018 or y > 2025:
                continue
            rows.append({
                "dataset": "jvs_a_rate_r2",
                "nace": nace,
                "indic": "JVR",
                "unit": r.get("unit", "AVG_A"),
                "sizeclas": r.get("sizeclas", "TOTAL"),
                "geo": r["geo"],
                "year": y,
                "value": r["value"],
            })
            keep += 1
        log.append({
            "object": "jvs_a_rate_r2", "nace": nace,
            "status": "ok" if keep else "empty", "n": keep, "raw": len(recs),
        })
        print("JVR", nace, keep)
    df = pd.DataFrame(rows)
    if not df.empty:
        df.to_csv(OUT / "eurostat_job_vacancies.csv", index=False)
    pd.DataFrame(log).to_csv(OUT / "job_vacancies_fetch_log.csv", index=False)
    print("vacancies saved", df.shape)
    return df


def fetch_hours():
    log, rows = [], []
    # Probe units / items.
    probes = [
        {"unit": "THS_HW", "na_item": "EMP_DC"},
        {"unit": "THS_HW", "na_item": "SAL_DC"},
        {"unit": "THS_HW", "na_item": "EMP"},
        {"unit": "HW", "na_item": "EMP_DC"},
        {"unit": "THS_PER", "na_item": "EMP_DC"},
    ]
    ok_params = []
    for p in probes:
        js = eurostat_json(
            "nama_10_a64_e",
            {"nace_r2": "M71", "geo": "DE", "time": "2022", **p},
        )
        recs = parse_eurostat(js) if js else []
        status = "ok" if recs else "empty"
        log.append({"object": "hours_probe", **p, "status": status, "n": len(recs)})
        print("hours probe", p, status, len(recs))
        if recs:
            ok_params.append(p)

    for p in ok_params:
        for nace in ["M71", "F", "M"]:
            js = eurostat_json("nama_10_a64_e", {"nace_r2": nace, **p})
            recs = parse_eurostat(js) if js else []
            keep = 0
            for r in recs:
                if r.get("geo") not in GEOS:
                    continue
                y = year_of(r)
                if y is None or y < 2015 or y > 2025:
                    continue
                rows.append({
                    "dataset": "nama_10_a64_e",
                    "nace": nace,
                    "unit": p["unit"],
                    "na_item": p["na_item"],
                    "geo": r["geo"],
                    "year": y,
                    "value": r["value"],
                })
                keep += 1
            log.append({
                "object": "hours", "nace": nace, **p,
                "status": "ok" if keep else "empty", "n": keep,
            })
            print("hours", nace, p, keep)
    df = pd.DataFrame(rows)
    # Thousand hours (THS_HW) is the hours object. THS_PER is persons, already in SBS.
    hw = df[df.unit == "THS_HW"] if not df.empty and "unit" in df.columns else pd.DataFrame()
    if not hw.empty:
        hw.to_csv(OUT / "eurostat_hours_M71_F_M.csv", index=False)
    if not df.empty:
        df.to_csv(OUT / "eurostat_nama_employment_persons.csv", index=False)
    pd.DataFrame(log).to_csv(OUT / "hours_fetch_log.csv", index=False)
    print("hours THS_HW saved", hw.shape if not hw.empty else (0, 0), "persons", df.shape)
    return df


def fetch_sts():
    log, rows = [], []
    datasets = [
        ("sts_setu_a", {"nace_r2": "M71", "indic_bt": "NETTUR", "s_adj": "NSA", "unit": "I21"}),
        ("sts_setu_a", {"nace_r2": "M", "indic_bt": "NETTUR", "s_adj": "NSA", "unit": "I21"}),
        ("sts_setu_a", {"nace_r2": "M71", "indic_bt": "VOL_SLS", "s_adj": "NSA", "unit": "I21"}),
    ]
    for dataset, params in datasets:
        js = eurostat_json(dataset, params)
        recs = parse_eurostat(js) if js else []
        keep = 0
        for r in recs:
            if r.get("geo") not in GEOS:
                continue
            y = year_of(r)
            if y is None or y < 2018 or y > 2025:
                continue
            rows.append({
                "dataset": dataset,
                "nace": params.get("nace_r2"),
                "indic": params.get("indic_bt"),
                "unit": params.get("unit"),
                "s_adj": params.get("s_adj"),
                "geo": r["geo"],
                "year": y,
                "value": r["value"],
            })
            keep += 1
        log.append({
            "object": "sts", "dataset": dataset, **params,
            "status": "ok" if keep else "empty", "n": keep, "raw": len(recs),
        })
        print("STS", dataset, params.get("nace_r2"), keep)
    df = pd.DataFrame(rows)
    if not df.empty:
        df.to_csv(OUT / "eurostat_sts_turnover.csv", index=False)
    pd.DataFrame(log).to_csv(OUT / "sts_fetch_log.csv", index=False)
    print("sts saved", df.shape)
    return df


def fetch_eu27_tnlg():
    rows = []
    for nace in ["M", "F"]:
        for indic in ["E_AI_TNLG", "E_AI_TANY", "E_AI_TML"]:
            js = eurostat_json(
                "isoc_eb_ain2",
                {
                    "size_emp": "GE10",
                    "nace_r2": nace,
                    "indic_is": indic,
                    "unit": "PC_ENT",
                    "geo": "EU27_2020",
                },
            )
            recs = parse_eurostat(js) if js else []
            for r in recs:
                y = year_of(r)
                if y not in YEARS_AI:
                    continue
                rows.append({
                    "nace": nace, "indic": indic, "geo": "EU27_2020",
                    "year": y, "value": r["value"],
                })
            print("EU27", nace, indic, len(recs))
    df = pd.DataFrame(rows)
    if not df.empty:
        df.to_csv(OUT / "eurostat_eu27_tnlg.csv", index=False)
    print("EU27 TNLG saved", df.shape)
    return df


def main():
    print("=== size-class TNLG ===")
    fetch_tnlg_size()
    print("=== job vacancies ===")
    fetch_vacancies()
    print("=== hours ===")
    fetch_hours()
    print("=== STS ===")
    fetch_sts()
    print("=== EU-27 TNLG ===")
    fetch_eu27_tnlg()
    print("done")


if __name__ == "__main__":
    main()
