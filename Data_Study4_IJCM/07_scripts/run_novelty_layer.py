#!/usr/bin/env python3
"""Civil-specific novelty layer: NACE M71 GVA/employment, BaTIS SJ2 placebo, Eloundou scores."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
DATA, TAB, FIG = ROOT / "data", ROOT / "tables", ROOT / "figures"
FIG.mkdir(exist_ok=True)
TAB.mkdir(exist_ok=True)

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
    return f"{b:.3f}{star(p)} ({se:.3f})"


def fit_fe(df, y, x, fe, cluster):
    df = df.loc[:, ~df.columns.duplicated()].copy()
    use = list(dict.fromkeys([y] + x + fe + [cluster]))
    d = df[use].dropna().reset_index(drop=True)
    if len(d) < 20:
        return None
    work = d[[y] + x].astype(float)
    for _ in range(8):
        for g in fe:
            work = work - work.groupby(d[g].to_numpy()).transform("mean")
    res = sm.OLS(work[y], work[x]).fit(
        cov_type="cluster", cov_kwds={"groups": d[cluster], "use_correction": True}
    )
    return res, d


def main():
    plt.rcParams.update({"figure.dpi": 140, "savefig.dpi": 200, "axes.spines.top": False, "axes.spines.right": False})

    # Eloundou civil slice
    el = pd.read_csv(DATA / "eloundou_occ_level.csv")
    codes = ["17-2051.00", "17-2051.01", "17-2051.02", "17-3011.00", "17-3022.00", "17-1011.00"]
    elc = el[el["O*NET-SOC Code"].isin(codes)].copy()
    elc.to_csv(TAB / "table_eloundou_civil.csv", index=False)

    # M71 GVA / employment
    gva = pd.read_csv(DATA / "eurostat_nama_gva_M71_F_M.csv")
    emp = pd.read_csv(DATA / "eurostat_nama_emp_M71_F_M.csv")
    for d in (gva, emp):
        d["year"] = d.time.astype(int)
        d["iso3"] = d.geo.map(GEO2ISO)
        d["value"] = pd.to_numeric(d.value, errors="coerce")

    def growth_table(df, y0, y1, label):
        rows = []
        sub = df[df.iso3.notna() & df.nace.isin(["M71", "F", "M"])]
        for (iso, nace), s in sub.groupby(["iso3", "nace"]):
            a, b = s[s.year == y0], s[s.year == y1]
            if a.empty or b.empty:
                continue
            v0, v1 = float(a.value.iloc[0]), float(b.value.iloc[0])
            if v0 <= 0:
                continue
            rows.append({"iso3": iso, "country": ISO2NAME.get(iso, iso), "nace": nace, "y0": v0, "y1": v1, "pct": 100 * (v1 / v0 - 1)})
        t = pd.DataFrame(rows)
        wide = t.pivot_table(index=["country", "iso3"], columns="nace", values="pct")
        wide = wide.reset_index()
        wide.to_csv(TAB / f"table_{label}_pct_{y0}_{y1}.csv", index=False)
        return wide

    gva_g = growth_table(gva, 2019, 2023, "m71_gva")
    emp_g = growth_table(emp, 2019, 2023, "m71_emp")

    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    gg = gva_g.dropna(subset=["M71", "F"]).sort_values("M71")
    y = np.arange(len(gg))
    ax.barh(y + 0.18, gg.M71, height=0.35, label="NACE M71 architectural & engineering GVA")
    ax.barh(y - 0.18, gg.F, height=0.35, label="NACE F construction GVA")
    ax.set_yticks(y, gg.country)
    ax.set_xlabel("Percent change, 2019–2023 (current EUR)")
    ax.set_title("Eurostat national accounts: engineering activities vs construction")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "figure9_m71_vs_F_gva.png")
    plt.close()

    # Intensity merge
    inten = pd.read_csv(TAB / "table_ai_intensity.csv")

    # Domestic M71 TWFE: 2018-2023, Post 2023 x dM
    m71 = gva[(gva.nace == "M71") & gva.iso3.notna() & gva.year.between(2018, 2023)].copy()
    m71 = m71.merge(inten, on="iso3", how="left")
    m71["logv"] = np.log(m71.value.clip(lower=0.01))
    m71["post"] = (m71.year >= 2023).astype(float)
    m71["post_x_dM"] = m71.post * m71.dM
    m71["importer"] = m71.iso3
    f = gva[(gva.nace == "F") & gva.iso3.notna() & gva.year.between(2018, 2023)].copy()
    f = f.merge(inten, on="iso3", how="left")
    f["logv"] = np.log(f.value.clip(lower=0.01))
    f["post"] = (f.year >= 2023).astype(float)
    f["post_x_dM"] = f.post * f.dM
    f["importer"] = f.iso3

    results = []
    for name, dat, note in [
        ("(M71) log GVA Post × ΔM", m71, "NACE M71 GVA, country and year FE"),
        ("(F) log GVA Post × ΔM placebo", f, "Construction GVA"),
    ]:
        out = fit_fe(dat, "logv", ["post_x_dM"], ["importer", "year"], "importer")
        if out is None:
            continue
        res, used = out
        results.append({
            "spec": name, "coef": float(res.params["post_x_dM"]), "se": float(res.bse["post_x_dM"]),
            "p": float(res.pvalues["post_x_dM"]), "n": len(used),
            "display": fmt(res.params["post_x_dM"], res.bse["post_x_dM"], res.pvalues["post_x_dM"]),
            "note": note,
        })

    # Time-varying M AI on M71 in 2021 and 2023
    ai = pd.read_csv(DATA / "eurostat_ai_raw.csv")
    ai = ai[ai.nace == "M"].copy()
    ai["iso3"] = ai.geo.map(GEO2ISO)
    ai["year"] = ai.year.astype(int)
    tv = m71.merge(ai[["iso3", "year", "ai_pct"]], on=["iso3", "year"], how="left")
    tv = tv[tv.year.isin([2021, 2023])]
    tv = tv.rename(columns={"ai_pct": "ai_M"})
    out = fit_fe(tv, "logv", ["ai_M"], ["importer", "year"], "importer")
    if out:
        res, used = out
        results.append({
            "spec": "(M71) time-varying M-AI 2021/23",
            "coef": float(res.params["ai_M"]), "se": float(res.bse["ai_M"]),
            "p": float(res.pvalues["ai_M"]), "n": len(used),
            "display": fmt(res.params["ai_M"], res.bse["ai_M"], res.pvalues["ai_M"]),
            "note": "Two Eurostat AI years overlapping M71 GVA",
        })

    # SJ2 placebo on existing Mode-1 panel structure
    sj = pd.read_csv(DATA / "batis_SJ1_SJ2.csv")
    sj = sj[sj.ADJUSTMENT == "B"].copy()
    sj["year"] = sj.TIME_PERIOD.astype(int)
    sj["value"] = pd.to_numeric(sj.OBS_VALUE, errors="coerce")
    panel = pd.read_csv(DATA / "panel_eu_sj3_mode1.csv")
    panel = panel.loc[:, ~panel.columns.duplicated()]
    keys = ["importer", "partner", "year"]
    for svc, lab in [("SJ2", "SJ2 consulting placebo"), ("SJ1", "SJ1 R&D placebo")]:
        m = sj[(sj.SERVICE == svc) & (sj.TRADE_FLOW == "M") & sj.COUNTERPART_AREA.isin(["IND", "PHL", "VNM"])]
        m = m.rename(columns={"REF_AREA": "importer", "COUNTERPART_AREA": "partner"})
        m = m[keys + ["value"]].drop_duplicates(keys)
        p = panel[keys + ["dM", "post_x_dM"]].drop_duplicates(keys).merge(m, on=keys, how="inner")
        p["logv"] = np.log(p.value.clip(lower=0.01))
        out = fit_fe(p, "logv", ["post_x_dM"], ["importer", "year", "partner"], "importer")
        if out:
            res, used = out
            results.append({
                "spec": f"(trade) {lab} Post × ΔM",
                "coef": float(res.params["post_x_dM"]), "se": float(res.bse["post_x_dM"]),
                "p": float(res.pvalues["post_x_dM"]), "n": len(used),
                "display": fmt(res.params["post_x_dM"], res.bse["post_x_dM"], res.pvalues["post_x_dM"]),
                "note": "Same importers/partners/years as SJ3 panel",
            })

    pd.DataFrame(results).to_csv(TAB / "table_novelty_m71_sj2.csv", index=False)
    print(pd.DataFrame(results)[["spec", "display", "n"]].to_string(index=False))
    print("M71 GVA growth countries", len(gva_g))
    print(gva_g.round(1).to_string(index=False))


if __name__ == "__main__":
    main()
