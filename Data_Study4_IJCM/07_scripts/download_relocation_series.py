#!/usr/bin/env python3
"""Retrieve official series that could identify *transnational relocation*
of civil-engineering activity under generative AI.

Never interpolate missing cells. Empty API responses are written to the
fetch log as unpublished, not filled.

New objects
-----------
1. Eurostat BPM6 ITS (`bop_its6_det`): EBOPS SJ31 / SJ311 / SJ312
   (architectural and engineering services) by EU reporter × partner.
   BaTIS does not publish these headings.
2. Eurostat LFS (`lfsa_egai2d`): ISCO-08 two-digit employment. Closest
   published occupation group is OC21 (science and engineering
   professionals). ISCO 2142 is not in this dataset.
3. ILOSTAT occupation employment: attempted at 4-digit 2142 and coarser
   codes; absence is informative.
4. BaTIS reported (N) vs balanced (B) is already in
   `03_trade/batis_civil_related.csv`; this script does not re-download it.

UK Pink Book bilateral engineering cells and GATS modes are not requested
here because prior ONS file URLs 404'd in this environment and BaTIS does
not identify mode of supply.
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

UA = "Study4-relocation-probe/1.0 (academic; eurostat/ilo retrieval)"
GEOS = [
    "EU27_2020",
    "DE", "FR", "NL", "PL", "RO", "IT", "ES", "IE", "BE", "AT",
    "SE", "DK", "PT", "CZ", "HU", "FI", "EL", "UK",
]
PARTNERS = ["IN", "CN", "PH", "VN", "US", "UK", "EXT_EU27_2020", "WORLD"]
ITEMS = [
    "SJ3", "SJ31", "SJ311", "SJ312", "SJ313",
    "SE", "SE1", "SE2",
    "SI", "SI2",
]
FLOWS = ["DEB", "CRE"]
YEARS = list(range(2015, 2025))


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


def fetch_its():
    """One item × partner × flow per call. Combined filters return 413 or empty."""
    log = []
    rows = []
    # India/China are the relocation contrast; PH matches the BaTIS Mode-1 pool.
    # China is CN_X_HK (China except Hong Kong). CN and VN return empty cubes.
    partners = ["IN", "CN_X_HK", "PH", "VN"]
    items = ["SJ312", "SJ31", "SJ311", "SJ313", "SJ3", "SE", "SI"]
    for partner in partners:
        for item in items:
            for flow in FLOWS:
                js = eurostat_json(
                    "bop_its6_det",
                    {
                        "bop_item": item,
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
                    if y not in YEARS:
                        continue
                    if r.get("geo") not in GEOS:
                        continue
                    rows.append(
                        {
                            "dataset": "bop_its6_det",
                            "bop_item": r.get("bop_item", item),
                            "bop_item_label": r.get("bop_item_label"),
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
                log.append(
                    {
                        "partner": partner,
                        "bop_item": item,
                        "stk_flow": flow,
                        "status": status,
                        "raw": len(recs),
                        "kept": keep,
                    }
                )
                print("ITS", partner, item, flow, status, "kept", keep, "raw", len(recs))
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.drop_duplicates(
            ["bop_item", "stk_flow", "partner", "geo", "year"]
        )
        df.to_csv(OUT / "eurostat_its_engineering.csv", index=False)
    pd.DataFrame(log).to_csv(OUT / "eurostat_its_fetch_log.csv", index=False)
    print("ITS saved", df.shape)
    return df


def coverage_table(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    recs = []
    for item in ITEMS:
        for partner in ["IN", "CN_X_HK", "PH", "VN"]:
            sub = df[
                (df.bop_item == item)
                & (df.stk_flow == "DEB")
                & (df.partner == partner)
                & (df.geo != "EU27_2020")
            ]
            years = sorted(sub.year.unique().tolist()) if not sub.empty else []
            recs.append(
                {
                    "bop_item": item,
                    "partner": partner,
                    "n_cells": int(len(sub)),
                    "n_geos": int(sub.geo.nunique()) if not sub.empty else 0,
                    "n_years": int(sub.year.nunique()) if not sub.empty else 0,
                    "min_year": int(min(years)) if years else None,
                    "max_year": int(max(years)) if years else None,
                    "geos_with_2023": int(sub[sub.year == 2023].geo.nunique())
                    if not sub.empty
                    else 0,
                    "geos_with_2024": int(sub[sub.year == 2024].geo.nunique())
                    if not sub.empty
                    else 0,
                    "complete_2022_and_2024": int(
                        len(
                            set(sub[sub.year == 2022].geo)
                            & set(sub[sub.year == 2024].geo)
                        )
                    )
                    if not sub.empty
                    else 0,
                }
            )
    cov = pd.DataFrame(recs)
    cov.to_csv(OUT / "coverage_eurostat_its.csv", index=False)
    return cov


def fetch_lfs_occupation():
    """ISCO-08 two-digit employment. Civil engineers (2142) are not published."""
    log = []
    rows = []
    iscos = ["OC21", "OC31", "OC25", "OC71", "OC93", "OC2", "OC3"]
    geos = [g for g in GEOS if g != "EU27_2020"] + ["EU27_2020"]
    for isco in iscos:
        js = eurostat_json(
            "lfsa_egai2d",
            {
                "isco08": isco,
                "sex": "T",
                "age": "Y15-64",
                "unit": "THS_PER",
            },
        )
        recs = parse_eurostat(js) if js else []
        keep = 0
        for r in recs:
            try:
                y = int(str(r.get("time"))[:4])
            except (TypeError, ValueError):
                continue
            if y < 2015 or y > 2025:
                continue
            if r.get("geo") not in geos:
                continue
            rows.append(
                {
                    "dataset": "lfsa_egai2d",
                    "isco08": r.get("isco08"),
                    "isco08_label": r.get("isco08_label"),
                    "geo": r.get("geo"),
                    "year": y,
                    "unit": r.get("unit", "THS"),
                    "age": r.get("age"),
                    "sex": r.get("sex"),
                    "value": r["value"],
                }
            )
            keep += 1
        log.append(
            {
                "dataset": "lfsa_egai2d",
                "isco08": isco,
                "status": "ok" if recs else ("empty" if js else "fail"),
                "raw": len(recs),
                "kept": keep,
            }
        )
        print("LFS", isco, "kept", keep, "raw", len(recs))
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.drop_duplicates(["isco08", "geo", "year", "age", "sex"])
        df.to_csv(OUT / "eurostat_lfsa_occ2d.csv", index=False)
    pd.DataFrame(log).to_csv(OUT / "eurostat_lfs_fetch_log.csv", index=False)
    print("LFS saved", df.shape)
    return df


def fetch_ilo_occupation():
    """Attempt ILO occupation employment. 2142 is the civil-engineer code."""
    keys = [
        "OCU_ISCO08_2142",
        "OCU_ISCO08_214",
        "OCU_ISCO08_21",
        "OCU_ISCO08_2",
        "OCU_ISCO08_OC2",
        "OCU_ISCO08_TOTAL",
    ]
    areas = "GBR+IND+CHN+PHL+VNM+DEU+FRA+NLD"
    log = []
    for key in keys:
        url = (
            "https://www.ilo.org/sdmx-service/rest/data/ILO,DF_EMP_TEMP_SEX_OCU_NB/"
            f"A.{areas}.SEX_T.{key}.NB?format=csv"
        )
        raw = get(url, timeout=45)
        if not raw:
            log.append({"key": key, "status": "fail", "url": url})
            print("ILO", key, "fail")
            continue
        if raw.lstrip().startswith(b"<") or raw.lstrip().startswith(b"["):
            log.append(
                {
                    "key": key,
                    "status": "xml_or_error",
                    "bytes": len(raw),
                    "head": raw[:160].decode("utf-8", errors="replace"),
                    "url": url,
                }
            )
            print("ILO", key, "xml_or_error")
            continue
        text = raw.decode("utf-8", errors="replace")
        if "OBS_VALUE" not in text and "ObsValue" not in text:
            log.append(
                {
                    "key": key,
                    "status": "no_obs",
                    "bytes": len(raw),
                    "head": text[:160],
                    "url": url,
                }
            )
            print("ILO", key, "no_obs")
            continue
        path = OUT / f"ilo_emp_{key}.csv"
        path.write_text(text)
        log.append(
            {
                "key": key,
                "status": "ok",
                "bytes": len(raw),
                "file": path.name,
                "url": url,
            }
        )
        print("ILO saved", key, len(raw))
        break
    pd.DataFrame(log).to_csv(OUT / "ilo_occupation_fetch_log.csv", index=False)


def main():
    print("=== Eurostat ITS architectural/engineering ===")
    its = fetch_its()
    coverage_table(its if its is not None else pd.DataFrame())
    print("=== Eurostat LFS ISCO 2-digit ===")
    fetch_lfs_occupation()
    print("=== ILO occupation ===")
    fetch_ilo_occupation()
    print("done")


if __name__ == "__main__":
    main()
