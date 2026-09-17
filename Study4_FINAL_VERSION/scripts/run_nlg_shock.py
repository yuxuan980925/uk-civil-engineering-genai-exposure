#!/usr/bin/env python3
"""Preferred AI shock: Eurostat generative NLG (E_AI_TNLG), NACE M vs F/C/J/N.

Generic E_AI_TANY mixes pre-ChatGPT ML with GenAI. TNLG is the language-generation
item whose 2023–24 jump is the identification window. TML/TTM/TIR are technology
placebos; construction and ICT/manufacturing TNLG are sector placebos.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
DATA, TAB, FIG = ROOT / "data", ROOT / "tables", ROOT / "figures"
TAB.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

GEO2ISO = {
    "DE": "DEU", "FR": "FRA", "NL": "NLD", "PL": "POL", "RO": "ROU", "IT": "ITA",
    "ES": "ESP", "IE": "IRL", "BE": "BEL", "AT": "AUT", "SE": "SWE", "DK": "DNK",
    "PT": "PRT", "CZ": "CZE", "HU": "HUN", "FI": "FIN", "EL": "GRC",
}
ISO2NAME = {
    "DEU": "Germany", "FRA": "France", "NLD": "Netherlands", "POL": "Poland",
    "ROU": "Romania", "ITA": "Italy", "ESP": "Spain", "IRL": "Ireland",
    "BEL": "Belgium", "AUT": "Austria", "SWE": "Sweden", "DNK": "Denmark",
    "PRT": "Portugal", "CZE": "Czechia", "HUN": "Hungary", "FIN": "Finland",
    "GRC": "Greece",
}
MODE1 = ["IND", "PHL", "VNM"]


def star(p):
    if pd.isna(p):
        return ""
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def fmt(b, se, p):
    if pd.isna(b):
        return "—"
    return f"{b:.3f}{star(p)} ({se:.3f})"


def fit_fe(df, y, x, fe, cluster=None):
    df = df.loc[:, ~df.columns.duplicated()].copy()
    use = list(dict.fromkeys([y] + x + fe + ([cluster] if cluster else [])))
    d = df[use].dropna().copy().reset_index(drop=True)
    if len(d) < 20:
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
            cov_type="cluster", cov_kwds={"groups": d[cluster], "use_correction": True}
        )
    else:
        res = sm.OLS(yv, X).fit(cov_type="HC1")
    sst = float(np.sum((d[y] - d[y].mean()) ** 2))
    res.rsquared = 1 - float(np.sum(res.resid**2) / sst) if sst else np.nan
    return res, d


def row(name, res, key, n, note):
    if key not in res.params:
        return {
            "spec": name, "coef": np.nan, "se": np.nan, "p": np.nan, "n": n,
            "r2": float(res.rsquared), "note": note, "display": "—",
        }
    return {
        "spec": name,
        "coef": float(res.params[key]),
        "se": float(res.bse[key]),
        "p": float(res.pvalues[key]),
        "n": n,
        "r2": float(res.rsquared),
        "note": note,
        "display": fmt(res.params[key], res.bse[key], res.pvalues[key]),
    }


def load_types():
    g = pd.read_csv(DATA / "eurostat_ai_genai_types.csv")
    g["value"] = pd.to_numeric(g.value, errors="coerce")
    g["year"] = g.time.astype(int)
    extra = pd.read_csv(DATA / "eurostat_ai_nace_placebos.csv")
    extra["value"] = pd.to_numeric(extra.value, errors="coerce")
    extra = extra.rename(columns={"indic": "indic_is"}) if "indic_is" not in extra.columns else extra
    if "indic" in extra.columns and extra.get("indic_is") is extra.get("indic"):
        pass
    extra = extra.rename(columns={"indic": "indic"})
    extra["nace"] = extra.nace
    extra["year"] = extra.year.astype(int)
    extra["geo"] = extra.geo
    # unify extra to same columns
    e2 = extra[["nace", "geo", "year", "value"]].copy()
    e2["indic"] = extra["indic"] if "indic" in extra.columns else extra["indic_is"]
    g2 = g[["nace", "geo", "year", "value", "indic"]].copy()
    all_ = pd.concat([g2, e2], ignore_index=True)
    all_ = all_.drop_duplicates(["nace", "geo", "indic", "year"])
    return all_


def intensity(all_):
    recs = []
    countries = [g for g in all_.geo.unique() if g in GEO2ISO]
    for geo in countries:
        r = {"geo": geo, "iso3": GEO2ISO[geo]}
        for indic, nace, lab in [
            ("E_AI_TNLG", "M", "tnlg_M"),
            ("E_AI_TNLG", "F", "tnlg_F"),
            ("E_AI_TML", "M", "tml_M"),
            ("E_AI_TTM", "M", "ttm_M"),
            ("E_AI_TIR", "M", "tir_M"),
            ("E_AI_TNLG", "C", "tnlg_C"),
            ("E_AI_TNLG", "J", "tnlg_J"),
            ("E_AI_TNLG", "N", "tnlg_N"),
            ("E_AI_TANY", "C", "tany_C"),
            ("E_AI_TANY", "J", "tany_J"),
        ]:
            s = all_[(all_.geo == geo) & (all_.indic == indic) & (all_.nace == nace)]
            for y in (2021, 2023, 2024, 2025):
                hit = s[s.year == y]
                r[f"{lab}_{y}"] = float(hit.value.iloc[0]) if len(hit) else np.nan
        recs.append(r)
    inten = pd.DataFrame(recs)
    # generic TANY from existing raw
    tany = pd.read_csv(DATA / "eurostat_ai_raw.csv")
    tany = tany[tany.geo.isin(GEO2ISO)]
    tany["iso3"] = tany.geo.map(GEO2ISO)
    w = tany.pivot_table(index="iso3", columns=["nace", "year"], values="ai_pct")
    for y in (2021, 2023, 2024, 2025):
        if ("M", y) in w.columns:
            inten = inten.merge(
                w[("M", y)].rename(f"tany_M_{y}").reset_index(),
                on="iso3",
                how="left",
            )
        if ("F", y) in w.columns:
            inten = inten.merge(
                w[("F", y)].rename(f"tany_F_{y}").reset_index(),
                on="iso3",
                how="left",
            )
    inten["d_tnlg_M_2124"] = inten.tnlg_M_2024 - inten.tnlg_M_2021
    inten["d_tnlg_M_2324"] = inten.tnlg_M_2024 - inten.tnlg_M_2023
    inten["d_tnlg_F_2124"] = inten.tnlg_F_2024 - inten.tnlg_F_2021
    inten["d_tnlg_F_2324"] = inten.tnlg_F_2024 - inten.tnlg_F_2023
    inten["d_tml_M_2324"] = inten.tml_M_2024 - inten.tml_M_2023
    inten["d_ttm_M_2324"] = inten.ttm_M_2024 - inten.ttm_M_2023
    inten["d_tir_M_2324"] = inten.tir_M_2024 - inten.tir_M_2023
    inten["d_tany_M_2124"] = inten.tany_M_2024 - inten.tany_M_2021
    inten["d_tnlg_J_2324"] = inten.tnlg_J_2024 - inten.tnlg_J_2023
    inten["d_tnlg_C_2324"] = inten.tnlg_C_2024 - inten.tnlg_C_2023
    inten["d_tnlg_N_2324"] = inten.tnlg_N_2024 - inten.tnlg_N_2023
    inten["country"] = inten.iso3.map(ISO2NAME)
    return inten


def load_batis():
    df = pd.read_csv(DATA / "batis_civil_related.csv")
    df = df[df.ADJUSTMENT == "B"].copy()
    df["year"] = df.TIME_PERIOD.astype(int)
    df["value"] = pd.to_numeric(df.OBS_VALUE, errors="coerce")
    df = df.dropna(subset=["value"])
    df = df.drop_duplicates(["REF_AREA", "COUNTERPART_AREA", "TRADE_FLOW", "SERVICE", "year"])
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


def build_panel(trade, inten):
    importers = sorted(set(inten.iso3) & set(trade.importer.unique()))
    p = trade[trade.importer.isin(importers) & trade.year.between(2018, 2024)].copy()
    p = p.merge(inten, left_on="importer", right_on="iso3", how="left")
    p["logv"] = np.log(p.value.clip(lower=0.01))
    p["post"] = (p.year >= 2023).astype(float)
    p["post24"] = (p.year >= 2024).astype(float)
    shocks = [
        "d_tnlg_M_2324", "d_tnlg_M_2124", "d_tnlg_F_2324", "d_tml_M_2324",
        "d_ttm_M_2324", "d_tir_M_2324", "d_tany_M_2124", "d_tnlg_J_2324",
        "d_tnlg_C_2324", "d_tnlg_N_2324", "tnlg_M_2024",
    ]
    for s in shocks:
        p[f"post_x_{s}"] = p.post * p[s]
        p[f"p24_x_{s}"] = p.post24 * p[s]
    return p


def run_spec(results, name, dat, key, extra, note):
    fe = ["importer", "year"]
    if dat.partner.nunique() > 1:
        fe.append("partner")
    out = fit_fe(dat, "logv", extra, fe, "importer")
    if out is None:
        results.append({
            "spec": name, "coef": np.nan, "se": np.nan, "p": np.nan,
            "n": len(dat), "r2": np.nan, "note": note, "display": "—",
        })
        return
    res, used = out
    results.append(row(name, res, key, len(used), note))


def main():
    plt.rcParams.update({
        "figure.dpi": 140, "savefig.dpi": 200, "font.size": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.25,
    })
    all_ = load_types()
    inten = intensity(all_)
    inten.to_csv(TAB / "table_tnlg_intensity.csv", index=False)

    eu = all_[all_.geo == "EU27_2020"]
    eu_tab = eu.pivot_table(index=["nace", "indic"], columns="year", values="value").reset_index()
    eu_tab.to_csv(TAB / "table_tnlg_eu27.csv", index=False)

    batis = load_batis()
    sj3 = make_imports(batis, "SJ3", MODE1)
    si = make_imports(batis, "SI", MODE1)
    se_chn = make_imports(batis, "SE", ["CHN"])
    sj3_chn = make_imports(batis, "SJ3", ["CHN"])
    panel = build_panel(sj3, inten)
    panel.to_csv(DATA / "panel_eu_sj3_tnlg.csv", index=False)
    panel_si = build_panel(si, inten)
    panel_se = build_panel(se_chn, inten)
    panel_sj3c = build_panel(sj3_chn, inten)

    results = []
    run_spec(
        results, "(N1) Post×ΔM TNLG 2023–24 [preferred GenAI shock]",
        panel, "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
        "NLG jump is the ChatGPT window; EU × IND/PHL/VNM",
    )
    run_spec(
        results, "(N2) Post2024×ΔM TNLG 2023–24",
        panel, "p24_x_d_tnlg_M_2324", ["p24_x_d_tnlg_M_2324"],
        "Treat only 2024 as post (BaTIS ends 2024)",
    )
    run_spec(
        results, "(N3) Post×ΔM TNLG 2021–24",
        panel, "post_x_d_tnlg_M_2124", ["post_x_d_tnlg_M_2124"],
        "Comparable window to generic TANY ΔM",
    )
    run_spec(
        results, "(N4) Post× TNLG M 2024 level",
        panel, "post_x_tnlg_M_2024", ["post_x_tnlg_M_2024"],
        "Level not change",
    )
    run_spec(
        results, "(N5) Placebo Post×ΔF TNLG 2023–24",
        panel, "post_x_d_tnlg_F_2324", ["post_x_d_tnlg_F_2324"],
        "Construction enterprises using NLG",
    )
    run_spec(
        results, "(N6) Horse: Post×ΔM TNLG",
        panel, "post_x_d_tnlg_M_2324",
        ["post_x_d_tnlg_M_2324", "post_x_d_tml_M_2324"],
        "Same regression as N7",
    )
    run_spec(
        results, "(N7) Horse: Post×ΔM TML (ML placebo)",
        panel, "post_x_d_tml_M_2324",
        ["post_x_d_tnlg_M_2324", "post_x_d_tml_M_2324"],
        "Machine learning, not generative NLG",
    )
    run_spec(
        results, "(N8) Placebo Post×ΔM TTM 2023–24",
        panel, "post_x_d_ttm_M_2324", ["post_x_d_ttm_M_2324"],
        "Text mining (also jumped; not NLG)",
    )
    run_spec(
        results, "(N9) Placebo Post×ΔM TIR 2023–24",
        panel, "post_x_d_tir_M_2324", ["post_x_d_tir_M_2324"],
        "Image recognition",
    )
    run_spec(
        results, "(N10) Comparison Post×ΔM TANY 2021–24",
        panel, "post_x_d_tany_M_2124", ["post_x_d_tany_M_2124"],
        "Generic any-AI; mixes ML and GenAI",
    )
    run_spec(
        results, "(N11) Placebo SI Post×ΔM TNLG",
        panel_si, "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
        "Computer services from same partners",
    )
    run_spec(
        results, "(N12) Placebo China SE Post×ΔM TNLG",
        panel_se, "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
        "Mode-3 construction from China",
    )
    run_spec(
        results, "(N13) Placebo China SJ3 Post×ΔM TNLG",
        panel_sj3c, "post_x_d_tnlg_M_2324", ["post_x_d_tnlg_M_2324"],
        "SJ3 from China",
    )
    run_spec(
        results, "(N14) Placebo Post×ΔJ TNLG 2023–24",
        panel, "post_x_d_tnlg_J_2324", ["post_x_d_tnlg_J_2324"],
        "ICT sector NLG (NACE J), not M71-containing M",
    )
    run_spec(
        results, "(N15) Placebo Post×ΔC TNLG 2023–24",
        panel, "post_x_d_tnlg_C_2324", ["post_x_d_tnlg_C_2324"],
        "Manufacturing NLG",
    )
    run_spec(
        results, "(N16) Placebo Post×ΔN TNLG 2023–24",
        panel, "post_x_d_tnlg_N_2324", ["post_x_d_tnlg_N_2324"],
        "Administrative/support NLG",
    )
    for partner, lab in [("IND", "India"), ("PHL", "Philippines"), ("VNM", "Viet Nam")]:
        run_spec(
            results, f"(NH) {lab} only Post×ΔM TNLG 2023–24",
            panel[panel.partner == partner], "post_x_d_tnlg_M_2324",
            ["post_x_d_tnlg_M_2324"], f"Partner = {partner}",
        )

    eu8 = ["DEU", "FRA", "NLD", "POL", "ITA", "ESP", "IRL", "ROU"]
    run_spec(
        results, "(N17) EU-8 Post×ΔM TNLG 2023–24",
        panel[panel.importer.isin(eu8)], "post_x_d_tnlg_M_2324",
        ["post_x_d_tnlg_M_2324"], "Same fragile eight-country sample as TANY EU-8",
    )

    # Event study year × ΔTNLG 2023-24
    es = panel.copy()
    year_d = pd.get_dummies(es.year.astype(int), prefix="y", dtype=float)
    inter = []
    for y in range(2018, 2025):
        if y == 2022:
            continue
        col = f"tnlg_y{y}"
        es[col] = year_d[f"y_{y}"] * es.d_tnlg_M_2324
        inter.append(col)
    out = fit_fe(es, "logv", inter, ["importer", "year", "partner"], "importer")
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
    es_df.to_csv(TAB / "table_event_study_tnlg.csv", index=False)

    # Cross-section India
    chg_in = sj3[(sj3.importer.isin(panel.importer.unique())) & (sj3.partner == "IND") & sj3.year.isin([2022, 2024])]
    chg_in = chg_in.pivot_table(index="importer", columns="year", values="value").reset_index()
    chg_in = chg_in.rename(columns={2022: "v22", 2024: "v24"})
    chg_in["dlog"] = np.log(chg_in.v24) - np.log(chg_in.v22)
    chg_in = chg_in.merge(inten, left_on="importer", right_on="iso3")
    chg_in = chg_in.dropna(subset=["dlog", "d_tnlg_M_2324"])
    chg_in.to_csv(TAB / "table_cross_section_india_tnlg.csv", index=False)
    if len(chg_in) >= 8:
        rA = sm.OLS(chg_in.dlog, sm.add_constant(chg_in["d_tnlg_M_2324"])).fit(cov_type="HC1")
        results.append(row(
            "(N18) Cross-section Δlog IN SJ3 22–24 on ΔTNLG 23–24",
            rA, "d_tnlg_M_2324", len(chg_in), "No FE; one obs per importer",
        ))

    # M71 GVA with TNLG shock
    gva = pd.read_csv(DATA / "eurostat_nama_gva_M71_F_M.csv")
    gva["year"] = gva.time.astype(int)
    gva["iso3"] = gva.geo.map(GEO2ISO)
    gva["value"] = pd.to_numeric(gva.value, errors="coerce")
    m71 = gva[(gva.nace == "M71") & gva.iso3.notna() & gva.year.between(2018, 2023)].copy()
    m71 = m71.merge(inten, on="iso3", how="left")
    m71["logv"] = np.log(m71.value.clip(lower=0.01))
    m71["post"] = (m71.year >= 2023).astype(float)
    m71["post_x_d_tnlg_M_2324"] = m71.post * m71.d_tnlg_M_2324
    m71["importer"] = m71.iso3
    m71["partner"] = "DOM"
    out = fit_fe(m71, "logv", ["post_x_d_tnlg_M_2324"], ["importer", "year"], "importer")
    if out:
        res, used = out
        results.append(row(
            "(N19) log M71 GVA Post×ΔM TNLG 2023–24",
            res, "post_x_d_tnlg_M_2324", len(used),
            "Domestic architectural & engineering GVA; GVA only to 2023",
        ))

    sj12 = pd.read_csv(DATA / "batis_SJ1_SJ2.csv")
    sj12 = sj12[sj12.ADJUSTMENT == "B"].copy()
    sj12["year"] = sj12.TIME_PERIOD.astype(int)
    sj12["value"] = pd.to_numeric(sj12.OBS_VALUE, errors="coerce")
    keys = ["importer", "partner", "year"]
    base = panel[keys + ["d_tnlg_M_2324", "post_x_d_tnlg_M_2324"]].drop_duplicates(keys)
    for svc, lab in [("SJ2", "SJ2 consulting"), ("SJ1", "SJ1 R&D")]:
        m = sj12[(sj12.SERVICE == svc) & (sj12.TRADE_FLOW == "M") & sj12.COUNTERPART_AREA.isin(MODE1)]
        m = m.rename(columns={"REF_AREA": "importer", "COUNTERPART_AREA": "partner"})
        p = base.merge(m[keys + ["value"]].drop_duplicates(keys), on=keys, how="inner")
        p["logv"] = np.log(p.value.clip(lower=0.01))
        run_spec(results, f"(N20) {lab} Post×ΔM TNLG", p, "post_x_d_tnlg_M_2324",
                 ["post_x_d_tnlg_M_2324"], "Same importers/partners as SJ3")

    t = pd.DataFrame(results)
    t.to_csv(TAB / "table_nlg_identification.csv", index=False)
    pretty = t[["spec", "display", "n", "note"]].copy()
    pretty.columns = ["Specification", "Coefficient (s.e.)", "N", "Note"]
    pretty.to_csv(TAB / "article_T13_nlg_shock.csv", index=False)

    # Figures
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    years = [2021, 2023, 2024, 2025]
    def eu_val(nace, indic, y):
        s = eu[(eu.nace == nace) & (eu.indic == indic) & (eu.year == y)]
        return float(s.value.iloc[0]) if len(s) else np.nan
    ax.plot(years, [eu_val("M", "E_AI_TNLG", y) for y in years], marker="o", label="M NLG (generative text)")
    ax.plot(years, [eu_val("M", "E_AI_TML", y) for y in years], marker="^", label="M machine learning")
    ax.plot(years, [eu_val("M", "E_AI_TTM", y) for y in years], marker="D", label="M text mining")
    ax.plot(years, [eu_val("F", "E_AI_TNLG", y) for y in years], marker="s", label="F NLG (construction)")
    ax.axvline(2022.9, color="0.6", ls="--", lw=0.8)
    ax.set_ylabel("Enterprises using technology, % (10+)")
    ax.set_xlabel("Year")
    ax.set_title("Eurostat AI types, EU-27: generative NLG vs older AI vs construction")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "figure12_tnlg_vs_tml.png")
    plt.close()

    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    c = inten.dropna(subset=["tnlg_M_2024"]).sort_values("tnlg_M_2024")
    ax.barh(c.country, c.tnlg_M_2024, color="#3b6d99", label="M NLG 2024")
    ax.barh(c.country, c.tnlg_F_2024, color="#c47a3a", alpha=0.75, label="F NLG 2024")
    ax.set_xlabel("Enterprises using NLG AI, 2024 (%)")
    ax.set_title("Professional vs construction generative-text use, 2024")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "figure13_tnlg_2024_MF.png")
    plt.close()

    if not es_df.empty:
        fig, ax = plt.subplots(figsize=(8.2, 4.6))
        ax.axhline(0, color="0.4", lw=0.8)
        ax.axvline(2022.5, color="0.6", ls="--", lw=0.8, label="ChatGPT public release")
        ax.errorbar(es_df.year, es_df.coef, yerr=1.96 * es_df.se.replace({0: np.nan}), fmt="o-", capsize=3)
        ax.set_xlabel("Year (2022 = reference)")
        ax.set_ylabel("Year × importer ΔM TNLG 2023–24")
        ax.set_title("Event study with generative-NLG shock, Mode-1 SJ3")
        ax.legend(frameon=False)
        fig.tight_layout()
        fig.savefig(FIG / "figure14_event_study_tnlg.png")
        plt.close()

    fig, ax = plt.subplots(figsize=(6.8, 4.8))
    ax.scatter(chg_in.d_tnlg_M_2324, chg_in.dlog)
    for _, r in chg_in.iterrows():
        ax.annotate(r.importer, (r.d_tnlg_M_2324, r.dlog), textcoords="offset points", xytext=(4, 4), fontsize=8)
    ax.set_xlabel("NACE M NLG, 2024 minus 2023 (pp)")
    ax.set_ylabel("Δ log SJ3 imports from India, 2022–24")
    ax.set_title("GenAI NLG acceleration and India Mode-1 SJ3 growth")
    fig.tight_layout()
    fig.savefig(FIG / "figure15_cross_section_tnlg.png")
    plt.close()

    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    years = [2021, 2023, 2024, 2025]
    for nace, lab in [("M", "M professional"), ("J", "J ICT"), ("C", "C manufacturing"), ("N", "N admin"), ("F", "F construction")]:
        vals = []
        for y in years:
            s = all_[(all_.geo == "EU27_2020") & (all_.nace == nace) & (all_.indic == "E_AI_TNLG") & (all_.year == y)]
            vals.append(float(s.value.iloc[0]) if len(s) else np.nan)
        ax.plot(years, vals, marker="o", label=lab)
    ax.set_ylabel("NLG use, % of enterprises (10+)")
    ax.set_title("Eurostat NLG by NACE: ICT leads; construction lags; M is the civil-professional proxy")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "figure16_tnlg_by_nace.png")
    plt.close()

    nlg_json = {
        "preferred_shock": "Eurostat E_AI_TNLG NACE M, 2024 minus 2023",
        "eu27_M_TNLG": {str(y): eu_val("M", "E_AI_TNLG", y) for y in years},
        "eu27_F_TNLG": {str(y): eu_val("F", "E_AI_TNLG", y) for y in years},
        "identification": results,
        "cannot_identify": "APS 2121 causing partner GDP or ISCO 2142",
        "failed_downloads": ["OWID ChatGPT user CSV 404", "IMF AIPI datamapper empty JSON", "OECD ICT_BUS AI 404", "NACE K AI unpublished", "M71 AI unpublished"],
    }
    (ROOT / "results_nlg.json").write_text(json.dumps(nlg_json, indent=2, default=str))
    print(t[["spec", "display", "n"]].to_string(index=False))
    print("EU27 M TNLG", {y: eu_val("M", "E_AI_TNLG", y) for y in years})


if __name__ == "__main__":
    main()
