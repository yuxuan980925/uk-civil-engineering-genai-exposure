#!/usr/bin/env python3
"""Reset research questions for GenAI and *transnational civil-engineering
relocation*, then run only the tests the official series can support.

Claim boundary
--------------
Causal relocation of ISCO 2142 jobs or partner GDP is not identified.
The tests below are associations and descriptive composition checks.

Reset questions
---------------
RQ1 Coverage. Does Eurostat ITS publish bilateral engineering services
    (SJ312 / SJ31) for EU importers × India/China after 2022?
RQ2 Digitally deliverable association. Among EU importers, is the 2023–24
    NACE M NLG jump associated with Indian SJ3 (BaTIS B) and, where N
    permits, Indian SJ31/SJ312 (Eurostat ITS)?
RQ3 Project-based falsification. Is the same shock associated with Chinese
    construction services (SE)? Relocation-as-projects predicts a positive
    coefficient; a null rejects that channel in these data.
RQ4 Relocation index. Does Δlog Indian SJ3 minus Δlog Chinese SE, 2022–24,
    rise with importer ΔTNLG?
RQ5 Domestic inconsistency with headcount offshoring. Is M71 employment
    flat while M71 turnover slows and Indian SJ3 rises where NLG jumped?
RQ6 Reported vs balanced BaTIS. Do reported (N) Indian SJ3 cells, which
    end in 2023 for the EU panel, change the Post-2023 association?
RQ7 UK occupation composition (descriptive). After 2022, did high-exposure
    civil occupations (SOC 2121, 3120) fall relative to technicians (3114)
    and a non-civil comparison (2114)? Not an identified AI effect.
RQ8 EU occupation composition (descriptive). Did ISCO OC21 (science and
    engineering professionals) change after 2022 relative to OC25 (ICT
    professionals) and OC31 (engineering associate professionals)?
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
EXT = ROOT / "04_external_indices"
PROBE = ROOT / "09_relocation_probe"
TAB = PROBE / "tables"
FIG = PROBE / "figures"
for p in (PROBE, TAB, FIG):
    p.mkdir(parents=True, exist_ok=True)

GEO2ISO = {
    "DE": "DEU", "FR": "FRA", "NL": "NLD", "PL": "POL", "RO": "ROU",
    "IT": "ITA", "ES": "ESP", "IE": "IRL", "BE": "BEL", "AT": "AUT",
    "SE": "SWE", "DK": "DNK", "PT": "PRT", "CZ": "CZE", "HU": "HUN",
    "FI": "FIN", "EL": "GRC", "UK": "GBR",
}
ISO2GEO = {v: k for k, v in GEO2ISO.items()}
EU17 = [
    "DEU", "FRA", "NLD", "POL", "ROU", "ITA", "ESP", "IRL", "BEL",
    "AUT", "SWE", "DNK", "PRT", "CZE", "HUN", "FIN", "GRC",
]


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
        "rq": rq,
        "spec": name,
        "coef": float(res.params[key]),
        "se": float(res.bse[key]),
        "p": float(res.pvalues[key]),
        "n": n,
        "r2": float(res.rsquared),
        "note": note,
        "display": fmt(res.params[key], res.bse[key], res.pvalues[key]),
    }


def load_intensity():
    """Rebuild NACE M TNLG 2023–24 from official Eurostat extracts."""
    g = pd.read_csv(AI / "eurostat_ai_genai_types.csv")
    g["value"] = pd.to_numeric(g.value, errors="coerce")
    g["year"] = g.time.astype(int)
    extra_path = AI / "eurostat_ai_nace_placebos.csv"
    frames = [g[["nace", "geo", "year", "value"]].assign(indic=g["indic"])]
    if extra_path.exists():
        extra = pd.read_csv(extra_path)
        extra["value"] = pd.to_numeric(extra.value, errors="coerce")
        extra["year"] = extra.year.astype(int)
        indic = extra["indic"] if "indic" in extra.columns else extra["indic_is"]
        frames.append(extra[["nace", "geo", "year", "value"]].assign(indic=indic))
    all_ = pd.concat(frames, ignore_index=True)
    all_ = all_.drop_duplicates(["nace", "geo", "indic", "year"])
    recs = []
    for geo, iso in GEO2ISO.items():
        if iso not in EU17:
            continue
        r = {"geo": geo, "iso3": iso}
        s = all_[(all_.geo == geo) & (all_.indic == "E_AI_TNLG") & (all_.nace == "M")]
        for y in (2021, 2023, 2024, 2025):
            hit = s[s.year == y]
            r[f"tnlg_M_{y}"] = float(hit.value.iloc[0]) if len(hit) else np.nan
        recs.append(r)
    inten = pd.DataFrame(recs)
    inten["d_tnlg_M_2324"] = inten.tnlg_M_2024 - inten.tnlg_M_2023
    inten["d_tnlg_M_2124"] = inten.tnlg_M_2024 - inten.tnlg_M_2021
    return inten, all_


def load_batis(adjustment: str) -> pd.DataFrame:
    df = pd.read_csv(TRADE / "batis_civil_related.csv", low_memory=False)
    df = df[df.ADJUSTMENT == adjustment].copy()
    df["year"] = df.TIME_PERIOD.astype(int)
    df["value"] = pd.to_numeric(df.OBS_VALUE, errors="coerce")
    df = df.dropna(subset=["value"])
    df = df.drop_duplicates(
        ["REF_AREA", "COUNTERPART_AREA", "TRADE_FLOW", "SERVICE", "year"]
    )
    return df


def make_imports(batis, service, partners):
    m = batis[
        (batis.TRADE_FLOW == "M")
        & (batis.SERVICE == service)
        & (batis.COUNTERPART_AREA.isin(partners))
    ].copy()
    return m.rename(columns={"REF_AREA": "importer", "COUNTERPART_AREA": "partner"})[
        ["importer", "partner", "year", "value"]
    ]


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
    fe = ["importer", "year"]
    if "partner" in dat.columns and dat.partner.nunique() > 1:
        fe.append("partner")
    out = fit_fe(dat, "logv", extra, fe, "importer")
    if out is None:
        results.append(row(name, None, key, len(dat), note + " [N too small]", rq))
        return
    res, used = out
    results.append(row(name, res, key, len(used), note, rq))


def load_its():
    path = PROBE / "eurostat_its_engineering.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    df["value"] = pd.to_numeric(df.value, errors="coerce")
    df = df.dropna(subset=["value"])
    df["iso3"] = df.geo.map(GEO2ISO)
    return df


def its_to_trade(its, item, partner, flow="DEB"):
    if its.empty:
        return pd.DataFrame(columns=["importer", "partner", "year", "value"])
    pcode = {"IND": "IN", "CHN": "CN_X_HK", "PHL": "PH", "VNM": "VN"}[partner]
    m = its[
        (its.bop_item == item)
        & (its.stk_flow == flow)
        & (its.partner == pcode)
        & its.iso3.isin(EU17)
    ].copy()
    m = m.rename(columns={"iso3": "importer"})
    m["partner"] = partner
    return m[["importer", "partner", "year", "value"]]


def main():
    plt.rcParams.update({
        "figure.dpi": 140, "savefig.dpi": 200, "font.size": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.25,
    })
    results = []
    notes = []
    inten, _ai = load_intensity()
    inten.to_csv(TAB / "table_tnlg_intensity.csv", index=False)

    batis_b = load_batis("B")
    batis_n = load_batis("N")
    its = load_its()

    # ----- RQ1 coverage -----
    cov_path = PROBE / "coverage_eurostat_its.csv"
    if cov_path.exists():
        cov = pd.read_csv(cov_path)
    else:
        cov = pd.DataFrame()
    rq1 = {
        "sj312_published_in_eurostat_its": bool(
            not its.empty and (its.bop_item == "SJ312").any()
        ),
        "sj312_india_debit_cells": int(
            len(its[(its.bop_item == "SJ312") & (its.partner == "IN") & (its.stk_flow == "DEB")])
        ) if not its.empty else 0,
        "sj312_india_geos_2024": int(
            its[(its.bop_item == "SJ312") & (its.partner == "IN") & (its.stk_flow == "DEB") & (its.year == 2024)].geo.nunique()
        ) if not its.empty else 0,
        "sj312_india_geos_with_2022_and_2024": int(
            len(
                set(its[(its.bop_item == "SJ312") & (its.partner == "IN") & (its.stk_flow == "DEB") & (its.year == 2022)].geo)
                & set(its[(its.bop_item == "SJ312") & (its.partner == "IN") & (its.stk_flow == "DEB") & (its.year == 2024)].geo)
            )
        ) if not its.empty else 0,
        "uk_its_max_year": int(its[its.geo == "UK"].year.max()) if (not its.empty and (its.geo == "UK").any()) else None,
        "batis_sj312": "not published (OECD SDMX 404)",
        "ilo_isco_2142": "not published in this pull",
    }
    (TAB / "rq1_coverage.json").write_text(json.dumps(rq1, indent=2))
    notes.append("RQ1: Eurostat ITS publishes SJ312 but cells are sparse; BaTIS SJ312 unpublished; ILO 2142 unpublished.")

    # ----- RQ2 / RQ3 BaTIS B (preferred, includes 2024) -----
    sj3_ind = make_imports(batis_b, "SJ3", ["IND"])
    sj3_pool = make_imports(batis_b, "SJ3", ["IND", "PHL", "VNM"])
    se_chn = make_imports(batis_b, "SE", ["CHN"])
    si_ind = make_imports(batis_b, "SI", ["IND"])
    sj3_chn = make_imports(batis_b, "SJ3", ["CHN"])
    se_ind = make_imports(batis_b, "SE", ["IND"])

    p_ind = build_panel(sj3_ind, inten)
    p_pool = build_panel(sj3_pool, inten)
    p_se = build_panel(se_chn, inten)
    p_si = build_panel(si_ind, inten)
    p_sj3c = build_panel(sj3_chn, inten)
    p_sei = build_panel(se_ind, inten)

    run_spec(results, "RQ2a Indian SJ3 Post×ΔM TNLG (BaTIS B)", p_ind,
             "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
             "Preferred balanced series; includes 2024", "RQ2")
    run_spec(results, "RQ2b Indian SJ3 Post2024×ΔM TNLG (BaTIS B)", p_ind,
             "p24_x_d_tnlg_M_2324", ["p24_x_d_tnlg_M_2324"],
             "Treat only 2024 as post", "RQ2")
    run_spec(results, "RQ2c Pooled SJ3 IND/PHL/VNM Post×ΔM TNLG (BaTIS B)", p_pool,
             "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
             "Partner FE", "RQ2")
    run_spec(results, "RQ3a Chinese SE Post×ΔM TNLG (BaTIS B)", p_se,
             "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
             "Project-based comparison; not a GATS mode", "RQ3")
    run_spec(results, "RQ3b Indian SI Post×ΔM TNLG (BaTIS B)", p_si,
             "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
             "Computer-services placebo", "RQ3")
    run_spec(results, "RQ3c Chinese SJ3 Post×ΔM TNLG (BaTIS B)", p_sj3c,
             "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
             "Same heading, different partner", "RQ3")
    run_spec(results, "RQ3d Indian SE Post×ΔM TNLG (BaTIS B)", p_sei,
             "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
             "Indian construction services (thin corridor)", "RQ3")

    # Eurostat ITS engineering, if enough cells
    for item, lab in [("SJ312", "engineering SJ312"), ("SJ31", "arch+eng SJ31"),
                      ("SJ311", "architectural SJ311"), ("SJ3", "ITS SJ3")]:
        tr = its_to_trade(its, item, "IND")
        panel = build_panel(tr, inten) if not tr.empty else pd.DataFrame()
        n_imp = int(tr.importer.nunique()) if not tr.empty else 0
        n_y = int(tr.year.nunique()) if not tr.empty else 0
        run_spec(
            results, f"RQ2d Indian {lab} Post×ΔM TNLG (Eurostat ITS)",
            panel if not panel.empty else pd.DataFrame({"logv": [], "importer": [], "year": [],
                                                       "post_x_d_tnlg_M_2324": []}),
            "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
            f"Official engineering heading; importers={n_imp}, years={n_y}; missing years not filled",
            "RQ2",
        )
        tr_cn = its_to_trade(its, item, "CHN")
        panel_cn = build_panel(tr_cn, inten) if not tr_cn.empty else pd.DataFrame()
        run_spec(
            results, f"RQ3e Chinese {lab} Post×ΔM TNLG (Eurostat ITS)",
            panel_cn if not panel_cn.empty else pd.DataFrame(
                {"logv": [], "importer": [], "year": [], "post_x_d_tnlg_M_2324": []}
            ),
            "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
            "Same official heading from China except Hong Kong",
            "RQ3",
        )
        if not tr.empty:
            w = tr[tr.year.isin([2022, 2024])].pivot_table(
                index="importer", columns="year", values="value"
            )
            if 2022 in w.columns and 2024 in w.columns:
                w = w.dropna(subset=[2022, 2024]).reset_index()
                w["dlog"] = np.log(w[2024].clip(lower=0.01)) - np.log(w[2022].clip(lower=0.01))
                w = w.merge(inten, left_on="importer", right_on="iso3")
                w = w.dropna(subset=["dlog", "d_tnlg_M_2324"])
                w.to_csv(TAB / f"cross_section_{item}_india.csv", index=False)
                if len(w) >= 6:
                    rA = sm.OLS(w.dlog, sm.add_constant(w["d_tnlg_M_2324"])).fit(cov_type="HC1")
                    results.append(row(
                        f"RQ2e Cross-section Δlog IN {lab} 22–24 on ΔTNLG",
                        rA, "d_tnlg_M_2324", len(w),
                        "No FE; only reporters with both 2022 and 2024 published",
                        "RQ2",
                    ))
                else:
                    results.append(row(
                        f"RQ2e Cross-section Δlog IN {lab} 22–24 on ΔTNLG",
                        None, "d_tnlg_M_2324", len(w),
                        f"Only {len(w)} reporters publish both 2022 and 2024",
                        "RQ2",
                    ))

    # ----- RQ4 relocation index -----
    a = sj3_ind.rename(columns={"value": "sj3_ind"})
    b = se_chn.rename(columns={"value": "se_chn"})
    idx = a.merge(b[["importer", "year", "se_chn"]], on=["importer", "year"], how="inner")
    idx = idx[idx.importer.isin(EU17) & idx.year.between(2018, 2024)]
    idx["reloc"] = np.log(idx.sj3_ind.clip(lower=0.01)) - np.log(idx.se_chn.clip(lower=0.01))
    idx = idx.merge(inten, left_on="importer", right_on="iso3", how="left")
    idx["post"] = (idx.year >= 2023).astype(float)
    idx["post24"] = (idx.year >= 2024).astype(float)
    idx["logv"] = idx.reloc
    idx["post_x_d_tnlg_M_2324"] = idx.post * idx.d_tnlg_M_2324
    idx["p24_x_d_tnlg_M_2324"] = idx.post24 * idx.d_tnlg_M_2324
    idx["partner"] = "IDX"
    idx.to_csv(TAB / "relocation_index_panel.csv", index=False)
    run_spec(results, "RQ4a Relocation index log(IN SJ3)−log(CN SE) Post×ΔTNLG",
             idx, "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
             "Positive = Indian technical services rose relative to Chinese construction", "RQ4")
    run_spec(results, "RQ4b Same index, Post2024×ΔTNLG",
             idx, "p24_x_d_tnlg_M_2324", ["p24_x_d_tnlg_M_2324"],
             "2024 only", "RQ4")

    # Official engineering heading analogue of the relocation index
    its_in = its_to_trade(its, "SJ312", "IND")
    its_cn = its_to_trade(its, "SJ312", "CHN").rename(columns={"value": "sj312_cn"})
    if not its_in.empty and not its_cn.empty:
        ix2 = its_in.rename(columns={"value": "sj312_ind"}).merge(
            its_cn[["importer", "year", "sj312_cn"]], on=["importer", "year"], how="inner"
        )
        ix2 = ix2[ix2.importer.isin(EU17) & ix2.year.between(2018, 2024)]
        if not ix2.empty:
            ix2["reloc"] = np.log(ix2.sj312_ind.clip(lower=0.01)) - np.log(ix2.sj312_cn.clip(lower=0.01))
            ix2 = ix2.merge(inten, left_on="importer", right_on="iso3", how="left")
            ix2["post"] = (ix2.year >= 2023).astype(float)
            ix2["logv"] = ix2.reloc
            ix2["post_x_d_tnlg_M_2324"] = ix2.post * ix2.d_tnlg_M_2324
            ix2["partner"] = "IDX312"
            ix2.to_csv(TAB / "relocation_index_sj312_panel.csv", index=False)
            run_spec(
                results, "RQ4d ITS index log(IN SJ312)−log(CN SJ312) Post×ΔTNLG",
                ix2, "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
                "Engineering services only; unbalanced (missing years dropped, not filled)",
                "RQ4",
            )

    chg = idx[idx.year.isin([2022, 2024])].pivot_table(
        index="importer", columns="year", values="reloc"
    )
    if 2022 in chg.columns and 2024 in chg.columns:
        chg = chg.dropna().reset_index()
        chg["d_reloc"] = chg[2024] - chg[2022]
        chg = chg.merge(inten, left_on="importer", right_on="iso3")
        chg = chg.dropna(subset=["d_reloc", "d_tnlg_M_2324"])
        chg.to_csv(TAB / "cross_section_relocation_index.csv", index=False)
        if len(chg) >= 8:
            rA = sm.OLS(chg.d_reloc, sm.add_constant(chg["d_tnlg_M_2324"])).fit(cov_type="HC1")
            results.append(row(
                "RQ4c Cross-section Δrelocation index 22–24 on ΔTNLG",
                rA, "d_tnlg_M_2324", len(chg),
                "One observation per importer", "RQ4",
            ))
            fig, ax = plt.subplots(figsize=(6.8, 4.8))
            ax.scatter(chg.d_tnlg_M_2324, chg.d_reloc)
            for _, r in chg.iterrows():
                ax.annotate(r.importer, (r.d_tnlg_M_2324, r.d_reloc),
                            textcoords="offset points", xytext=(4, 4), fontsize=8)
            ax.set_xlabel("NACE M NLG, 2024 minus 2023 (pp)")
            ax.set_ylabel("Δ [log IN SJ3 − log CN SE], 2022–24")
            ax.set_title("NLG jump and the Indian-SJ3 vs Chinese-SE shift")
            fig.tight_layout()
            fig.savefig(FIG / "figure_relocation_index.png")
            plt.close()

    # ----- RQ5 domestic M71 vs trade -----
    sbs = pd.read_csv(IND / "eurostat_sbs_M71_F_M.csv")
    sbs["iso3"] = sbs.geo.map(GEO2ISO)
    sbs["value"] = pd.to_numeric(sbs.value, errors="coerce")
    sbs = sbs[sbs.iso3.isin(EU17)].copy()

    def sbs_pick(nace, indic):
        d = sbs[(sbs.nace == nace) & (sbs.indic == indic)]
        if indic == "NETTUR_MEUR":
            d = d[d.dataset == "sbs_sc_ovw"]
        else:
            d = d[d.dataset == "sbs_ovw_act"]
        return d[["iso3", "year", "value"]].rename(columns={"iso3": "importer"})

    for indic, lab in [("NETTUR_MEUR", "M71 turnover"), ("EMP_NR", "M71 employment"),
                       ("WAGE_MEUR", "M71 wages")]:
        d = sbs_pick("M71", indic)
        d = d[d.year.between(2021, 2024)]
        d = d.merge(inten, left_on="importer", right_on="iso3", how="left")
        d["logv"] = np.log(d.value.clip(lower=0.01))
        d["post24"] = (d.year >= 2024).astype(float)
        d["p24_x_d_tnlg_M_2324"] = d.post24 * d.d_tnlg_M_2324
        d["partner"] = "DOM"
        run_spec(results, f"RQ5 {lab} Post2024×ΔM TNLG",
                 d, "p24_x_d_tnlg_M_2324", ["p24_x_d_tnlg_M_2324"],
                 "SBS current prices; one complete post-shock year", "RQ5")

    # ----- RQ6 reported BaTIS N (ends 2023 for EU-IND SJ3) -----
    sj3_n = make_imports(batis_n, "SJ3", ["IND"])
    p_n = build_panel(sj3_n, inten, year0=2018, year1=2023)
    max_y = int(p_n.year.max()) if not p_n.empty else None
    run_spec(results, "RQ6a Indian SJ3 Post×ΔM TNLG (BaTIS reported N, ≤2023)",
             p_n, "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
             f"Reported cells; sample max year={max_y}; 2024 unpublished so Post=2023 only",
             "RQ6")
    # Compare 2019 and 2023 (last reported year) GBR and EU medians
    def corridor_change(df, adj_label):
        recs = []
        for importer, partner, svc in [
            ("GBR", "IND", "SJ3"), ("GBR", "CHN", "SJ3"),
            ("GBR", "IND", "SE"), ("GBR", "CHN", "SE"),
            ("GBR", "IND", "SI"), ("GBR", "CHN", "SI"),
        ]:
            sub = df[(df.REF_AREA == importer) & (df.COUNTERPART_AREA == partner)
                     & (df.SERVICE == svc) & (df.TRADE_FLOW == "M")]
            y0 = sub[sub.year == 2019]
            y1 = sub[sub.year == 2024]
            y1b = sub[sub.year == 2023]  # N often stops here
            recs.append({
                "adjustment": adj_label,
                "importer": importer,
                "partner": partner,
                "service": svc,
                "v2019": float(y0.value.iloc[0]) if len(y0) else np.nan,
                "v2023": float(y1b.value.iloc[0]) if len(y1b) else np.nan,
                "v2024": float(y1.value.iloc[0]) if len(y1) else np.nan,
            })
        return pd.DataFrame(recs)

    corr = pd.concat([
        corridor_change(batis_b, "B_balanced"),
        corridor_change(batis_n, "N_reported"),
        corridor_change(load_batis("F"), "F_adjusted_or_imputed"),
    ], ignore_index=True)
    corr.to_csv(TAB / "uk_corridors_B_vs_N.csv", index=False)

    # ----- RQ7 UK APS occupations -----
    aps_path = EXT / "from_study1" / "aps_employment_2021_2025.csv"
    if not aps_path.exists():
        aps_path = EXT / "from_legacy_study4" / "aps_employment_2021_2025.csv"
    aps = pd.read_csv(aps_path)
    aps["soc"] = aps.SOC2020_FULL_NAME.str.extract(r"^(\d{4})")
    aps["year"] = pd.to_datetime(aps.DATE).dt.year
    aps["value"] = pd.to_numeric(aps.OBS_VALUE, errors="coerce")
    keep = {
        "2121": "Civil engineers",
        "3120": "CAD, drawing and architectural technicians",
        "3114": "Building and civil engineering technicians",
        "2455": "Construction project managers",
        "2453": "Quantity surveyors",
        "2114": "Physical scientists (comparison)",
    }
    aps_k = aps[aps.soc.isin(keep)].copy()
    # Annual mean of available quarters
    ann = aps_k.groupby(["year", "soc"], as_index=False)["value"].mean()
    ann["name"] = ann.soc.map(keep)
    ann.to_csv(TAB / "uk_aps_annual.csv", index=False)
    pre = ann[ann.year.isin([2021, 2022])].groupby("soc")["value"].mean()
    post = ann[ann.year.isin([2023, 2024, 2025])].groupby("soc")["value"].mean()
    occ_tab = []
    for soc, name in keep.items():
        a, b = pre.get(soc, np.nan), post.get(soc, np.nan)
        occ_tab.append({
            "soc": soc, "name": name,
            "mean_2021_22": a, "mean_2023_25": b,
            "pct_change": 100 * (b / a - 1) if a and a > 0 else np.nan,
        })
    occ_df = pd.DataFrame(occ_tab)
    occ_df.to_csv(TAB / "uk_aps_prepost.csv", index=False)
    notes.append(
        "RQ7: UK APS is a national occupation series; there is no importer NLG "
        "treatment and no Indian/Chinese ISCO counterpart."
    )

    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    for soc, name in keep.items():
        s = ann[ann.soc == soc].sort_values("year")
        ax.plot(s.year, s.value / 1000, marker="o", label=f"{soc} {name.split('(')[0].strip()}")
    ax.axvline(2022.75, color="0.6", ls="--", lw=0.8)
    ax.set_ylabel("Employment (thousands, APS annual mean)")
    ax.set_title("UK civil-related occupations, 2021–2025")
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout()
    fig.savefig(FIG / "figure_uk_aps_occupations.png")
    plt.close()

    # ----- RQ8 EU LFS 2-digit occupations -----
    lfs_path = PROBE / "eurostat_lfsa_occ2d.csv"
    if lfs_path.exists():
        lfs = pd.read_csv(lfs_path)
        lfs["value"] = pd.to_numeric(lfs.value, errors="coerce")
        lfs["iso3"] = lfs.geo.map(GEO2ISO)
        recs = []
        for isco, lab in [
            ("OC21", "Science and engineering professionals"),
            ("OC31", "Science and engineering associate professionals"),
            ("OC25", "ICT professionals"),
            ("OC71", "Building trades workers"),
        ]:
            d = lfs[(lfs.isco08 == isco) & lfs.iso3.isin(EU17) & lfs.year.between(2018, 2024)].copy()
            d = d.merge(inten, on="iso3", how="left")
            d["logv"] = np.log(d.value.clip(lower=0.01))
            d["post"] = (d.year >= 2023).astype(float)
            d["post_x_d_tnlg_M_2324"] = d.post * d.d_tnlg_M_2324
            d["importer"] = d.iso3
            d["partner"] = "OCC"
            run_spec(results, f"RQ8 {lab} Post×ΔM TNLG",
                     d, "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
                     "ISCO 2-digit; not civil engineers (2142)", "RQ8")
            recs.append({"isco": isco, "label": lab, "n_cells": int(len(d.dropna(subset=["value"])))})
        pd.DataFrame(recs).to_csv(TAB / "lfs_occupation_counts.csv", index=False)

    t = pd.DataFrame(results)
    t.to_csv(TAB / "table_relocation_experiments.csv", index=False)
    pretty = t[["rq", "spec", "display", "n", "note"]].copy()
    pretty.columns = ["RQ", "Specification", "Coefficient (s.e.)", "N", "Note"]
    pretty.to_csv(TAB / "article_relocation_results.csv", index=False)

    # Event-study of relocation index
    es = idx.copy()
    year_d = pd.get_dummies(es.year.astype(int), prefix="y", dtype=float)
    inter = []
    for y in range(2018, 2025):
        if y == 2022:
            continue
        col = f"tnlg_y{y}"
        if f"y_{y}" not in year_d.columns:
            continue
        es[col] = year_d[f"y_{y}"] * es.d_tnlg_M_2324
        inter.append(col)
    out = fit_fe(es, "logv", inter, ["importer", "year"], "importer")
    es_rows = []
    if out:
        res, used = out
        for y in range(2018, 2025):
            if y == 2022:
                es_rows.append({"year": y, "coef": 0.0, "se": 0.0, "p": 1.0})
            else:
                k = f"tnlg_y{y}"
                es_rows.append({
                    "year": y,
                    "coef": float(res.params.get(k, np.nan)),
                    "se": float(res.bse.get(k, np.nan)),
                    "p": float(res.pvalues.get(k, np.nan)),
                })
        es_df = pd.DataFrame(es_rows)
        es_df.to_csv(TAB / "event_study_relocation_index.csv", index=False)
        fig, ax = plt.subplots(figsize=(8.2, 4.6))
        ax.axhline(0, color="0.4", lw=0.8)
        ax.axvline(2022.5, color="0.6", ls="--", lw=0.8, label="ChatGPT public release")
        ax.errorbar(es_df.year, es_df.coef, yerr=1.96 * es_df.se.replace({0: np.nan}),
                    fmt="o-", capsize=3)
        ax.set_xlabel("Year (2022 = reference)")
        ax.set_ylabel("Year × importer ΔM TNLG 2023–24")
        ax.set_title("Event study: Indian SJ3 minus Chinese SE")
        ax.legend(frameon=False)
        fig.tight_layout()
        fig.savefig(FIG / "figure_event_study_relocation.png")
        plt.close()

    payload = {
        "reset_question": (
            "Among EU importers, is the 2023–24 professional-service NLG jump "
            "associated with a shift toward digitally deliverable Indian technical "
            "services relative to Chinese construction services, and with slower "
            "nominal M71 turnover but not falling M71 employment — a pattern that "
            "would be consistent with task unbundling rather than civil-engineer "
            "headcount relocation?"
        ),
        "cannot_identify": [
            "Generative AI caused ISCO 2142 jobs to move between countries",
            "Civil-engineering GDP or national-income effects",
            "GATS Mode 1 vs Mode 3 switching",
            "UK, Indian or Chinese enterprise NLG as a treatment",
            "Bilateral SJ312 in BaTIS",
        ],
        "rq1_coverage": rq1,
        "results": results,
        "notes": notes,
    }
    (PROBE / "results_relocation.json").write_text(json.dumps(payload, indent=2, default=str))
    print(t[["rq", "spec", "display", "n"]].to_string(index=False))
    print("RQ1", json.dumps(rq1, indent=2))


if __name__ == "__main__":
    main()
