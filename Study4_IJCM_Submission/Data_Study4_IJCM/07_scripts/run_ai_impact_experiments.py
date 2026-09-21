#!/usr/bin/env python3
"""AI-shock impact experiments. Official cells only. No interpolation.

Identification: 2023–24 change in Eurostat E_AI_TNLG among NACE M enterprises.
UK, India and China are not in that panel and are not given this treatment.

Formulas: Data_Study4_IJCM/AI_SHOCK_IMPACT.md
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
AI = ROOT / "01_ai_shock"
IND = ROOT / "02_industry_accounts"
TRADE = ROOT / "03_trade"
PROBE = ROOT / "09_relocation_probe"
NEW = ROOT / "11_ai_shock_impact"
TAB = NEW / "tables"
FIG = NEW / "figures"
for p in (NEW, TAB, FIG):
    p.mkdir(parents=True, exist_ok=True)

GEO2ISO = {
    "DE": "DEU", "FR": "FRA", "NL": "NLD", "PL": "POL", "RO": "ROU",
    "IT": "ITA", "ES": "ESP", "IE": "IRL", "BE": "BEL", "AT": "AUT",
    "SE": "SWE", "DK": "DNK", "PT": "PRT", "CZ": "CZE", "HU": "HUN",
    "FI": "FIN", "EL": "GRC",
}
ISO2NAME = {
    "DEU": "Germany", "FRA": "France", "NLD": "Netherlands", "POL": "Poland",
    "ROU": "Romania", "ITA": "Italy", "ESP": "Spain", "IRL": "Ireland",
    "BEL": "Belgium", "AUT": "Austria", "SWE": "Sweden", "DNK": "Denmark",
    "PRT": "Portugal", "CZE": "Czechia", "HUN": "Hungary", "FIN": "Finland",
    "GRC": "Greece",
}
EU17 = list(GEO2ISO.values())


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


def row(name, res, key, n, note, layer):
    if res is None or key not in getattr(res, "params", {}):
        return {
            "layer": layer, "spec": name, "coef": np.nan, "se": np.nan, "p": np.nan,
            "n": n, "r2": np.nan, "note": note, "display": "—",
        }
    return {
        "layer": layer, "spec": name,
        "coef": float(res.params[key]), "se": float(res.bse[key]),
        "p": float(res.pvalues[key]), "n": n, "r2": float(res.rsquared),
        "note": note,
        "display": fmt(res.params[key], res.bse[key], res.pvalues[key]),
    }


def load_intensity():
    g = pd.read_csv(AI / "eurostat_ai_genai_types.csv")
    g["value"] = pd.to_numeric(g.value, errors="coerce")
    g["year"] = g.time.astype(int) if "time" in g.columns else g.year.astype(int)
    indic_col = "indic" if "indic" in g.columns else "indic_is"
    recs = []
    for geo, iso in GEO2ISO.items():
        r = {"geo": geo, "iso3": iso, "country": ISO2NAME[iso]}
        for y in (2021, 2023, 2024, 2025):
            hit = g[(g.geo == geo) & (g[indic_col] == "E_AI_TNLG") & (g.nace == "M") & (g.year == y)]
            r[f"tnlg_M_{y}"] = float(hit.value.iloc[0]) if len(hit) else np.nan
            hitf = g[(g.geo == geo) & (g[indic_col] == "E_AI_TNLG") & (g.nace == "F") & (g.year == y)]
            r[f"tnlg_F_{y}"] = float(hitf.value.iloc[0]) if len(hitf) else np.nan
        recs.append(r)
    inten = pd.DataFrame(recs)
    inten["d_tnlg_M_2324"] = inten.tnlg_M_2024 - inten.tnlg_M_2023
    inten["d_tnlg_F_2324"] = inten.tnlg_F_2024 - inten.tnlg_F_2023
    inten["d_tnlg_M_2425"] = inten.tnlg_M_2025 - inten.tnlg_M_2024
    return inten


def attach_shock(d, inten, geo_col="geo"):
    if "iso3" not in d.columns:
        d = d.copy()
        d["iso3"] = d[geo_col].map(GEO2ISO)
    d = d.merge(
        inten[["iso3", "d_tnlg_M_2324", "d_tnlg_F_2324", "tnlg_M_2024", "country"]],
        on="iso3", how="left",
    )
    d["importer"] = d["iso3"]
    return d


def estimate_sbs(sbs, inten, nace, indic, dataset, yname, layer, results):
    d = sbs[(sbs.nace == nace) & (sbs.indic == indic)].copy()
    if dataset and "dataset" in d.columns:
        d = d[d.dataset == dataset]
    d["value"] = pd.to_numeric(d.value, errors="coerce")
    d = d.dropna(subset=["value"])
    d = d[d.value > 0]
    d = attach_shock(d, inten)
    d = d[d.iso3.isin(EU17) & d.year.between(2021, 2024)]
    d["logv"] = np.log(d.value)
    d["post24"] = (d.year >= 2024).astype(float)
    d["p24_tnlg"] = d.post24 * d.d_tnlg_M_2324
    out = fit_fe(d, "logv", ["p24_tnlg"], ["importer", "year"], "importer")
    n = len(out[1]) if out else len(d.dropna(subset=["logv", "p24_tnlg"]))
    results.append(row(
        yname, out[0] if out else None, "p24_tnlg", n,
        f"SBS {nace} {indic} {dataset or ''}; country+year FE; Post-2024 × ΔTNLG-M",
        layer,
    ))
    return out


def main():
    plt.rcParams.update({
        "figure.dpi": 140, "savefig.dpi": 200, "font.size": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.25,
    })
    inten = load_intensity()
    inten.to_csv(TAB / "tnlg_intensity.csv", index=False)
    iqr = float(inten.d_tnlg_M_2324.quantile(0.75) - inten.d_tnlg_M_2324.quantile(0.25))
    med = float(inten.d_tnlg_M_2324.median())
    shock_desc = {
        "n": int(inten.d_tnlg_M_2324.notna().sum()),
        "mean": float(inten.d_tnlg_M_2324.mean()),
        "median": med,
        "p25": float(inten.d_tnlg_M_2324.quantile(0.25)),
        "p75": float(inten.d_tnlg_M_2324.quantile(0.75)),
        "iqr": iqr,
        "min": float(inten.d_tnlg_M_2324.min()),
        "max": float(inten.d_tnlg_M_2324.max()),
        "mean_2025_minus_2024": float(inten.d_tnlg_M_2425.mean()),
    }
    print("SHOCK", shock_desc)

    results = []

    # A1–A2: SBS M71 including official labour productivity
    sbs = pd.read_csv(IND / "eurostat_sbs_M71_F_M.csv")
    sbs["year"] = sbs.year.astype(int)
    specs = [
        ("A1 log M71 turnover", "M71", "NETTUR_MEUR", "sbs_sc_ovw", "A1"),
        ("A1 log M71 employment", "M71", "EMP_NR", "sbs_ovw_act", "A1"),
        ("A1 log M71 wages", "M71", "WAGE_MEUR", "sbs_ovw_act", "A1"),
        ("A1 log M71 value added", "M71", "AV_MEUR", "sbs_ovw_act", "A1"),
        ("A1 log M71 GOS", "M71", "GOS_MEUR", "sbs_ovw_act", "A1"),
        ("A2 log M71 labour productivity (LABPRY)", "M71", "LABPRY_TEUR", "sbs_ovw_act", "A2"),
        ("A2 log M71 labour cost per employed (LC_EMP)", "M71", "LC_EMP_TEUR", "sbs_ovw_act", "A2"),
        ("A3 log F turnover (placebo)", "F", "NETTUR_MEUR", "sbs_sc_ovw", "A3"),
        ("A3 log F employment (placebo)", "F", "EMP_NR", "sbs_ovw_act", "A3"),
        ("A3 log F labour productivity", "F", "LABPRY_TEUR", "sbs_ovw_act", "A3"),
        ("A3 log M turnover (placebo)", "M", "NETTUR_MEUR", "sbs_sc_ovw", "A3"),
        ("A3 log M labour productivity", "M", "LABPRY_TEUR", "sbs_ovw_act", "A3"),
    ]
    for name, nace, indic, ds, layer in specs:
        estimate_sbs(sbs, inten, nace, indic, ds, name, layer, results)

    # Author-constructed VA/E only from co-published cells (check, not a fill)
    va = sbs[(sbs.nace == "M71") & (sbs.indic == "AV_MEUR") & (sbs.dataset == "sbs_ovw_act")][
        ["geo", "year", "value"]
    ].rename(columns={"value": "va"})
    emp = sbs[(sbs.nace == "M71") & (sbs.indic == "EMP_NR") & (sbs.dataset == "sbs_ovw_act")][
        ["geo", "year", "value"]
    ].rename(columns={"value": "emp"})
    ratio = va.merge(emp, on=["geo", "year"])
    ratio["value"] = pd.to_numeric(ratio.va, errors="coerce") / pd.to_numeric(ratio.emp, errors="coerce")
    ratio = ratio[(ratio.value > 0) & ratio.value.notna()].copy()
    ratio["nace"] = "M71"
    ratio["indic"] = "VA_PER_EMP"
    ratio["dataset"] = "derived_from_published_cells"
    estimate_sbs(ratio, inten, "M71", "VA_PER_EMP", "derived_from_published_cells",
                 "A2 log M71 VA per employed (co-published cells)", "A2", results)

    # A3 M7112 / M7111
    m71x = PROBE / "eurostat_sbs_M7112_engineering.csv"
    if m71x.exists():
        fine = pd.read_csv(m71x)
        fine["year"] = fine.year.astype(int)
        for nace, lab in [("M7112", "engineering consultancy"), ("M7111", "architecture")]:
            for indic, iname, ds in [
                ("EMP_NR", "employment", None),
                ("VAL_OUT_MEUR", "output", None),
                ("WAGE_MEUR", "wages", None),
                ("AV_MEUR", "value added", None),
                ("NETTUR_MEUR", "turnover", None),
            ]:
                if indic not in set(fine.indic):
                    continue
                estimate_sbs(
                    fine, inten, nace, indic, ds,
                    f"A3 log {nace} {lab} {iname}", "A3", results,
                )

    # A4–A5 trade
    its_path = PROBE / "eurostat_its_engineering.csv"
    if its_path.exists():
        its = pd.read_csv(its_path)
        its["year"] = pd.to_numeric(its.get("time", its.get("year")), errors="coerce")
        valcol = "value" if "value" in its.columns else "OBS_VALUE"
        its["value"] = pd.to_numeric(its[valcol], errors="coerce")
        geo_col = "geo" if "geo" in its.columns else "reporter"
        partner_col = "partner" if "partner" in its.columns else "partner"
        item_col = "stk_flow" if "bop_item" not in its.columns else "bop_item"
        # Flexible column names from Eurostat parse
        for c in its.columns:
            if c.lower() in ("bop_item", "item", "indic_bop"):
                item_col = c
            if c.lower() in ("partner", "partner_label") and c == "partner":
                partner_col = c
            if c.lower() in ("stk_flow", "flow"):
                flow_col = c
        flow_col = "stk_flow" if "stk_flow" in its.columns else ("flow" if "flow" in its.columns else None)

        def its_panel(item, partner, flow="DEB"):
            d = its.copy()
            if item_col in d.columns:
                d = d[d[item_col] == item]
            if partner_col in d.columns:
                d = d[d[partner_col] == partner]
            if flow_col:
                d = d[d[flow_col] == flow]
            d = d[d[geo_col].isin(GEO2ISO)]
            d = d.dropna(subset=["value", "year"])
            d = d[d.value > 0]
            d = d[d.year.between(2018, 2024)]
            d = attach_shock(d, inten, geo_col=geo_col)
            d["logv"] = np.log(d.value)
            d["post"] = (d.year >= 2023).astype(float)
            d["p_tnlg"] = d.post * d.d_tnlg_M_2324
            return d

        for item, partner, lab in [
            ("SJ312", "IN", "Indian SJ312 engineering"),
            ("SJ312", "CN_X_HK", "Chinese SJ312 engineering"),
            ("SJ311", "IN", "Indian SJ311 architecture"),
            ("SJ3", "IN", "Indian ITS SJ3"),
            ("SE", "CN_X_HK", "Chinese ITS construction"),
        ]:
            d = its_panel(item, partner)
            if d.empty:
                # try partner CN if CN_X_HK missing
                if partner == "CN_X_HK":
                    d = its_panel(item, "CN")
            out = fit_fe(d, "logv", ["p_tnlg"], ["importer", "year"], "importer") if not d.empty else None
            n = len(out[1]) if out else 0
            results.append(row(
                f"A4 log {lab} Post×ΔTNLG", out[0] if out else None, "p_tnlg", n,
                "Eurostat ITS; missing years dropped", "A4" if "Indian" in lab else "A5",
            ))

        # Mix: need both IN and CN SJ312 in same year
        a = its_panel("SJ312", "IN")[["importer", "year", "value", "d_tnlg_M_2324"]]
        b = its_panel("SJ312", "CN_X_HK")
        if b.empty:
            b = its_panel("SJ312", "CN")
        b = b[["importer", "year", "value"]].rename(columns={"value": "cn"})
        mix = a.merge(b, on=["importer", "year"])
        mix = mix[(mix.value > 0) & (mix.cn > 0)]
        mix["logv"] = np.log(mix.value) - np.log(mix.cn)
        mix["post"] = (mix.year >= 2023).astype(float)
        mix["p_tnlg"] = mix.post * mix.d_tnlg_M_2324
        out = fit_fe(mix, "logv", ["p_tnlg"], ["importer", "year"], "importer") if not mix.empty else None
        results.append(row(
            "A4 Mix log(IN SJ312)−log(CN SJ312)", out[0] if out else None, "p_tnlg",
            len(out[1]) if out else 0, "ITS engineering mix; missing years dropped", "A4",
        ))

    # Placebo partners if corroboration file exists
    plc = PROBE / "eurostat_its_sj312_placebos.csv"
    if plc.exists():
        pld = pd.read_csv(plc)
        pld["year"] = pd.to_numeric(pld.get("time", pld.get("year")), errors="coerce")
        pld["value"] = pd.to_numeric(pld.value, errors="coerce")
        geo_col = "geo" if "geo" in pld.columns else "reporter"
        partner_col = "partner" if "partner" in pld.columns else None
        flow_col = "stk_flow" if "stk_flow" in pld.columns else None
        if partner_col:
            for partner, lab in [
                ("US", "US SJ312"), ("UK", "UK SJ312"), ("CH", "CH SJ312"),
                ("JP", "JP SJ312"), ("EXT_EU27_2020", "extra-EU SJ312"),
            ]:
                d = pld[pld[partner_col] == partner].copy()
                if flow_col:
                    d = d[d[flow_col] == "DEB"]
                d = d[d[geo_col].isin(GEO2ISO) & (d.value > 0) & d.year.between(2018, 2024)]
                d = attach_shock(d, inten, geo_col=geo_col)
                d["logv"] = np.log(d.value)
                d["post"] = (d.year >= 2023).astype(float)
                d["p_tnlg"] = d.post * d.d_tnlg_M_2324
                out = fit_fe(d, "logv", ["p_tnlg"], ["importer", "year"], "importer") if not d.empty else None
                results.append(row(
                    f"A5 log {lab} Post×ΔTNLG", out[0] if out else None, "p_tnlg",
                    len(out[1]) if out else 0, "ITS placebo partner", "A5",
                ))

    batis = pd.read_csv(TRADE / "batis_civil_related.csv")
    batis = batis[batis.ADJUSTMENT == "B"].copy()
    batis["year"] = batis.TIME_PERIOD.astype(int)
    batis["value"] = pd.to_numeric(batis.OBS_VALUE, errors="coerce")

    def batis_panel(svc, partner):
        d = batis[
            (batis.TRADE_FLOW == "M")
            & (batis.SERVICE == svc)
            & (batis.COUNTERPART_AREA == partner)
            & batis.REF_AREA.isin(EU17)
            & batis.year.between(2018, 2024)
        ].copy()
        d = d.rename(columns={"REF_AREA": "iso3"})
        d = attach_shock(d, inten)
        d = d[d.value > 0]
        d["logv"] = np.log(d.value)
        d["post"] = (d.year >= 2023).astype(float)
        d["p_tnlg"] = d.post * d.d_tnlg_M_2324
        return d

    for svc, partner, lab in [
        ("SJ3", "IND", "Indian SJ3 (BaTIS B)"),
        ("SE", "CHN", "Chinese SE (BaTIS B)"),
        ("SJ3", "CHN", "Chinese SJ3 (BaTIS B)"),
        ("SI", "IND", "Indian SI (BaTIS B)"),
    ]:
        d = batis_panel(svc, partner)
        out = fit_fe(d, "logv", ["p_tnlg"], ["importer", "year"], "importer")
        results.append(row(
            f"A4 log {lab} Post×ΔTNLG", out[0] if out else None, "p_tnlg",
            len(out[1]) if out else 0, "BaTIS adjustment B; OBS_STATUS I in 2024",
            "A4" if "Indian SJ3" in lab else "A5",
        ))

    ind_sj3 = batis_panel("SJ3", "IND")[["importer", "year", "value", "d_tnlg_M_2324"]]
    cn_se = batis_panel("SE", "CHN")[["importer", "year", "value"]].rename(columns={"value": "cn"})
    mixb = ind_sj3.merge(cn_se, on=["importer", "year"])
    mixb = mixb[(mixb.value > 0) & (mixb.cn > 0)]
    mixb["logv"] = np.log(mixb.value) - np.log(mixb.cn)
    mixb["post"] = (mixb.year >= 2023).astype(float)
    mixb["p_tnlg"] = mixb.post * mixb.d_tnlg_M_2324
    out = fit_fe(mixb, "logv", ["p_tnlg"], ["importer", "year"], "importer")
    results.append(row(
        "A4 Mix log(IN SJ3)−log(CN SE)", out[0] if out else None, "p_tnlg",
        len(out[1]) if out else 0, "BaTIS B task-vs-project mix", "A4",
    ))

    # A6 size-class shock if retrieved
    size_path = NEW / "eurostat_tnlg_sizeclass.csv"
    if size_path.exists():
        sz = pd.read_csv(size_path)
        sz["value"] = pd.to_numeric(sz.value, errors="coerce")
        # ΔTNLG 2023–24 by size, NACE M
        wide = []
        for geo in GEO2ISO:
            rec = {"geo": geo, "iso3": GEO2ISO[geo]}
            for size in sorted(sz.size_emp.unique()):
                s = sz[(sz.geo == geo) & (sz.nace == "M") & (sz.indic == "E_AI_TNLG") & (sz.size_emp == size)]
                v23 = s[s.year == 2023]
                v24 = s[s.year == 2024]
                rec[f"d_{size}"] = (
                    float(v24.value.iloc[0]) - float(v23.value.iloc[0])
                    if len(v23) and len(v24) else np.nan
                )
            wide.append(rec)
        wide = pd.DataFrame(wide)
        wide.to_csv(TAB / "tnlg_sizeclass_delta.csv", index=False)
        d = sbs[(sbs.nace == "M71") & (sbs.indic == "NETTUR_MEUR") & (sbs.dataset == "sbs_sc_ovw")].copy()
        d["value"] = pd.to_numeric(d.value, errors="coerce")
        d = attach_shock(d, inten)
        d = d.merge(wide.drop(columns=["geo"], errors="ignore"), on="iso3", how="left")
        d = d[d.iso3.isin(EU17) & d.year.between(2021, 2024) & (d.value > 0)]
        d["logv"] = np.log(d.value)
        d["post24"] = (d.year >= 2024).astype(float)
        for col in [c for c in wide.columns if c.startswith("d_")]:
            if wide[col].notna().sum() < 8:
                results.append(row(
                    f"A6 M71 turnover × {col}", None, col, 0,
                    "size-class ΔTNLG too sparse; not estimated", "A6",
                ))
                continue
            d[f"p_{col}"] = d.post24 * d[col]
            out = fit_fe(d, "logv", [f"p_{col}"], ["importer", "year"], "importer")
            results.append(row(
                f"A6 log M71 turnover Post×{col}", out[0] if out else None, f"p_{col}",
                len(out[1]) if out else 0, "Size-class TNLG shock", "A6",
            ))

    # Vacancies / hours if published through 2024
    for fname, yname in [
        (NEW / "eurostat_job_vacancies.csv", "job vacancy rate"),
        (NEW / "eurostat_hours_M71_F_M.csv", "hours"),
        (NEW / "eurostat_sts_turnover.csv", "STS turnover index"),
    ]:
        if not fname.exists():
            results.append(row(
                f"A6 {yname}", None, "p24_tnlg", 0,
                f"{fname.name} not published in this pull", "A6",
            ))
            continue
        extra = pd.read_csv(fname)
        extra["value"] = pd.to_numeric(extra.value, errors="coerce")
        extra["year"] = extra.year.astype(int)
        # Prefer M71 then M
        for nace in ["M71", "M", "F"]:
            d = extra[extra.nace == nace].copy()
            if "indic" in d.columns and d.indic.nunique() > 1:
                prefer = "JOBRATE" if "JOBRATE" in set(d.indic) else d.indic.iloc[0]
                d = d[d.indic == prefer]
            if d.empty or d.year.max() < 2024:
                continue
            d = d[d.value > 0]
            d = attach_shock(d, inten)
            d = d[d.iso3.isin(EU17) & d.year.between(2018, 2024)]
            if d[["iso3", "year"]].drop_duplicates().shape[0] < 16:
                continue
            d["logv"] = np.log(d.value)
            d["post24"] = (d.year >= 2024).astype(float)
            d["p24_tnlg"] = d.post24 * d.d_tnlg_M_2324
            out = fit_fe(d, "logv", ["p24_tnlg"], ["importer", "year"], "importer")
            results.append(row(
                f"A6 log {nace} {yname} Post2024×ΔTNLG", out[0] if out else None,
                "p24_tnlg", len(out[1]) if out else 0,
                f"{fname.name}; missing years dropped", "A6",
            ))
            break

    t = pd.DataFrame(results)
    t.to_csv(TAB / "ai_impact_estimates.csv", index=False)

    # A7 magnitude for headline domestic coefficients
    mag_rows = []
    for spec in [
        "A1 log M71 turnover",
        "A1 log M71 employment",
        "A1 log M71 wages",
        "A1 log M71 value added",
        "A2 log M71 labour productivity (LABPRY)",
        "A2 log M71 labour cost per employed (LC_EMP)",
        "A4 log Indian SJ3 (BaTIS B) Post×ΔTNLG",
        "A4 Mix log(IN SJ312)−log(CN SJ312)",
    ]:
        hit = t[t.spec == spec]
        if hit.empty or pd.isna(hit.coef.iloc[0]):
            continue
        b = float(hit.coef.iloc[0])
        mag_rows.append({
            "spec": spec,
            "beta": b,
            "se": float(hit.se.iloc[0]),
            "display": hit.display.iloc[0],
            "pct_per_pp": 100 * b,
            "iqr_dlog": b * iqr,
            "iqr_pct": 100 * (np.exp(b * iqr) - 1),
            "iqr_pp": iqr,
        })
    mag = pd.DataFrame(mag_rows)
    mag.to_csv(TAB / "ai_impact_magnitude.csv", index=False)

    headline = {
        "identification": "EU-17; ΔTNLG NACE M 2024 minus 2023; not UK/IN/CN NLG",
        "cannot_identify": [
            "Generative AI caused civil jobs or GDP to move from the UK to India",
            "M71-specific AI adoption",
            "Civil-only invoices inside SJ312",
        ],
        "shock": shock_desc,
        "estimates": t.to_dict(orient="records"),
        "magnitude": mag.to_dict(orient="records"),
    }
    (NEW / "results_ai_impact.json").write_text(json.dumps(headline, indent=2, default=str))

    # Figures
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    gg = inten.sort_values("d_tnlg_M_2324")
    ax.barh(gg.country, gg.d_tnlg_M_2324, color="#3b6ea5")
    ax.axvline(0, color="0.4", lw=0.7)
    ax.set_xlabel("Percentage-point change in NLG use, NACE M, 2023–24")
    ax.set_title("Generative-AI shock used in the impact design")
    fig.tight_layout()
    fig.savefig(FIG / "figure_tnlg_shock.png")
    plt.close()

    # Productivity vs turnover coefficients plot from table
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    show = t[t.spec.isin([
        "A1 log M71 turnover", "A1 log M71 employment", "A1 log M71 wages",
        "A1 log M71 value added", "A2 log M71 labour productivity (LABPRY)",
        "A2 log M71 labour cost per employed (LC_EMP)",
    ])].copy()
    if not show.empty and show.coef.notna().any():
        y = np.arange(len(show))
        ax.errorbar(show.coef, y, xerr=show.se, fmt="o", color="#3b6ea5", capsize=3)
        ax.axvline(0, color="0.4", lw=0.7)
        ax.set_yticks(y, show.spec.str.replace("A1 log ", "").str.replace("A2 log ", ""))
        ax.set_xlabel("Post-2024 × ΔTNLG coefficient (log points)")
        ax.set_title("Domestic M71 outcomes under the NLG shock")
        fig.tight_layout()
        fig.savefig(FIG / "figure_m71_impact.png")
    plt.close()

    print("\nESTIMATES")
    print(t[["layer", "spec", "display", "n"]].to_string(index=False))
    print("\nMAGNITUDE")
    print(mag.to_string(index=False) if not mag.empty else "empty")


if __name__ == "__main__":
    main()
