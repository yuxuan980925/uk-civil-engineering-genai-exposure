#!/usr/bin/env python3
"""Study 4: GenAI, engineering-adjacent services, and cross-border civil-industry adjustment.

Identified object: importer NACE M AI adoption associated with SJ3 imports.
Not identified: APS 2121 in country A causing employment or GDP in country B.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TAB = ROOT / "tables"
FIG = ROOT / "figures"
for p in (TAB, FIG):
    p.mkdir(parents=True, exist_ok=True)

GEO2ISO = {
    "DE": "DEU",
    "FR": "FRA",
    "NL": "NLD",
    "PL": "POL",
    "RO": "ROU",
    "IT": "ITA",
    "ES": "ESP",
    "IE": "IRL",
    "BE": "BEL",
    "AT": "AUT",
    "SE": "SWE",
    "DK": "DNK",
    "PT": "PRT",
    "CZ": "CZE",
    "HU": "HUN",
    "FI": "FIN",
    "EL": "GRC",
}
ISO2NAME = {
    "DEU": "Germany",
    "FRA": "France",
    "NLD": "Netherlands",
    "POL": "Poland",
    "ROU": "Romania",
    "ITA": "Italy",
    "ESP": "Spain",
    "IRL": "Ireland",
    "BEL": "Belgium",
    "AUT": "Austria",
    "SWE": "Sweden",
    "DNK": "Denmark",
    "PRT": "Portugal",
    "CZE": "Czechia",
    "HUN": "Hungary",
    "FIN": "Finland",
    "GRC": "Greece",
    "GBR": "United Kingdom",
    "IND": "India",
    "CHN": "China",
    "USA": "United States",
    "PHL": "Philippines",
    "VNM": "Viet Nam",
    "ARE": "United Arab Emirates",
    "SGP": "Singapore",
    "AUS": "Australia",
    "JPN": "Japan",
}
MODE1 = ["IND", "PHL", "VNM"]
SOC_KEEP = {
    "2121": "Civil engineers",
    "3114": "Building and civil engineering technicians",
    "3120": "CAD, drawing and architectural technicians",
    "2453": "Quantity surveyors",
    "2455": "Construction project managers",
}


def star(p: float) -> str:
    if pd.isna(p):
        return ""
    if p < 0.01:
        return "***"
    if p < 0.05:
        return "**"
    if p < 0.10:
        return "*"
    return ""


def fmt(b, se, p) -> str:
    if pd.isna(b):
        return "—"
    return f"{b:.3f}{star(p)} ({se:.3f})"


def fit_fe(df, y, x, fe, cluster=None):
    """OLS with iterative within transformation for importer/year/partner FE."""
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
    yv = work[y]
    X = work[x]
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


def row(name, res, key, n, note):
    if key not in res.params:
        return {
            "spec": name,
            "coef": np.nan,
            "se": np.nan,
            "p": np.nan,
            "n": n,
            "r2": float(res.rsquared),
            "clusters": np.nan,
            "note": note,
            "display": "—",
        }
    return {
        "spec": name,
        "coef": float(res.params[key]),
        "se": float(res.bse[key]),
        "p": float(res.pvalues[key]),
        "n": n,
        "r2": float(res.rsquared),
        "clusters": int(getattr(res, "n_groups", np.nan)) if hasattr(res, "n_groups") else np.nan,
        "note": note,
        "display": fmt(res.params[key], res.bse[key], res.pvalues[key]),
    }


def load_eurostat():
    eu = pd.read_csv(DATA / "eurostat_ai_raw.csv")
    eu = eu[eu.geo != "EU27_2020"].copy()
    eu["iso3"] = eu.geo.map(GEO2ISO)
    eu = eu.dropna(subset=["iso3"])
    wide = eu.pivot_table(index=["iso3", "year"], columns="nace", values="ai_pct").reset_index()
    wide = wide.rename(columns={"F": "ai_F", "M": "ai_M"})
    inten = wide.loc[wide.year == 2024, ["iso3", "ai_M", "ai_F"]].rename(
        columns={"ai_M": "ai_M_2024", "ai_F": "ai_F_2024"}
    )
    a21 = wide.loc[wide.year == 2021, ["iso3", "ai_M", "ai_F"]].rename(
        columns={"ai_M": "ai_M_2021", "ai_F": "ai_F_2021"}
    )
    inten = inten.merge(a21, on="iso3", how="left")
    inten["dM"] = inten.ai_M_2024 - inten.ai_M_2021
    inten["dF"] = inten.ai_F_2024 - inten.ai_F_2021
    inten["gap24"] = inten.ai_M_2024 - inten.ai_F_2024
    eu27 = pd.read_csv(DATA / "eurostat_ai_raw.csv")
    eu27 = eu27[eu27.geo == "EU27_2020"]
    return wide, inten, eu27


def load_batis():
    df = pd.read_csv(DATA / "batis_civil_related.csv")
    df = df[df.ADJUSTMENT == "B"].copy()
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


def build_panel(trade, inten, tv, importers):
    p = trade[trade.importer.isin(importers) & trade.year.between(2018, 2024)].copy()
    p = p.merge(inten, left_on="importer", right_on="iso3", how="left")
    p = p.merge(tv.rename(columns={"iso3": "importer"}), on=["importer", "year"], how="left")
    p["logv"] = np.log(p.value.clip(lower=0.01))
    p["ihs"] = np.arcsinh(p.value)
    p["post"] = (p.year >= 2023).astype(float)
    p["post20"] = (p.year >= 2020).astype(float)
    p["post_x_dM"] = p.post * p.dM
    p["post_x_dF"] = p.post * p.dF
    p["post_x_M24"] = p.post * p.ai_M_2024
    p["post_x_F24"] = p.post * p.ai_F_2024
    p["post_x_gap"] = p.post * p.gap24
    p["fake_x_dM"] = p.post20 * p.dM
    return p


def fe_list(dat):
    fe = ["importer", "year"]
    if "partner" in dat.columns and dat.partner.nunique() > 1:
        fe.append("partner")
    return fe


def run_spec(results, name, dat, key, extra, note, cluster="importer"):
    out = fit_fe(dat, "logv", extra, fe_list(dat), cluster)
    if out is None:
        results.append(
            {
                "spec": name,
                "coef": np.nan,
                "se": np.nan,
                "p": np.nan,
                "n": len(dat),
                "r2": np.nan,
                "clusters": np.nan,
                "note": note,
                "display": "—",
            }
        )
        return None
    res, used = out
    results.append(row(name, res, key, len(used), note))
    return res


def main():
    plt.rcParams.update(
        {
            "figure.dpi": 140,
            "savefig.dpi": 200,
            "font.size": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.25,
        }
    )
    wide, inten, eu27 = load_eurostat()
    batis = load_batis()
    tv = wide[["iso3", "year", "ai_M", "ai_F"]]
    importers = sorted(set(inten.iso3) & set(batis.REF_AREA.unique()))
    sj3 = make_imports(batis, "SJ3", MODE1)
    si = make_imports(batis, "SI", MODE1)
    se_chn = make_imports(batis, "SE", ["CHN"])
    sj3_chn = make_imports(batis, "SJ3", ["CHN"])
    se_m1 = make_imports(batis, "SE", MODE1)
    panel = build_panel(sj3, inten, tv, importers)
    panel_si = build_panel(si, inten, tv, importers)
    panel_se_chn = build_panel(se_chn, inten, tv, importers)
    panel_sj3_chn = build_panel(sj3_chn, inten, tv, importers)
    panel_se_m1 = build_panel(se_m1, inten, tv, importers)
    panel.to_csv(DATA / "panel_eu_sj3_mode1.csv", index=False)

    results = []
    run_spec(results, "(1) Post × M-AI 2024", panel, "post_x_M24", ["post_x_M24"], "EU importers × IND/PHL/VNM; TWFE")
    run_spec(results, "(2) Post × ΔM 2021–24 [headline]", panel, "post_x_dM", ["post_x_dM"], "Preferred: GenAI window is the 2023–24 jump")
    run_spec(results, "(3) Horse race: Post × ΔM", panel, "post_x_dM", ["post_x_dM", "post_x_dF"], "Same regression as (4)")
    run_spec(results, "(4) Horse race: Post × ΔF", panel, "post_x_dF", ["post_x_dM", "post_x_dF"], "Construction AI change, controlling for M")
    run_spec(results, "(5) Placebo SI digital services", panel_si, "post_x_dM", ["post_x_dM"], "Computer services from same partners")
    run_spec(results, "(6) Placebo SE from China", panel_se_chn, "post_x_dM", ["post_x_dM"], "Project-based construction services; BaTIS does not identify mode")
    run_spec(results, "(7) Placebo SJ3 from China", panel_sj3_chn, "post_x_dM", ["post_x_dM"], "SJ3 from China")
    run_spec(results, "(8) Placebo SE from SJ3 exporters", panel_se_m1, "post_x_dM", ["post_x_dM"], "Construction services from IND/PHL/VNM")
    run_spec(results, "(9) Post × (M−F) 2024 gap", panel, "post_x_gap", ["post_x_gap"], "Professional minus construction AI")

    tvp = panel[panel.year.isin([2021, 2023, 2024])].copy()
    out = fit_fe(tvp, "logv", ["ai_M"], ["importer", "year", "partner"], "importer")
    if out:
        res, used = out
        results.append(row("(10) Time-varying M-AI 2021/23/24", res, "ai_M", len(used), "Eurostat years overlapping BaTIS"))
    out = fit_fe(tvp, "logv", ["ai_F"], ["importer", "year", "partner"], "importer")
    if out:
        res, used = out
        results.append(row("(11) Placebo time-varying F-AI", res, "ai_F", len(used), "Construction AI"))

    nocovid = panel[~panel.year.isin([2020, 2021])]
    run_spec(results, "(12) Drop 2020–21", nocovid, "post_x_dM", ["post_x_dM"], "Omit COVID years")

    pre = panel[panel.year.between(2018, 2021)].copy()
    run_spec(results, "(13) Fake post=2020 × ΔM, sample 2018–21", pre, "fake_x_dM", ["fake_x_dM"], "Pre-trend placebo")

    out = fit_fe(panel, "ihs", ["post_x_dM"], ["importer", "year", "partner"], "importer")
    if out:
        res, used = out
        results.append(row("(14) IHS(value), Post × ΔM", res, "post_x_dM", len(used), "arcsinh instead of log"))

    w0 = panel[panel.year == 2019][["importer", "partner", "value"]].rename(columns={"value": "w2019"})
    pw = panel.merge(w0, on=["importer", "partner"], how="left")
    pw["w2019"] = pw.w2019.clip(lower=0.01)
    d = pw[["logv", "post_x_dM", "importer", "year", "partner", "w2019"]].dropna().reset_index(drop=True)
    work = d[["logv", "post_x_dM"]].astype(float)
    for _ in range(8):
        for g in ["importer", "year", "partner"]:
            work = work - work.groupby(d[g].to_numpy()).transform("mean")
    if len(d) >= 20:
        res = sm.WLS(work.logv, work[["post_x_dM"]], weights=d.w2019).fit(
            cov_type="cluster", cov_kwds={"groups": d.importer}
        )
        results.append(row("(15) WLS by 2019 SJ3 value", res, "post_x_dM", len(d), "Larger corridors weighted more"))

    for partner, lab in [("IND", "India"), ("PHL", "Philippines"), ("VNM", "Viet Nam")]:
        sub = panel[panel.partner == partner]
        run_spec(
            results,
            f"(H) {lab} only, Post × ΔM",
            sub,
            "post_x_dM",
            ["post_x_dM"],
            f"Partner = {partner}",
            cluster="importer",
        )

    loo_rows = []
    for iso in sorted(panel.importer.unique()):
        sub = panel[panel.importer != iso]
        out = fit_fe(sub, "logv", ["post_x_dM"], ["importer", "year", "partner"], "importer")
        if not out:
            continue
        res, used = out
        loo_rows.append(
            {
                "dropped": iso,
                "country": ISO2NAME.get(iso, iso),
                "coef": float(res.params["post_x_dM"]),
                "se": float(res.bse["post_x_dM"]),
                "p": float(res.pvalues["post_x_dM"]),
                "n": len(used),
                "display": fmt(res.params["post_x_dM"], res.bse["post_x_dM"], res.pvalues["post_x_dM"]),
            }
        )
    loo = pd.DataFrame(loo_rows)
    loo.to_csv(TAB / "table_loo_importer.csv", index=False)

    t5 = pd.DataFrame(results)
    t5.to_csv(TAB / "table_identification.csv", index=False)

    es = panel.copy()
    year_d = pd.get_dummies(es.year.astype(int), prefix="y", dtype=float)
    inter = []
    for y in range(2018, 2025):
        if y == 2022:
            continue
        col = f"dM_y{y}"
        es[col] = year_d[f"y_{y}"] * es.dM
        inter.append(col)
    out = fit_fe(es, "logv", inter, ["importer", "year", "partner"], "importer")
    es_rows = []
    if out:
        res, used = out
        for y in range(2018, 2025):
            if y == 2022:
                es_rows.append({"year": y, "coef": 0.0, "se": 0.0, "p": 1.0})
            else:
                k = f"dM_y{y}"
                es_rows.append(
                    {
                        "year": y,
                        "coef": float(res.params.get(k, np.nan)),
                        "se": float(res.bse.get(k, np.nan)),
                        "p": float(res.pvalues.get(k, np.nan)),
                    }
                )
    es_df = pd.DataFrame(es_rows)
    es_df.to_csv(TAB / "table_event_study.csv", index=False)

    # Corridors
    def corridor(imp, part, svc, flow="M"):
        s = batis[
            (batis.REF_AREA == imp)
            & (batis.COUNTERPART_AREA == part)
            & (batis.SERVICE == svc)
            & (batis.TRADE_FLOW == flow)
        ]
        return s.sort_values("year")

    desc = []
    for imp, part, svc, lab in [
        ("GBR", "IND", "SJ3", "UK ← India SJ3 (digitally deliverable proxy)"),
        ("GBR", "CHN", "SE", "UK ← China SE (project-based comparison)"),
        ("GBR", "IND", "SI", "UK ← India SI (computer)"),
        ("USA", "IND", "SJ3", "US ← India SJ3"),
        ("DEU", "IND", "SJ3", "Germany ← India SJ3"),
        ("DEU", "POL", "SJ3", "Germany ← Poland SJ3 (nearshore)"),
        ("AUS", "IND", "SJ3", "Australia ← India SJ3"),
        ("NLD", "IND", "SJ3", "Netherlands ← India SJ3"),
        ("FRA", "IND", "SJ3", "France ← India SJ3"),
    ]:
        s = corridor(imp, part, svc)
        if s.empty:
            continue
        v19 = s.loc[s.year == 2019, "value"]
        v24 = s.loc[s.year == 2024, "value"]
        desc.append(
            {
                "series": lab,
                "usd_mn_2019": float(v19.iloc[0]) if len(v19) else np.nan,
                "usd_mn_2024": float(v24.iloc[0]) if len(v24) else np.nan,
            }
        )
    t4 = pd.DataFrame(desc)
    t4["pct"] = 100 * (t4.usd_mn_2024 / t4.usd_mn_2019 - 1)
    t4.to_csv(TAB / "table_batis_corridors.csv", index=False)

    # Eurostat table
    eu_tab = wide.copy()
    eu_tab["country"] = eu_tab.iso3.map(ISO2NAME)
    eu_p = eu_tab.pivot_table(index=["country", "iso3"], columns="year", values=["ai_M", "ai_F"])
    eu_p.columns = [f"{a}_{b}" for a, b in eu_p.columns]
    eu_p.reset_index().to_csv(TAB / "table_eurostat_M_F.csv", index=False)
    inten.assign(country=inten.iso3.map(ISO2NAME)).to_csv(TAB / "table_ai_intensity.csv", index=False)

    # APS
    aps_path = DATA / "from_study1" / "aps_employment_2021_2025.csv"
    if not aps_path.exists():
        aps_path = Path("/workspace/Data_IJCM/04_external_indices/aps_employment_2021_2025.csv")
    aps = pd.read_csv(aps_path)
    aps["soc"] = aps.SOC2020_FULL_NAME.str.extract(r"^(\d{4})")
    aps["name"] = aps.SOC2020_FULL_NAME.str.replace(r"^\d{4}\s*:\s*", "", regex=True)
    aps = aps[aps.soc.isin(SOC_KEEP) & (aps.OBS_STATUS == "A")].copy()
    aps["date"] = pd.to_datetime(aps.DATE)
    aps["emp"] = pd.to_numeric(aps.OBS_VALUE, errors="coerce")
    aps.to_csv(TAB / "table_uk_aps_civil_bundle.csv", index=False)
    first, last = "2021-12", "2025-09"
    chg = []
    for soc, lab in SOC_KEEP.items():
        a = aps[(aps.soc == soc) & (aps.DATE == first)]
        b = aps[(aps.soc == soc) & (aps.DATE == last)]
        if a.empty or b.empty:
            continue
        e0, e1 = float(a.emp.iloc[0]), float(b.emp.iloc[0])
        chg.append({"soc": soc, "occupation": lab, "emp_2021_12": e0, "emp_2025_09": e1, "pct": 100 * (e1 / e0 - 1)})
    t_aps = pd.DataFrame(chg)
    t_aps.to_csv(TAB / "table_uk_aps_change.csv", index=False)

    uk_sj3 = corridor("GBR", "IND", "SJ3")
    aps_y = (
        aps[aps.soc == "2121"]
        .assign(year=lambda x: x.date.dt.year)
        .groupby("year", as_index=False)["emp"]
        .mean()
    )
    ukm = uk_sj3.merge(aps_y, on="year", how="inner")
    ukm["log_sj3"] = np.log(ukm.value)
    ukm["log_emp"] = np.log(ukm.emp)
    ukm.to_csv(TAB / "table_uk_aps_vs_india_sj3.csv", index=False)
    uk_corr = float(ukm.log_sj3.corr(ukm.log_emp)) if len(ukm) >= 3 else np.nan

    # ILO
    ilo = pd.read_csv(DATA / "ilo_emp_FM.csv")
    ilo["year"] = ilo.TIME_PERIOD.astype(int)
    ilo["emp"] = pd.to_numeric(ilo.OBS_VALUE, errors="coerce")
    ilo["sector"] = ilo.ECO.map({"ECO_ISIC4_F": "F", "ECO_ISIC4_M": "M"})
    iw = ilo.pivot_table(index=["REF_AREA", "year"], columns="sector", values="emp").reset_index()
    g = []
    for iso, s in iw.groupby("REF_AREA"):
        r19, r24 = s[s.year == 2019], s[s.year == 2024]
        if r19.empty or r24.empty:
            continue
        g.append(
            {
                "iso3": iso,
                "country": ISO2NAME.get(iso, iso),
                "M_2019": float(r19.M.iloc[0]),
                "M_2024": float(r24.M.iloc[0]),
                "F_2019": float(r19.F.iloc[0]),
                "F_2024": float(r24.F.iloc[0]),
            }
        )
    t7 = pd.DataFrame(g)
    t7["pct_M"] = 100 * (t7.M_2024 / t7.M_2019 - 1)
    t7["pct_F"] = 100 * (t7.F_2024 / t7.F_2019 - 1)
    t7.to_csv(TAB / "table_ilo_FM.csv", index=False)

    # World Bank
    def wb_df(path, name):
        js = json.loads(Path(path).read_text())
        rows = []
        if not isinstance(js, list) or len(js) < 2 or js[1] is None:
            return pd.DataFrame(columns=["iso3", "year", name])
        for o in js[1]:
            if o.get("value") is None:
                continue
            rows.append({"iso3": o["countryiso3code"], "year": int(o["date"]), name: float(o["value"])})
        return pd.DataFrame(rows)

    gdp = wb_df(DATA / "wb_NY_GDP_MKTP_CD.json", "gdp_usd")
    srv = wb_df(DATA / "wb_NV_SRV_TOTL_ZS.json", "srv_share")
    ind = wb_df(DATA / "wb_NV_IND_TOTL_ZS.json", "ind_share")
    wb = gdp.merge(srv, on=["iso3", "year"], how="outer").merge(ind, on=["iso3", "year"], how="outer")
    wb.to_csv(TAB / "table_world_bank.csv", index=False)

    # Cross-section Δlog India 2022-24
    chg_in = sj3[(sj3.importer.isin(importers)) & (sj3.partner == "IND") & (sj3.year.isin([2022, 2024]))]
    chg_in = chg_in.pivot_table(index="importer", columns="year", values="value").reset_index()
    chg_in = chg_in.rename(columns={2022: "v22", 2024: "v24"})
    chg_in["dlog"] = np.log(chg_in.v24) - np.log(chg_in.v22)
    chg_in = chg_in.merge(inten, left_on="importer", right_on="iso3")
    chg_in = chg_in.dropna(subset=["dlog", "dM"])
    chg_in.to_csv(TAB / "table_cross_section_india.csv", index=False)
    if len(chg_in) >= 8:
        rA = sm.OLS(chg_in.dlog, sm.add_constant(chg_in["dM"])).fit(cov_type="HC1")
        results.append(row("(16) Cross-section Δlog IN SJ3 22–24 on ΔM", rA, "dM", len(chg_in), "No FE; one obs per importer"))

    eu8 = ["DEU", "FRA", "NLD", "POL", "ITA", "ESP", "IRL", "ROU"]
    run_spec(
        results,
        "(17) EU-8 only: Post × ΔM 2021–24",
        panel[panel.importer.isin(eu8)],
        "post_x_dM",
        ["post_x_dM"],
        "DEU FRA NLD POL ITA ESP IRL ROU; fragility check",
    )
    tv8 = panel[panel.importer.isin(eu8) & panel.year.isin([2021, 2023, 2024])]
    out = fit_fe(tv8, "logv", ["ai_M"], ["importer", "year", "partner"], "importer")
    if out:
        res, used = out
        results.append(row("(18) EU-8 only: time-varying M-AI", res, "ai_M", len(used), "Same 8 importers, 2021/23/24"))
    pd.DataFrame(results).to_csv(TAB / "table_identification.csv", index=False)

    # Figures
    years = [2021, 2023, 2024, 2025]
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    m = [eu27[(eu27.nace == "M") & (eu27.year == y)].ai_pct.iloc[0] for y in years]
    f = [eu27[(eu27.nace == "F") & (eu27.year == y)].ai_pct.iloc[0] for y in years]
    ax.plot(years, m, marker="o", label="NACE M professional, scientific, technical")
    ax.plot(years, f, marker="s", label="NACE F construction (placebo)")
    ax.set_ylabel("Enterprises using AI, % (10+ persons)")
    ax.set_xlabel("Year")
    ax.set_title("Eurostat enterprise AI use: professional services vs construction, EU-27")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "figure1_eurostat_M_vs_F.png")
    plt.close()

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    for soc, lab in SOC_KEEP.items():
        s = aps[aps.soc == soc].sort_values("date")
        if s.empty:
            continue
        ax.plot(s.date, s.emp / 1000, marker="o", ms=3, label=f"{soc} {lab}")
    ax.set_ylabel("Employment (thousands)")
    ax.set_xlabel("Survey date")
    ax.set_title("UK APS: civil-adjacent occupations, 2021–2025")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "figure2_uk_aps_bundle.png")
    plt.close()

    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    for imp, part, svc, lab in [
        ("GBR", "IND", "SJ3", "UK ← India SJ3 (Mode 1)"),
        ("GBR", "CHN", "SE", "UK ← China SE (Mode 3)"),
        ("GBR", "IND", "SI", "UK ← India SI (computer)"),
    ]:
        s = corridor(imp, part, svc)
        ax.plot(s.year, s.value, marker="o", label=lab)
    ax.set_ylabel("USD million (BaTIS balanced)")
    ax.set_xlabel("Year")
    ax.set_title("UK imports: SJ3 vs construction SE vs computer SI")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "figure3_uk_trade.png")
    plt.close()

    if not es_df.empty:
        fig, ax = plt.subplots(figsize=(8.2, 4.6))
        ax.axhline(0, color="0.4", lw=0.8)
        ax.axvline(2022.5, color="0.6", ls="--", lw=0.8, label="ChatGPT public release")
        ax.errorbar(es_df.year, es_df.coef, yerr=1.96 * es_df.se.replace({0: np.nan}), fmt="o-", capsize=3)
        ax.set_xlabel("Year (2022 = reference)")
        ax.set_ylabel("Year × importer ΔM AI 2021–24")
        ax.set_title("Event study: EU SJ3 imports from India, Philippines, Viet Nam")
        ax.legend(frameon=False)
        fig.tight_layout()
        fig.savefig(FIG / "figure4_event_study.png")
        plt.close()

    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    t7s = t7.sort_values("pct_M")
    y = np.arange(len(t7s))
    h = 0.35
    ax.barh(y + h / 2, t7s.pct_M, height=h, label="ISIC M professional")
    ax.barh(y - h / 2, t7s.pct_F, height=h, label="ISIC F construction")
    ax.set_yticks(y, t7s.country)
    ax.set_xlabel("Percent change, 2019–2024")
    ax.set_title("ILO employment: professional services vs construction")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "figure5_ilo_M_vs_F.png")
    plt.close()

    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    for part, svc, lab in [
        ("IND", "SJ3", "EU ← India SJ3"),
        ("PHL", "SJ3", "EU ← Philippines SJ3"),
        ("VNM", "SJ3", "EU ← Viet Nam SJ3"),
        ("CHN", "SE", "EU ← China SE"),
    ]:
        s = sj3 if svc == "SJ3" and part != "CHN" else None
        src = batis[
            (batis.REF_AREA.isin(importers))
            & (batis.TRADE_FLOW == "M")
            & (batis.SERVICE == svc)
            & (batis.COUNTERPART_AREA == part)
        ]
        gsum = src.groupby("year", as_index=False)["value"].sum()
        ax.plot(gsum.year, gsum.value, marker="o", label=lab)
    ax.set_ylabel("USD million (sum of balanced imports)")
    ax.set_xlabel("Year")
    ax.set_title("EU-importer engineering-related imports: SJ3 vs China SE")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "figure6_eu_mode1_vs_china.png")
    plt.close()

    fig, ax = plt.subplots(figsize=(6.6, 4.8))
    ax.scatter(chg_in.dM, chg_in.dlog)
    for _, r in chg_in.iterrows():
        ax.annotate(r.importer, (r.dM, r.dlog), textcoords="offset points", xytext=(4, 4), fontsize=8)
    ax.set_xlabel("Eurostat NACE M AI, 2024 minus 2021 (pp)")
    ax.set_ylabel("Δ log SJ3 imports from India, 2022–24")
    ax.set_title("Importer professional-AI acceleration and India SJ3 growth")
    fig.tight_layout()
    fig.savefig(FIG / "figure7_cross_section.png")
    plt.close()

    if not loo.empty:
        fig, ax = plt.subplots(figsize=(8.2, 5.0))
        loo2 = loo.sort_values("coef")
        ax.errorbar(loo2.coef, np.arange(len(loo2)), xerr=1.96 * loo2.se, fmt="o", capsize=3)
        ax.axvline(0, color="0.5", lw=0.8)
        ax.set_yticks(np.arange(len(loo2)), "drop " + loo2.dropped)
        ax.set_xlabel("Post × ΔM coefficient")
        ax.set_title("Leave-one-importer-out robustness")
        fig.tight_layout()
        fig.savefig(FIG / "figure8_loo.png")
        plt.close()

    headline = {
        "importers": importers,
        "n_importers": len(importers),
        "n_panel": int(len(panel)),
        "batis_balanced_rows": int(len(batis)),
        "uk_log_corr_2121_sj3": uk_corr,
        "uk_n_overlap": int(len(ukm)),
        "aps_change": t_aps.to_dict(orient="records"),
        "identification": results,
        "cannot_identify": "A-country civil-engineer headcount causing B-country GDP or engineer counts",
        "identified_object": "Importer NACE M AI change × post-2023 associated with SJ3 imports; F/SE/SI/China comparisons",
    }
    (ROOT / "results.json").write_text(json.dumps(headline, indent=2, default=str))
    print("importers", len(importers), importers)
    print("panel", len(panel))
    print(pd.DataFrame(results)[["spec", "display", "n"]].to_string(index=False))
    print("UK corr", uk_corr, "n", len(ukm))
    print("APS\n", t_aps)


if __name__ == "__main__":
    main()
