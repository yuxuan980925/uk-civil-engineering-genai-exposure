#!/usr/bin/env python3
"""Corroboration tests for the association conclusion.

Conclusion being tested (not a causal relocation claim)
-------------------------------------------------------
Among EU importers, a larger 2023–24 NACE M NLG jump is associated with
higher Indian engineering-service imports, not with Chinese engineering or
construction services, and with slower nominal engineering-industry turnover
but not falling employment.

Additional official objects in this script
------------------------------------------
- NACE M7112 (engineering consultancy) vs M7111 (architecture)
- ITS SJ312 from US/UK/CH/JP and extra-EU (placebos)
- Independent re-fetch of IN/CN SJ312 vs the previous extract
- FATS M71 by controlling country (coverage only; series ends 2020)
- Leave-one-out of Finland (ITS SJ312 2022–24 outlier)
- Indian SJ312 share of extra-EU SJ312
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
AI = ROOT / "01_ai_shock"
PROBE = ROOT / "09_relocation_probe"
TAB = PROBE / "tables"
TAB.mkdir(parents=True, exist_ok=True)

GEO2ISO = {
    "DE": "DEU", "FR": "FRA", "NL": "NLD", "PL": "POL", "RO": "ROU",
    "IT": "ITA", "ES": "ESP", "IE": "IRL", "BE": "BEL", "AT": "AUT",
    "SE": "SWE", "DK": "DNK", "PT": "PRT", "CZ": "CZE", "HU": "HUN",
    "FI": "FIN", "EL": "GRC", "UK": "GBR",
}
EU17 = list(GEO2ISO.values())
EU17.remove("GBR")


def star(p):
    if pd.isna(p):
        return ""
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def fmt(b, se, p):
    if pd.isna(b):
        return "—"
    return f"{b:.3f}{star(p)} ({se:.3f})"


def fit_fe(df, y, x, fe, cluster=None, min_n=16):
    df = df.loc[:, ~df.columns.duplicated()].copy()
    use = list(dict.fromkeys([y] + x + fe + ([cluster] if cluster else [])))
    d = df[use].dropna().copy().reset_index(drop=True)
    if len(d) < min_n:
        return None
    work = d[[y] + x].astype(float)
    for _ in range(8):
        for g in fe:
            gv = d[g]
            if isinstance(gv, pd.DataFrame):
                gv = gv.iloc[:, 0]
            work = work - work.groupby(gv.to_numpy()).transform("mean")
    yv, X = work[y], work[x]
    if cluster and d[cluster].nunique() >= 4:
        res = sm.OLS(yv, X).fit(
            cov_type="cluster",
            cov_kwds={"groups": d[cluster], "use_correction": True},
        )
    else:
        res = sm.OLS(yv, X).fit(cov_type="HC1")
    sst = float(np.sum((d[y] - d[y].mean()) ** 2))
    res.rsquared = 1 - float(np.sum(res.resid**2) / sst) if sst else np.nan
    return res, d


def row(name, res, key, n, note, rq):
    if res is None or key not in getattr(res, "params", {}):
        return {
            "rq": rq, "spec": name, "coef": np.nan, "se": np.nan, "p": np.nan,
            "n": n, "r2": np.nan, "note": note, "display": "—",
        }
    return {
        "rq": rq, "spec": name,
        "coef": float(res.params[key]), "se": float(res.bse[key]),
        "p": float(res.pvalues[key]), "n": n, "r2": float(res.rsquared),
        "note": note,
        "display": fmt(res.params[key], res.bse[key], res.pvalues[key]),
    }


def load_intensity():
    g = pd.read_csv(AI / "eurostat_ai_genai_types.csv")
    g["value"] = pd.to_numeric(g.value, errors="coerce")
    g["year"] = g.time.astype(int)
    recs = []
    for geo, iso in GEO2ISO.items():
        if iso not in EU17:
            continue
        s = g[(g.geo == geo) & (g.indic == "E_AI_TNLG") & (g.nace == "M")]
        r = {"geo": geo, "iso3": iso}
        for y in (2023, 2024):
            hit = s[s.year == y]
            r[f"tnlg_M_{y}"] = float(hit.value.iloc[0]) if len(hit) else np.nan
        recs.append(r)
    inten = pd.DataFrame(recs)
    inten["d_tnlg_M_2324"] = inten.tnlg_M_2024 - inten.tnlg_M_2023
    return inten


def build_panel(trade, inten, year0=2018, year1=2024):
    importers = sorted(set(inten.iso3) & set(trade.importer.unique()))
    p = trade[trade.importer.isin(importers) & trade.year.between(year0, year1)].copy()
    p = p.merge(inten, left_on="importer", right_on="iso3", how="left")
    p["logv"] = np.log(p.value.clip(lower=0.01))
    p["post"] = (p.year >= 2023).astype(float)
    p["post24"] = (p.year >= 2024).astype(float)
    p["post_x_d_tnlg_M_2324"] = p.post * p.d_tnlg_M_2324
    p["p24_x_d_tnlg_M_2324"] = p.post24 * p.d_tnlg_M_2324
    return p


def run_spec(results, name, dat, key, extra, note, rq):
    if dat is None or dat.empty or "logv" not in dat.columns:
        results.append(row(name, None, key, 0, note + " [empty]", rq))
        return
    fe = ["importer", "year"]
    if "partner" in dat.columns and dat.partner.nunique() > 1:
        fe.append("partner")
    out = fit_fe(dat, "logv", extra, fe, "importer")
    if out is None:
        results.append(row(name, None, key, len(dat), note + " [N too small]", rq))
        return
    res, used = out
    results.append(row(name, res, key, len(used), note, rq))


def its_to_trade(its, partner_code, flow="DEB"):
    if its is None or its.empty:
        return pd.DataFrame(columns=["importer", "partner", "year", "value"])
    iso_partner = {
        "IN": "IND", "CN_X_HK": "CHN", "US": "USA", "UK": "GBR",
        "CH": "CHE", "JP": "JPN", "EXT_EU27_2020": "XE27",
    }.get(partner_code, partner_code)
    m = its[
        (its.stk_flow == flow)
        & (its.partner == partner_code)
        & its.geo.map(GEO2ISO).isin(EU17)
    ].copy()
    m["importer"] = m.geo.map(GEO2ISO)
    m["partner"] = iso_partner
    m["value"] = pd.to_numeric(m.value, errors="coerce")
    return m.dropna(subset=["value"])[["importer", "partner", "year", "value"]]


def sbs_series(sbs, nace, indic):
    d = sbs[(sbs.nace == nace) & (sbs.indic == indic) & (sbs.dataset == "sbs_ovw_act")].copy()
    d["importer"] = d.geo.map(GEO2ISO)
    d = d[d.importer.isin(EU17)]
    d["value"] = pd.to_numeric(d.value, errors="coerce")
    return d.dropna(subset=["value"])[["importer", "year", "value"]]


def main():
    results = []
    notes = []
    inten = load_intensity()

    # ----- Independent re-fetch vs prior ITS -----
    prior = pd.read_csv(PROBE / "eurostat_its_engineering.csv")
    prior = prior[(prior.bop_item == "SJ312")]
    refetch_path = PROBE / "eurostat_its_sj312_refetch.csv"
    audit = {"refetch_file": refetch_path.exists()}
    if refetch_path.exists():
        ref = pd.read_csv(refetch_path)
        keys = ["geo", "year", "partner", "stk_flow"]
        a = prior[prior.partner.isin(["IN", "CN_X_HK"])][keys + ["value"]].copy()
        a["value"] = pd.to_numeric(a.value, errors="coerce")
        b = ref[keys + ["value"]].copy()
        b["value"] = pd.to_numeric(b.value, errors="coerce")
        m = a.merge(b, on=keys, suffixes=("_prior", "_refetch"))
        m["diff"] = (m.value_prior - m.value_refetch).abs()
        audit.update({
            "n_matched": int(len(m)),
            "n_differ": int((m["diff"] > 1e-6).sum()),
            "max_abs_diff": float(m["diff"].max()) if len(m) else None,
            "de_in_2024_prior": float(
                a[(a.geo == "DE") & (a.year == 2024) & (a.partner == "IN") & (a.stk_flow == "DEB")].value.iloc[0]
            ) if len(a[(a.geo == "DE") & (a.year == 2024) & (a.partner == "IN") & (a.stk_flow == "DEB")]) else None,
            "de_in_2024_refetch": float(
                b[(b.geo == "DE") & (b.year == 2024) & (b.partner == "IN") & (b.stk_flow == "DEB")].value.iloc[0]
            ) if len(b[(b.geo == "DE") & (b.year == 2024) & (b.partner == "IN") & (b.stk_flow == "DEB")]) else None,
        })
    (TAB / "its_refetch_audit.json").write_text(json.dumps(audit, indent=2))
    notes.append(f"ITS re-fetch audit: {audit}")

    # ----- Placebo partners -----
    plc_path = PROBE / "eurostat_its_sj312_placebos.csv"
    plc = pd.read_csv(plc_path) if plc_path.exists() else pd.DataFrame()
    # Combine refetch India/China with prior if refetch exists
    its_ind = pd.read_csv(refetch_path) if refetch_path.exists() else prior
    for code, lab in [
        ("IN", "Indian SJ312 (re-fetch)"),
        ("CN_X_HK", "Chinese SJ312 (re-fetch)"),
    ]:
        src = its_ind if refetch_path.exists() else prior
        tr = its_to_trade(src, code)
        run_spec(
            results, f"C2 {lab} Post×ΔM TNLG",
            build_panel(tr, inten), "post_x_d_tnlg_M_2324",
            ["post_x_d_tnlg_M_2324"], "Independent Eurostat pull", "C2",
        )
    if not plc.empty:
        for code, lab in [
            ("US", "US SJ312 placebo"),
            ("UK", "UK SJ312 placebo"),
            ("CH", "Swiss SJ312 placebo"),
            ("JP", "Japan SJ312 placebo"),
            ("EXT_EU27_2020", "Extra-EU SJ312 total"),
        ]:
            tr = its_to_trade(plc, code)
            n_imp = int(tr.importer.nunique()) if not tr.empty else 0
            run_spec(
                results, f"C3 {lab} Post×ΔM TNLG",
                build_panel(tr, inten), "post_x_d_tnlg_M_2324",
                ["post_x_d_tnlg_M_2324"],
                f"Same heading, different partner; importers={n_imp}",
                "C3",
            )

    # Indian share of extra-EU engineering imports
    if not plc.empty and refetch_path.exists():
        inn = its_to_trade(pd.read_csv(refetch_path), "IN").rename(columns={"value": "in_sj312"})
        ext = its_to_trade(plc, "EXT_EU27_2020").rename(columns={"value": "ext_sj312"})
        sh = inn.merge(ext[["importer", "year", "ext_sj312"]], on=["importer", "year"], how="inner")
        sh = sh[sh.ext_sj312 > 0]
        sh["value"] = 100 * sh.in_sj312 / sh.ext_sj312
        sh["partner"] = "SHARE"
        sh.to_csv(TAB / "india_share_of_extra_eu_sj312.csv", index=False)
        p = build_panel(sh[["importer", "partner", "year", "value"]], inten)
        # share is already a percentage; still log would distort. Use level.
        p["logv"] = p.value  # reuse field as the outcome (percentage points)
        run_spec(
            results, "C4 Indian share of extra-EU SJ312 Post×ΔM TNLG",
            p, "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
            "Outcome is percentage points, not log; missing years dropped",
            "C4",
        )

    # Leave-one-out Finland on Indian SJ312
    src = pd.read_csv(refetch_path) if refetch_path.exists() else prior
    tr = its_to_trade(src, "IN")
    run_spec(
        results, "C5 Indian SJ312 drop Finland Post×ΔM TNLG",
        build_panel(tr[tr.importer != "FIN"], inten),
        "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
        "Finland 2022–24 SJ312 21→145 EUR m is an outlier",
        "C5",
    )

    # ----- M7112 engineering consultancy vs architecture -----
    sbs_path = PROBE / "eurostat_sbs_M7112_engineering.csv"
    if sbs_path.exists():
        sbs = pd.read_csv(sbs_path)
        for nace, lab in [
            ("M7112", "M7112 engineering consultancy"),
            ("M7111", "M7111 architectural activities"),
            ("M712", "M712 technical testing"),
            ("M71", "M71 (repeat)"),
        ]:
            for indic, ilab in [("EMP_NR", "employment"), ("VAL_OUT_MEUR", "output"),
                                ("WAGE_MEUR", "wages"), ("AV_MEUR", "value added")]:
                d = sbs_series(sbs, nace, indic)
                if d.empty:
                    results.append(row(
                        f"C6 {lab} {ilab} Post2024×ΔTNLG", None, "p24_x_d_tnlg_M_2324",
                        0, "Unpublished in this pull", "C6",
                    ))
                    continue
                d = d.merge(inten, left_on="importer", right_on="iso3", how="left")
                d["logv"] = np.log(d.value.clip(lower=0.01))
                d["post24"] = (d.year >= 2024).astype(float)
                d["p24_x_d_tnlg_M_2324"] = d.post24 * d.d_tnlg_M_2324
                d["partner"] = "DOM"
                run_spec(
                    results, f"C6 {lab} {ilab} Post2024×ΔTNLG",
                    d, "p24_x_d_tnlg_M_2324", ["p24_x_d_tnlg_M_2324"],
                    "SBS current prices 2021–24; tighter industry than all M71",
                    "C6",
                )

    # ----- FATS coverage -----
    fats_path = PROBE / "eurostat_fats_M71.csv"
    fats_cov = {"exists": fats_path.exists()}
    if fats_path.exists():
        fats = pd.read_csv(fats_path)
        fats["value"] = pd.to_numeric(fats.value, errors="coerce")
        fats_cov.update({
            "n_cells": int(len(fats)),
            "max_year": int(fats.year.max()) if len(fats) else None,
            "min_year": int(fats.year.min()) if len(fats) else None,
            "controls": sorted(fats.c_ctrl.dropna().unique().tolist()),
            "india_cells": int(len(fats[fats.c_ctrl == "IN"])),
            "china_cells": int(len(fats[fats.c_ctrl == "CN_X_HK"])),
            "us_cells": int(len(fats[fats.c_ctrl == "US"])),
        })
        notes.append(
            "FATS inward M71 by controlling country ends in 2020, before the NLG "
            "window. India-controlled M71 affiliates are unpublished. Mode 3 "
            "cannot be tested against the 2023–24 shock."
        )
    (TAB / "fats_coverage.json").write_text(json.dumps(fats_cov, indent=2))

    t = pd.DataFrame(results)
    t.to_csv(TAB / "table_corroboration.csv", index=False)
    pretty = t[["rq", "spec", "display", "n", "note"]].copy()
    pretty.columns = ["RQ", "Specification", "Coefficient (s.e.)", "N", "Note"]
    pretty.to_csv(TAB / "article_corroboration_results.csv", index=False)
    payload = {
        "conclusion_tested": (
            "Importer NLG jump is associated with Indian engineering-service "
            "imports and not with Chinese engineering/construction services, "
            "while engineering-industry employment does not fall."
        ),
        "its_refetch_audit": audit,
        "fats_coverage": fats_cov,
        "results": results,
        "notes": notes,
    }
    (PROBE / "results_corroboration.json").write_text(json.dumps(payload, indent=2, default=str))
    print(t[["rq", "spec", "display", "n"]].to_string(index=False))
    print("AUDIT", json.dumps(audit, indent=2))
    print("FATS", json.dumps(fats_cov, indent=2))


if __name__ == "__main__":
    main()
