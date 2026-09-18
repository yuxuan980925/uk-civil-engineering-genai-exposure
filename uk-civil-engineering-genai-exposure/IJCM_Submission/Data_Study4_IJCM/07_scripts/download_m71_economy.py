#!/usr/bin/env python3
"""Download official civil-industry *economy* series (M71 vs F), not occupation LLM scores.

Shock remains Eurostat TNLG. Outcomes: SBS turnover/employment/wages/VA/GOS,
nama compensation, ILO M71 if published, BLS NAICS 54133 if public API allows.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
UA = "Study4-civil-industry-economy/1.0"
GEOS = [
    "EU27_2020", "DE", "FR", "NL", "PL", "RO", "IT", "ES", "IE", "BE", "AT",
    "SE", "DK", "PT", "CZ", "HU", "FI", "EL",
]


def get(url: str, timeout: int = 90) -> bytes | None:
    req = Request(url, headers={"User-Agent": UA, "Accept": "application/json,*/*"})
    try:
        with urlopen(req, timeout=timeout) as r:
            return r.read()
    except (HTTPError, URLError, TimeoutError, OSError) as e:
        print("FAIL", getattr(e, "code", ""), url[:130], str(e)[:80])
        return None


def eurostat_json(dataset: str, params: dict) -> dict | None:
    q = "&".join(f"{k}={v}" for k, v in params.items())
    url = (
        f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{dataset}"
        f"?format=JSON&lang=EN&{q}"
    )
    raw = get(url)
    if not raw:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError:
        print("JSON fail", dataset)
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


def fetch_sbs():
    rows = []
    # Overview (no size class): employment, VA, wages, GOS, output
    for nace in ["M71", "F", "M"]:
        js = eurostat_json("sbs_ovw_act", {"nace_r2": nace})
        recs = parse_eurostat(js)
        keep_ind = {
            "EMP_NR", "SAL_NR", "AV_MEUR", "VAL_OUT_MEUR", "WAGE_MEUR",
            "GOS_MEUR", "LABPRY_TEUR", "LC_EMP_TEUR", "ENT_NR",
        }
        n = 0
        for r in recs:
            if r.get("geo") not in GEOS:
                continue
            if r.get("indic_sbs") not in keep_ind:
                continue
            try:
                y = int(str(r.get("time"))[:4])
            except (TypeError, ValueError):
                continue
            rows.append(
                {
                    "dataset": "sbs_ovw_act",
                    "nace": nace,
                    "indic": r["indic_sbs"],
                    "indic_label": r.get("indic_sbs_label"),
                    "geo": r["geo"],
                    "year": y,
                    "value": r["value"],
                }
            )
            n += 1
        print("sbs_ovw_act", nace, "kept", n, "raw", len(recs))

    # Size-class TOTAL: net turnover
    for nace in ["M71", "F", "M"]:
        js = eurostat_json("sbs_sc_ovw", {"nace_r2": nace, "size_emp": "TOTAL"})
        recs = parse_eurostat(js)
        keep_ind = {"NETTUR_MEUR", "EMP_NR", "AV_MEUR", "WAGE_MEUR", "GOS_MEUR"}
        n = 0
        for r in recs:
            if r.get("geo") not in GEOS:
                continue
            if r.get("indic_sbs") not in keep_ind:
                continue
            try:
                y = int(str(r.get("time"))[:4])
            except (TypeError, ValueError):
                continue
            rows.append(
                {
                    "dataset": "sbs_sc_ovw",
                    "nace": nace,
                    "indic": r["indic_sbs"],
                    "indic_label": r.get("indic_sbs_label"),
                    "geo": r["geo"],
                    "year": y,
                    "value": r["value"],
                }
            )
            n += 1
        print("sbs_sc_ovw", nace, "kept", n, "raw", len(recs))

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.drop_duplicates(["dataset", "nace", "indic", "geo", "year"])
        df.to_csv(DATA / "eurostat_sbs_M71_F_M.csv", index=False)
    print("SBS", df.shape)
    return df


def fetch_nama_income():
    rows = []
    for item, unit in [("D1", "CP_MEUR"), ("P1", "CP_MEUR")]:
        for nace in ["M71", "F", "M"]:
            js = eurostat_json(
                "nama_10_a64",
                {"na_item": item, "nace_r2": nace, "unit": unit},
            )
            recs = parse_eurostat(js)
            n = 0
            for r in recs:
                if r.get("geo") not in GEOS and r.get("geo") != "UK":
                    continue
                try:
                    y = int(str(r.get("time"))[:4])
                except (TypeError, ValueError):
                    continue
                if y < 2015:
                    continue
                rows.append(
                    {
                        "dataset": "nama_10_a64",
                        "na_item": item,
                        "nace": nace,
                        "geo": r["geo"],
                        "year": y,
                        "unit": unit,
                        "value": r["value"],
                    }
                )
                n += 1
            print("nama", item, nace, "kept", n, "raw", len(recs))
    df = pd.DataFrame(rows)
    if not df.empty:
        df.to_csv(DATA / "eurostat_nama_D1_P1_M71_F_M.csv", index=False)
    print("nama income", df.shape)
    return df


def fetch_ilo_m71():
    """ILO employment ISIC M71 if the code exists; empty is informative."""
    url = (
        "https://www.ilo.org/sdmx-service/rest/data/ILO,DF_EMP_TEMP_SEX_ECO_NB/"
        "A.GBR+IND+CHN+USA+PHL+VNM+DEU+FRA+NLD+AUS.SEX_T.ECO_ISIC4_M71.NB"
        "?format=csv"
    )
    raw = get(url, timeout=60)
    log = []
    if not raw or raw.lstrip().startswith(b"<"):
        log.append({"url": url, "status": "fail_or_xml"})
        pd.DataFrame(log).to_csv(DATA / "ilo_m71_fetch_log.csv", index=False)
        print("ILO M71 fail")
        return
    text = raw.decode("utf-8", errors="replace")
    if "ObsValue" not in text and "OBS_VALUE" not in text and len(text) < 80:
        log.append({"url": url, "status": "short", "head": text[:200]})
        pd.DataFrame(log).to_csv(DATA / "ilo_m71_fetch_log.csv", index=False)
        print("ILO M71 short", text[:120])
        return
    path = DATA / "ilo_emp_M71.csv"
    path.write_text(text)
    log.append({"url": url, "status": "ok", "bytes": len(raw)})
    pd.DataFrame(log).to_csv(DATA / "ilo_m71_fetch_log.csv", index=False)
    print("ILO M71 saved", len(raw))


def fetch_bls_54133():
    """US engineering services (NAICS 54133) employment from BLS QCEW if public."""
    # ENUUS0002054133 is not guaranteed; try CES professional/technical as fallback later.
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    payload = json.dumps({
        "seriesid": ["CEU6054133301", "CEU6054000001"],
        "startyear": "2018",
        "endyear": "2025",
    }).encode()
    req = Request(
        url,
        data=payload,
        headers={"User-Agent": UA, "Content-Type": "application/json"},
        method="POST",
    )
    log = []
    try:
        with urlopen(req, timeout=60) as r:
            raw = r.read()
    except Exception as e:
        pd.DataFrame([{"status": "fail", "err": str(e)[:200]}]).to_csv(
            DATA / "bls_54133_fetch_log.csv", index=False
        )
        print("BLS fail", e)
        return
    text = raw.decode("utf-8", errors="replace")
    (DATA / "bls_54133_raw.json").write_text(text)
    try:
        js = json.loads(text)
    except json.JSONDecodeError:
        print("BLS not json")
        return
    status = js.get("status")
    rows = []
    for ser in (js.get("Results") or {}).get("series") or []:
        sid = ser.get("seriesID")
        for d in ser.get("data") or []:
            if d.get("period") != "M13" and not str(d.get("period", "")).startswith("M"):
                continue
            # keep annual if present, else March
            rows.append(
                {
                    "series": sid,
                    "year": int(d["year"]),
                    "period": d.get("period"),
                    "periodName": d.get("periodName"),
                    "value": d.get("value"),
                }
            )
    if rows:
        pd.DataFrame(rows).to_csv(DATA / "bls_engineering_ces.csv", index=False)
    pd.DataFrame([{"status": status, "n": len(rows), "message": str(js.get("message"))[:300]}]).to_csv(
        DATA / "bls_54133_fetch_log.csv", index=False
    )
    print("BLS", status, "rows", len(rows))


def main():
    fetch_sbs()
    fetch_nama_income()
    fetch_ilo_m71()
    fetch_bls_54133()
    print("done")


if __name__ == "__main__":
    main()
