#!/usr/bin/env python3
"""UK–India experiments: implement the measurement formulas on official cells.

Identification
--------------
Neither the UK nor India is in the Eurostat enterprise-NLG panel. The shock
used here is the *calendar event* of public ChatGPT (late 2022). That is a
common time break, not a measured UK or Indian adoption rate. Results are
descriptive growth, mix indices, and a two-by-two service-heading contrast.
They are not a causal GenAI treatment effect.

Formulas are defined in UK_INDIA_MEASUREMENT.md and coded below without
filling missing years.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "10_uk_india"
TAB = PROBE / "tables"
FIG = PROBE / "figures"
EXT = ROOT / "04_external_indices"
ILO = ROOT / "02_industry_accounts" / "ilo_emp_FM.csv"
APS = EXT / "from_study1" / "aps_employment_2021_2025.csv"
ELO = EXT / "eloundou_occ_level.csv"
for p in (TAB, FIG):
    p.mkdir(parents=True, exist_ok=True)

# Eloundou human β mapped only where Study 4 already records a civil O*NET match.
# Do not invent scores for occupations without a documented crosswalk.
EXPOSURE = {
    "2121": 0.375,   # Civil engineers ~ O*NET 17-2051
    "3120": 0.52,    # CAD / drafters ~ 17-3011
    "3114": 0.477,   # Civil engineering technicians ~ 17-3022
}


def g(v1, v0):
    if pd.isna(v1) or pd.isna(v0) or v0 <= 0 or v1 <= 0:
        return np.nan
    return float(np.log(v1) - np.log(v0))


def pick(df, ref, cpt, svc, year, adj="B"):
    sub = df[
        (df.REF_AREA == ref)
        & (df.COUNTERPART_AREA == cpt)
        & (df.SERVICE == svc)
        & (df.ADJUSTMENT == adj)
        & (df.TIME_PERIOD == year)
    ]
    if sub.empty:
        return np.nan
    return float(pd.to_numeric(sub.OBS_VALUE, errors="coerce").iloc[0])


def series(df, ref, cpt, svc, adj="B"):
    sub = df[
        (df.REF_AREA == ref)
        & (df.COUNTERPART_AREA == cpt)
        & (df.SERVICE == svc)
        & (df.ADJUSTMENT == adj)
    ].copy()
    sub["year"] = sub.TIME_PERIOD.astype(int)
    sub["value"] = pd.to_numeric(sub.OBS_VALUE, errors="coerce")
    return sub.dropna(subset=["value"]).sort_values("year")[["year", "value", "OBS_STATUS"]]


def main():
    plt.rcParams.update({
        "figure.dpi": 140, "savefig.dpi": 200, "font.size": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.25,
    })
    raw = pd.read_csv(PROBE / "batis_uk_india.csv")
    raw["TIME_PERIOD"] = raw.TIME_PERIOD.astype(int)

    years = list(range(2015, 2025))
    recs = []
    for adj in ["B", "N"]:
        for y in years:
            m_sj3 = pick(raw, "GBR", "IND", "SJ3", y, adj)
            m_se = pick(raw, "GBR", "IND", "SE", y, adj)
            m_si = pick(raw, "GBR", "IND", "SI", y, adj)
            x_sj3 = pick(raw, "IND", "GBR", "SJ3", y, adj)
            x_se = pick(raw, "IND", "GBR", "SE", y, adj)
            x_si = pick(raw, "IND", "GBR", "SI", y, adj)
            w_sj3 = pick(raw, "GBR", "W", "SJ3", y, adj)
            w_se = pick(raw, "GBR", "W", "SE", y, adj)
            # (1) digitally deliverable intensity
            ddi_imp = m_sj3 / (m_sj3 + m_se) if (m_sj3 + m_se) and not pd.isna(m_sj3 + m_se) else np.nan
            ddi_exp = x_sj3 / (x_sj3 + x_se) if (x_sj3 + x_se) and not pd.isna(x_sj3 + x_se) else np.nan
            # (2) net sourcing position
            nsp = np.log(m_sj3) - np.log(x_sj3) if m_sj3 > 0 and x_sj3 > 0 else np.nan
            # (3) transnational mix index (task vs project)
            tmi_imp = np.log(m_sj3) - np.log(m_se) if m_sj3 > 0 and m_se > 0 else np.nan
            tmi_exp = np.log(x_sj3) - np.log(x_se) if x_sj3 > 0 and x_se > 0 else np.nan
            # (4) computer-services placebo gap
            pg = np.log(m_sj3) - np.log(m_si) if m_sj3 > 0 and m_si > 0 else np.nan
            # (5) India share of UK world SJ3
            share = m_sj3 / w_sj3 if w_sj3 and w_sj3 > 0 else np.nan
            recs.append({
                "adjustment": adj, "year": y,
                "M_UK_IN_SJ3": m_sj3, "M_UK_IN_SE": m_se, "M_UK_IN_SI": m_si,
                "M_IN_UK_SJ3": x_sj3, "M_IN_UK_SE": x_se, "M_IN_UK_SI": x_si,
                "M_UK_W_SJ3": w_sj3, "M_UK_W_SE": w_se,
                "DDI_imp": ddi_imp, "DDI_exp": ddi_exp,
                "NSP": nsp, "TMI_imp": tmi_imp, "TMI_exp": tmi_exp,
                "PG": pg, "India_share_UK_SJ3": share,
            })
    idx = pd.DataFrame(recs)
    idx.to_csv(TAB / "uk_india_indices.csv", index=False)

    # Event growth (6): log V_t1 - log V_t0
    growth_rows = []
    for adj in ["B", "N"]:
        for t0, t1, window in [(2019, 2024, "2019-24"), (2022, 2024, "2022-24"),
                               (2015, 2019, "2015-19 pre"), (2019, 2022, "2019-22")]:
            for ref, cpt, lab in [("GBR", "IND", "UK←IN"), ("IND", "GBR", "IN←UK")]:
                for svc in ["SJ3", "SE", "SI", "SJ1", "SJ2"]:
                    v0, v1 = pick(raw, ref, cpt, svc, t0, adj), pick(raw, ref, cpt, svc, t1, adj)
                    growth_rows.append({
                        "adjustment": adj, "window": window, "flow": lab,
                        "service": svc, "v0": v0, "v1": v1, "dlog": g(v1, v0),
                        "pct": (np.exp(g(v1, v0)) - 1) * 100 if not pd.isna(g(v1, v0)) else np.nan,
                    })
    growth = pd.DataFrame(growth_rows)
    growth.to_csv(TAB / "uk_india_event_growth.csv", index=False)

    # (7) Difference-in-growth (DiG)
    # DiG = (g_SJ3 - g_SE)_UK←IN - (g_SJ3 - g_SE)_IN←UK
    dig_rows = []
    for adj in ["B", "N"]:
        for window in ["2019-24", "2022-24", "2015-19 pre", "2019-22"]:
            def dg(flow, svc):
                hit = growth[(growth.adjustment == adj) & (growth.window == window)
                             & (growth.flow == flow) & (growth.service == svc)]
                return float(hit.dlog.iloc[0]) if len(hit) else np.nan
            uk = dg("UK←IN", "SJ3") - dg("UK←IN", "SE")
            india = dg("IN←UK", "SJ3") - dg("IN←UK", "SE")
            si_gap = dg("UK←IN", "SJ3") - dg("UK←IN", "SI")
            dig_rows.append({
                "adjustment": adj, "window": window,
                "mix_UK_imports": uk, "mix_IN_imports": india,
                "DiG": uk - india,
                "SJ3_minus_SI_UK_imports": si_gap,
            })
    dig = pd.DataFrame(dig_rows)
    dig.to_csv(TAB / "uk_india_DiG.csv", index=False)

    # (8) Stacked 2×2: log value on Post × 1[SJ3] among {SJ3, SE}, UK←IN
    def stacked_did(ref, cpt, treated, control, adj="B", post_year=2023):
        a = series(raw, ref, cpt, treated, adj)
        b = series(raw, ref, cpt, control, adj)
        years = sorted(set(a.year) & set(b.year))
        if len(years) < 8:
            return {
                "flow": f"{ref}←{cpt}", "treated": treated, "control": control,
                "adj": adj, "n": int(len(years) * 2),
                "coef": np.nan, "se": np.nan, "p": np.nan,
                "note": f"too few overlapping years ({len(years)}); not estimated",
            }
        a = a[a.year.isin(years)]
        b = b[b.year.isin(years)]
        a["heading"] = treated
        b["heading"] = control
        d = pd.concat([a, b], ignore_index=True)
        d["logv"] = np.log(d.value.clip(lower=0.01))
        d["post"] = (d.year >= post_year).astype(float)
        d["sj3"] = (d.heading == treated).astype(float)
        d["post_x_sj3"] = d.post * d.sj3
        X = sm.add_constant(d[["sj3", "post", "post_x_sj3"]])
        res = sm.OLS(d.logv, X).fit(cov_type="HC1")
        return {
            "flow": f"{ref}←{cpt}", "treated": treated, "control": control,
            "adj": adj, "n": int(len(d)),
            "coef": float(res.params["post_x_sj3"]),
            "se": float(res.bse["post_x_sj3"]),
            "p": float(res.pvalues["post_x_sj3"]),
            "note": "2x2 heading × post; not a country NLG treatment",
        }

    did_rows = []
    for adj in ["B", "N"]:
        for spec in [
            ("GBR", "IND", "SJ3", "SE"),
            ("IND", "GBR", "SJ3", "SE"),
            ("GBR", "IND", "SJ3", "SI"),
            ("GBR", "IND", "SJ3", "SJ2"),
            ("GBR", "IND", "SJ1", "SE"),
        ]:
            out = stacked_did(*spec, adj=adj)
            if out:
                did_rows.append(out)
    did = pd.DataFrame(did_rows)
    if not did.empty:
        def _disp(r):
            if pd.isna(r.coef):
                return "—"
            star = "***" if r.p < 0.01 else "**" if r.p < 0.05 else "*" if r.p < 0.10 else ""
            return f"{r.coef:.3f}{star} ({r.se:.3f})"
        did["display"] = did.apply(_disp, axis=1)
    did.to_csv(TAB / "uk_india_stacked_did.csv", index=False)

    # UK occupations (9)–(10)
    aps = pd.read_csv(APS)
    aps["soc"] = aps.SOC2020_FULL_NAME.str.extract(r"^(\d{4})")
    aps["year"] = pd.to_datetime(aps.DATE).dt.year
    aps["value"] = pd.to_numeric(aps.OBS_VALUE, errors="coerce")
    keep = {
        "2121": "Civil engineers",
        "3120": "CAD/drafters",
        "3114": "Civil engineering technicians",
        "2455": "Construction project managers",
        "2114": "Physical scientists (comparison)",
    }
    ann = aps[aps.soc.isin(keep)].groupby(["year", "soc"], as_index=False)["value"].mean()
    occ = []
    for y, sub in ann.groupby("year"):
        e = {r.soc: r.value for _, r in sub.iterrows()}
        pol = np.log(e["3114"]) - np.log(e["3120"]) if e.get("3114") and e.get("3120") else np.nan
        wsum, w = 0.0, 0.0
        for soc, beta in EXPOSURE.items():
            if pd.isna(beta) or soc not in e:
                continue
            wsum += beta * np.log(e[soc])
            w += beta
        occ.append({
            "year": int(y),
            **{f"E_{s}": e.get(s, np.nan) for s in keep},
            "Pol_tech_minus_CAD": pol,
            "exposure_weighted_logE": wsum / w if w else np.nan,
        })
    occ_df = pd.DataFrame(occ)
    occ_df.to_csv(TAB / "uk_occupation_indices.csv", index=False)
    pre = occ_df[occ_df.year.isin([2021, 2022])].mean(numeric_only=True)
    post = occ_df[occ_df.year.isin([2023, 2024, 2025])].mean(numeric_only=True)
    occ_chg = pd.DataFrame({
        "metric": ["E_2121", "E_3120", "E_3114", "E_2455", "E_2114",
                   "Pol_tech_minus_CAD", "exposure_weighted_logE"],
        "pre_2021_22": [pre.get(m) for m in ["E_2121", "E_3120", "E_3114", "E_2455", "E_2114",
                                             "Pol_tech_minus_CAD", "exposure_weighted_logE"]],
        "post_2023_25": [post.get(m) for m in ["E_2121", "E_3120", "E_3114", "E_2455", "E_2114",
                                              "Pol_tech_minus_CAD", "exposure_weighted_logE"]],
    })
    occ_chg["pct_or_diff"] = np.where(
        occ_chg.metric.str.startswith("E_"),
        100 * (occ_chg.post_2023_25 / occ_chg.pre_2021_22 - 1),
        occ_chg.post_2023_25 - occ_chg.pre_2021_22,
    )
    occ_chg.to_csv(TAB / "uk_occupation_prepost.csv", index=False)

    # ILO ISIC F vs M, UK and India (11)
    ilo = pd.read_csv(ILO)
    ilo = ilo[ilo.REF_AREA.isin(["GBR", "IND"])].copy()
    ilo["year"] = ilo.TIME_PERIOD.astype(int)
    ilo["value"] = pd.to_numeric(ilo.OBS_VALUE, errors="coerce")
    lab = {"ECO_ISIC4_F": "construction_F", "ECO_ISIC4_M": "professional_M"}
    ilo["ind"] = ilo.ECO.map(lab)
    wide = ilo.pivot_table(index=["REF_AREA", "year"], columns="ind", values="value").reset_index()
    wide["logM_minus_logF"] = np.log(wide.professional_M) - np.log(wide.construction_F)
    wide.to_csv(TAB / "uk_india_ilo_FM.csv", index=False)

    # World Bank context
    wb_path = PROBE / "wb_uk_india.csv"
    if wb_path.exists():
        wb = pd.read_csv(wb_path)
        wb.to_csv(TAB / "wb_uk_india_context.csv", index=False)

    # Figures
    b = idx[idx.adjustment == "B"]
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.plot(b.year, b.M_UK_IN_SJ3, marker="o", label="UK←IN SJ3")
    ax.plot(b.year, b.M_IN_UK_SJ3, marker="s", label="IN←UK SJ3")
    ax.axvline(2022.75, color="0.6", ls="--", lw=0.8, label="ChatGPT public")
    ax.set_ylabel("USD million (BaTIS B)")
    ax.set_title("UK–India technical and other business services (SJ3)")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "figure_uk_india_sj3.png")
    plt.close()

    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.plot(b.year, 100 * b.DDI_imp, marker="o", label="UK imports DDI")
    ax.plot(b.year, 100 * b.DDI_exp, marker="s", label="India imports DDI")
    ax.axvline(2022.75, color="0.6", ls="--", lw=0.8)
    ax.set_ylabel("SJ3 / (SJ3+SE), percent")
    ax.set_title("Digitally deliverable intensity, UK–India")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIG / "figure_uk_india_DDI.png")
    plt.close()

    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.plot(b.year, b.TMI_imp, marker="o", label="TMI UK imports")
    ax.plot(b.year, b.NSP, marker="^", label="Net sourcing (log UK←IN − log IN←UK)")
    ax.axhline(0, color="0.4", lw=0.7)
    ax.axvline(2022.75, color="0.6", ls="--", lw=0.8)
    ax.set_title("Mix and sourcing position, UK–India SJ3 vs SE")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "figure_uk_india_TMI_NSP.png")
    plt.close()

    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    for soc, name in keep.items():
        s = ann[ann.soc == soc].sort_values("year")
        ax.plot(s.year, s.value / 1000, marker="o", label=f"{soc} {name}")
    ax.axvline(2022.75, color="0.6", ls="--", lw=0.8)
    ax.set_ylabel("Employment (thousands)")
    ax.set_title("UK civil-related occupations (APS)")
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout()
    fig.savefig(FIG / "figure_uk_occupations.png")
    plt.close()

    headline = {
        "identification": "Calendar break around ChatGPT; not a measured UK/India NLG rate",
        "cannot_identify": [
            "Generative AI caused UK civil jobs to move to India",
            "SJ312 civil invoices (not in BaTIS; UK ITS ends 2019)",
            "GATS Mode 1 vs Mode 3",
        ],
        "indices_B_2019_2024": {
            "M_UK_IN_SJ3": {
                "2019": pick(raw, "GBR", "IND", "SJ3", 2019),
                "2024": pick(raw, "GBR", "IND", "SJ3", 2024),
            },
            "DDI_imp": {
                "2019": float(b.loc[b.year == 2019, "DDI_imp"].iloc[0]) if (b.year == 2019).any() else None,
                "2024": float(b.loc[b.year == 2024, "DDI_imp"].iloc[0]) if (b.year == 2024).any() else None,
            },
            "NSP": {
                "2019": float(b.loc[b.year == 2019, "NSP"].iloc[0]) if (b.year == 2019).any() else None,
                "2024": float(b.loc[b.year == 2024, "NSP"].iloc[0]) if (b.year == 2024).any() else None,
            },
            "India_share_UK_SJ3": {
                "2019": float(b.loc[b.year == 2019, "India_share_UK_SJ3"].iloc[0]) if (b.year == 2019).any() else None,
                "2024": float(b.loc[b.year == 2024, "India_share_UK_SJ3"].iloc[0]) if (b.year == 2024).any() else None,
            },
        },
        "DiG": dig.to_dict(orient="records"),
        "stacked_did": did.to_dict(orient="records") if not did.empty else [],
        "occupation_prepost": occ_chg.to_dict(orient="records"),
    }
    (PROBE / "results_uk_india.json").write_text(json.dumps(headline, indent=2, default=str))
    print("INDICES 2019 vs 2024 (B)")
    print(b[b.year.isin([2019, 2024])][
        ["year", "M_UK_IN_SJ3", "M_IN_UK_SJ3", "DDI_imp", "NSP", "TMI_imp", "India_share_UK_SJ3"]
    ].to_string(index=False))
    print("\nDiG")
    print(dig.to_string(index=False))
    print("\nStacked DiD")
    print(did.to_string(index=False) if not did.empty else "empty")
    print("\nOccupations")
    print(occ_chg.to_string(index=False))


if __name__ == "__main__":
    main()
