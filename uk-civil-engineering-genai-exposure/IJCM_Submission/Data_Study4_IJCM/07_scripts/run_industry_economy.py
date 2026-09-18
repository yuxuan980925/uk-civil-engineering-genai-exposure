#!/usr/bin/env python3
"""Civil-engineering *industry* economy under a GenAI (TNLG) shock.

Outcomes: Eurostat SBS M71 turnover, employment, wages, VA, GOS (2021–24);
nama compensation/output; construction F placebos. Shock: ΔM TNLG 2023–24.
Does not identify APS 2121 → partner GDP.
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
    "PT": "PRT", "CZ": "CZE", "HU": "HUN", "FI": "FIN", "EL": "GRC", "UK": "GBR",
}
ISO2NAME = {
    "DEU": "Germany", "FRA": "France", "NLD": "Netherlands", "POL": "Poland",
    "ROU": "Romania", "ITA": "Italy", "ESP": "Spain", "IRL": "Ireland",
    "BEL": "Belgium", "AUT": "Austria", "SWE": "Sweden", "DNK": "Denmark",
    "PRT": "Portugal", "CZE": "Czechia", "HUN": "Hungary", "FIN": "Finland",
    "GRC": "Greece", "GBR": "United Kingdom",
}


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
    if len(d) < 16:
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
        return {"spec": name, "coef": np.nan, "se": np.nan, "p": np.nan, "n": n,
                "note": note, "display": "—"}
    return {
        "spec": name,
        "coef": float(res.params[key]),
        "se": float(res.bse[key]),
        "p": float(res.pvalues[key]),
        "n": n,
        "note": note,
        "display": fmt(res.params[key], res.bse[key], res.pvalues[key]),
    }


def growth(sub, y0, y1):
    a, b = sub[sub.year == y0], sub[sub.year == y1]
    if a.empty or b.empty:
        return np.nan
    v0, v1 = float(a.value.iloc[0]), float(b.value.iloc[0])
    if v0 <= 0:
        return np.nan
    return 100 * (v1 / v0 - 1)


def main():
    plt.rcParams.update({
        "figure.dpi": 140, "savefig.dpi": 200, "font.size": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.25,
    })
    inten = pd.read_csv(TAB / "table_tnlg_intensity.csv")
    sbs = pd.read_csv(DATA / "eurostat_sbs_M71_F_M.csv")
    sbs["iso3"] = sbs.geo.map(GEO2ISO)
    sbs["value"] = pd.to_numeric(sbs.value, errors="coerce")
    sbs = sbs[sbs.iso3.notna()].copy()

    # Prefer sc_ovw for turnover; ovw_act for emp/wages/VA (same EMP when both exist)
    def pick(nace, indic, dataset=None):
        d = sbs[(sbs.nace == nace) & (sbs.indic == indic)]
        if dataset:
            d = d[d.dataset == dataset]
        elif indic == "NETTUR_MEUR":
            d = d[d.dataset == "sbs_sc_ovw"]
        else:
            d = d[d.dataset == "sbs_ovw_act"]
        return d

    grow_rows = []
    for iso in sorted(sbs.iso3.unique()):
        rec = {"iso3": iso, "country": ISO2NAME.get(iso, iso)}
        for nace, lab in [("M71", "M71"), ("F", "F"), ("M", "M")]:
            for indic, name, ds in [
                ("NETTUR_MEUR", "turn", "sbs_sc_ovw"),
                ("EMP_NR", "emp", "sbs_ovw_act"),
                ("WAGE_MEUR", "wage", "sbs_ovw_act"),
                ("AV_MEUR", "va", "sbs_ovw_act"),
                ("GOS_MEUR", "gos", "sbs_ovw_act"),
            ]:
                sub = sbs[(sbs.iso3 == iso) & (sbs.nace == nace) & (sbs.indic == indic) & (sbs.dataset == ds)]
                rec[f"pct_{lab}_{name}_21_24"] = growth(sub, 2021, 2024)
                rec[f"pct_{lab}_{name}_23_24"] = growth(sub, 2023, 2024)
        grow_rows.append(rec)
    grow = pd.DataFrame(grow_rows).merge(inten[["iso3", "d_tnlg_M_2324", "d_tnlg_F_2324", "tnlg_M_2024"]], on="iso3", how="left")
    grow.to_csv(TAB / "table_sbs_m71_growth.csv", index=False)

    results = []

    def panel_outcome(nace, indic, dataset, yname):
        d = sbs[(sbs.nace == nace) & (sbs.indic == indic) & (sbs.dataset == dataset)].copy()
        d = d.merge(inten, on="iso3", how="left")
        d["logv"] = np.log(d.value.clip(lower=0.01))
        d["post24"] = (d.year >= 2024).astype(float)
        d["post23"] = (d.year >= 2023).astype(float)
        d["p24_tnlg"] = d.post24 * d.d_tnlg_M_2324
        d["p23_tnlg"] = d.post23 * d.d_tnlg_M_2324
        d["importer"] = d.iso3
        return d

    specs = [
        ("(I1) log M71 turnover Post2024×ΔTNLG", "M71", "NETTUR_MEUR", "sbs_sc_ovw", "p24_tnlg"),
        ("(I2) log M71 employment Post2024×ΔTNLG", "M71", "EMP_NR", "sbs_ovw_act", "p24_tnlg"),
        ("(I3) log M71 wages Post2024×ΔTNLG", "M71", "WAGE_MEUR", "sbs_ovw_act", "p24_tnlg"),
        ("(I4) log M71 value added Post2024×ΔTNLG", "M71", "AV_MEUR", "sbs_ovw_act", "p24_tnlg"),
        ("(I5) log M71 GOS Post2024×ΔTNLG", "M71", "GOS_MEUR", "sbs_ovw_act", "p24_tnlg"),
        ("(I6) log F turnover Post2024×ΔTNLG placebo", "F", "NETTUR_MEUR", "sbs_sc_ovw", "p24_tnlg"),
        ("(I7) log F employment Post2024×ΔTNLG placebo", "F", "EMP_NR", "sbs_ovw_act", "p24_tnlg"),
        ("(I8) log M turnover Post2024×ΔTNLG placebo", "M", "NETTUR_MEUR", "sbs_sc_ovw", "p24_tnlg"),
        ("(I9) log M71 turnover Post2023×ΔTNLG", "M71", "NETTUR_MEUR", "sbs_sc_ovw", "p23_tnlg"),
    ]
    for name, nace, indic, ds, key in specs:
        dat = panel_outcome(nace, indic, ds, name)
        out = fit_fe(dat, "logv", [key], ["importer", "year"], "importer")
        if out:
            res, used = out
            results.append(row(name, res, key, len(used), f"SBS {ds} {nace} {indic}; country+year FE"))

    # Cross-section 2023-24 growth on ΔTNLG
    g = grow.dropna(subset=["pct_M71_turn_23_24", "d_tnlg_M_2324"])
    if len(g) >= 8:
        y = g.pct_M71_turn_23_24 / 100.0
        rA = sm.OLS(y, sm.add_constant(g["d_tnlg_M_2324"])).fit(cov_type="HC1")
        results.append(row(
            "(I10) Δlog≈ M71 turnover 2023–24 on ΔTNLG",
            rA, "d_tnlg_M_2324", len(g), "Cross-section; LHS is percent/100",
        ))
        g2 = grow.dropna(subset=["pct_M71_emp_23_24", "d_tnlg_M_2324"])
        y2 = g2.pct_M71_emp_23_24 / 100.0
        rB = sm.OLS(y2, sm.add_constant(g2["d_tnlg_M_2324"])).fit(cov_type="HC1")
        results.append(row(
            "(I11) M71 employment % 2023–24 on ΔTNLG",
            rB, "d_tnlg_M_2324", len(g2), "Cross-section; LHS percent/100",
        ))

    # nama D1 compensation, P1 output
    nama = pd.read_csv(DATA / "eurostat_nama_D1_P1_M71_F_M.csv")
    nama["iso3"] = nama.geo.map(GEO2ISO)
    nama["value"] = pd.to_numeric(nama.value, errors="coerce")
    nama = nama[nama.iso3.notna() & nama.year.between(2018, 2023)]
    for item, lab, nace in [
        ("D1", "compensation", "M71"),
        ("P1", "output", "M71"),
        ("D1", "compensation", "F"),
        ("P1", "output", "F"),
    ]:
        d = nama[(nama.na_item == item) & (nama.nace == nace)].copy()
        d = d.merge(inten, on="iso3", how="left")
        d["logv"] = np.log(d.value.clip(lower=0.01))
        d["post"] = (d.year >= 2023).astype(float)
        d["p_tnlg"] = d.post * d.d_tnlg_M_2324
        d["importer"] = d.iso3
        out = fit_fe(d, "logv", ["p_tnlg"], ["importer", "year"], "importer")
        if out:
            res, used = out
            results.append(row(
                f"(I12) log {nace} {lab} Post×ΔTNLG",
                res, "p_tnlg", len(used),
                "nama_10_a64 current EUR; series ends 2023 so misses 2024 NLG year",
            ))

    # Partner-weighted: India SJ3 vs importer TNLG already in nlg script.
    # Destination-weighted China SE: high vs low TNLG importers (descriptive split).
    batis = pd.read_csv(DATA / "batis_civil_related.csv")
    batis = batis[batis.ADJUSTMENT == "B"].copy()
    batis["year"] = batis.TIME_PERIOD.astype(int)
    batis["value"] = pd.to_numeric(batis.OBS_VALUE, errors="coerce")
    se = batis[
        (batis.TRADE_FLOW == "M")
        & (batis.SERVICE == "SE")
        & (batis.COUNTERPART_AREA == "CHN")
        & batis.REF_AREA.isin(inten.iso3)
    ].copy()
    se = se.rename(columns={"REF_AREA": "importer"})
    med = inten.d_tnlg_M_2324.median()
    inten["high_tnlg"] = (inten.d_tnlg_M_2324 >= med).astype(int)
    se = se.merge(inten[["iso3", "d_tnlg_M_2324", "high_tnlg"]], left_on="importer", right_on="iso3")
    split = se[se.year.isin([2019, 2024])].pivot_table(
        index=["high_tnlg"], columns="year", values="value", aggfunc="sum"
    )
    split.to_csv(TAB / "table_china_se_by_tnlg_split.csv")

    t = pd.DataFrame(results)
    t.to_csv(TAB / "table_industry_economy.csv", index=False)
    pretty = t[["spec", "display", "n", "note"]].copy()
    pretty.columns = ["Specification", "Coefficient (s.e.)", "N", "Note"]
    pretty.to_csv(TAB / "article_T16_industry_economy.csv", index=False)

    # BLS NAICS 54 annual average
    bls_path = DATA / "bls_engineering_ces.csv"
    if bls_path.exists():
        bls = pd.read_csv(bls_path)
        bls["value"] = pd.to_numeric(bls.value, errors="coerce")
        ann = bls.groupby("year", as_index=False)["value"].mean()
        ann.to_csv(TAB / "table_bls_naics54_annual.csv", index=False)
    else:
        ann = pd.DataFrame()

    # Figures
    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    gg = grow.dropna(subset=["pct_M71_turn_21_24", "pct_F_turn_21_24"]).sort_values("pct_M71_turn_21_24")
    y = np.arange(len(gg))
    ax.barh(y + 0.18, gg.pct_M71_turn_21_24, height=0.35, label="M71 architectural & engineering turnover")
    ax.barh(y - 0.18, gg.pct_F_turn_21_24, height=0.35, label="F construction turnover")
    ax.set_yticks(y, gg.country)
    ax.set_xlabel("Percent change, 2021–2024 (current EUR)")
    ax.set_title("Enterprise statistics: engineering-consultancy vs construction turnover")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "figure17_sbs_turnover_m71_vs_F.png")
    plt.close()

    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    gg = grow.dropna(subset=["pct_M71_emp_21_24", "pct_F_emp_21_24"]).sort_values("pct_M71_emp_21_24")
    y = np.arange(len(gg))
    ax.barh(y + 0.18, gg.pct_M71_emp_21_24, height=0.35, label="M71 persons employed")
    ax.barh(y - 0.18, gg.pct_F_emp_21_24, height=0.35, label="F construction persons employed")
    ax.set_yticks(y, gg.country)
    ax.set_xlabel("Percent change, 2021–2024")
    ax.set_title("Enterprise statistics: engineering vs construction employment")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "figure18_sbs_emp_m71_vs_F.png")
    plt.close()

    fig, ax = plt.subplots(figsize=(6.8, 4.8))
    gsc = grow.dropna(subset=["pct_M71_turn_23_24", "d_tnlg_M_2324"])
    ax.scatter(gsc.d_tnlg_M_2324, gsc.pct_M71_turn_23_24)
    for _, r in gsc.iterrows():
        ax.annotate(r.iso3, (r.d_tnlg_M_2324, r.pct_M71_turn_23_24), textcoords="offset points", xytext=(4, 4), fontsize=8)
    ax.set_xlabel("NACE M NLG, 2024 minus 2023 (pp)")
    ax.set_ylabel("M71 net turnover change, 2023–24 (%)")
    ax.set_title("GenAI NLG jump and engineering-industry turnover")
    fig.tight_layout()
    fig.savefig(FIG / "figure19_tnlg_vs_m71_turnover.png")
    plt.close()

    # EU-27 / country M71 turnover time series selected
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    tur = pick("M71", "NETTUR_MEUR")
    for iso in ["DEU", "FRA", "ITA", "ESP", "NLD", "POL"]:
        s = tur[tur.iso3 == iso].sort_values("year")
        if s.empty:
            continue
        ax.plot(s.year, s.value / 1000, marker="o", label=ISO2NAME[iso])
    ax.set_ylabel("Net turnover (EUR billion)")
    ax.set_title("NACE M71 net turnover, selected EU members")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "figure20_m71_turnover_levels.png")
    plt.close()

    if not ann.empty:
        fig, ax = plt.subplots(figsize=(8.0, 4.4))
        ax.plot(ann.year, ann.value, marker="o")
        ax.set_ylabel("Thousands of employees (annual mean of months)")
        ax.set_title("US CES: Professional and technical services (NAICS 54), not 54133")
        fig.tight_layout()
        fig.savefig(FIG / "figure21_bls_naics54.png")
        plt.close()

    outj = {
        "identified_object": "Importer/domestic NACE M71 SBS economy associated with TNLG shock; F placebo",
        "cannot_identify": "APS 2121 causing partner GDP or ISCO 2142",
        "sbs_years": "2021-2024",
        "ilo_m71": "not published (404)",
        "bls_54133": "public API returned NAICS 54 only, not 54133",
        "identification": results,
    }
    (ROOT / "results_industry.json").write_text(json.dumps(outj, indent=2, default=str))
    print(t[["spec", "display", "n"]].to_string(index=False))
    print(grow[["country", "pct_M71_turn_21_24", "pct_F_turn_21_24", "pct_M71_emp_21_24"]].round(1).to_string(index=False))


if __name__ == "__main__":
    main()
