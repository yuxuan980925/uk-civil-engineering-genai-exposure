#!/usr/bin/env python3
"""UK-India generative-AI shock model for the civil-engineering industry.

Estimates a two-country (United Kingdom, India) empirical model of the
generative-AI shock (ChatGPT, Nov 2022) on the civil-engineering industry:

  Model 1 (labour side)  Difference-in-differences on UK APS employment,
                         codifiable civil-design core (SOC 2121 civil
                         engineers + 3120 CAD/architectural drafters) versus
                         the rest of the civil-adjacent occupations.
  Model 2 (offshoring)   Interrupted time series on UK <- India Mode-1
                         engineering-related services imports (OECD-WTO BaTIS
                         SJ3), 2015-2024, with a pre-trend placebo.
  Model 3 (exposure)     Cross-occupation slope of UK employment change on
                         Eloundou generative-text exposure (human beta).

Outputs: result tables in ``tables/`` (tbl_ukin_*.csv) and figures in
``figures/`` (fig_ukin_*.png). All numbers come from the local official CSVs;
nothing is interpolated here.

Usage:
    python3 scripts/uk_india_genai_model.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGS = ROOT / "figures"
TABLES = ROOT / "tables"
FIGS.mkdir(exist_ok=True)
TABLES.mkdir(exist_ok=True)

SHOCK_YEAR = 2022          # ChatGPT launched Nov 2022
POST_FROM = "2023-03"      # first APS quarter fully after the shock

# Codifiable civil-design core predicted by the task model to be AI-substituted.
CORE_SOC = {"2121", "3120"}


def load_trade() -> pd.DataFrame:
    b = pd.read_csv(DATA / "batis_civil_related.csv")
    m = b[
        (b.REF_AREA == "GBR")
        & (b.COUNTERPART_AREA == "IND")
        & (b.TRADE_FLOW == "M")
        & (b.SERVICE == "SJ3")
        & (b.ADJUSTMENT == "B")
    ][["TIME_PERIOD", "OBS_VALUE"]].copy()
    m = m.rename(columns={"TIME_PERIOD": "year", "OBS_VALUE": "sj3"})
    m = m.sort_values("year").reset_index(drop=True)
    m["lsj3"] = np.log(m["sj3"])
    return m


def load_aps() -> pd.DataFrame:
    a = pd.read_csv(DATA / "from_study1" / "aps_employment_2021_2025.csv")
    a = a.rename(columns={"OBS_VALUE": "emp"})
    a["soc"] = a["SOC2020_FULL_NAME"].str.split(":").str[0].str.strip()
    a["occupation"] = a["SOC2020_FULL_NAME"].str.split(":").str[1].str.strip()
    a["date"] = a["DATE"].astype(str)
    a["emp"] = pd.to_numeric(a["emp"], errors="coerce")
    a = a.dropna(subset=["emp"])
    a["lemp"] = np.log(a["emp"])
    a["core"] = a["soc"].isin(CORE_SOC).astype(int)
    a["post"] = (a["date"] >= POST_FROM).astype(int)
    a["core_post"] = a["core"] * a["post"]
    return a


def model_trade(trade: pd.DataFrame) -> dict:
    d = trade.copy()
    d["t"] = d["year"] - d["year"].min()
    d["post"] = (d["year"] > SHOCK_YEAR).astype(int)
    its = smf.ols("lsj3 ~ t + post", data=d).fit(cov_type="HC1")

    # Pre-trend placebo: fake shock in 2019, restricted to the pre-period only.
    pre = d[d.year <= SHOCK_YEAR].copy()
    pre["fake_post"] = (pre["year"] > 2019).astype(int)
    placebo = smf.ols("lsj3 ~ t + fake_post", data=pre).fit(cov_type="HC1")

    pre_cagr = np.exp(
        (d.loc[d.year == SHOCK_YEAR, "lsj3"].iloc[0]
         - d.loc[d.year == d.year.min(), "lsj3"].iloc[0])
        / (SHOCK_YEAR - d.year.min())
    ) - 1
    post_growth = d.loc[d.year == 2024, "sj3"].iloc[0] / d.loc[d.year == SHOCK_YEAR, "sj3"].iloc[0] - 1
    return {
        "its": its,
        "placebo": placebo,
        "pre_cagr": pre_cagr,
        "post_growth": post_growth,
        "d": d,
    }


def model_labour(aps: pd.DataFrame) -> dict:
    did = smf.ols("lemp ~ C(soc) + C(date) + core_post", data=aps).fit(
        cov_type="cluster", cov_kwds={"groups": aps["soc"]}
    )
    # Pre-trend placebo: pre-period only, fake post at 2022-06.
    pre = aps[aps.date < POST_FROM].copy()
    pre["fake_post"] = (pre["date"] >= "2022-06").astype(int)
    pre["core_fake"] = pre["core"] * pre["fake_post"]
    placebo = smf.ols("lemp ~ C(soc) + C(date) + core_fake", data=pre).fit(
        cov_type="cluster", cov_kwds={"groups": pre["soc"]}
    )
    return {"did": did, "placebo": placebo}


def model_exposure(aps: pd.DataFrame) -> dict:
    elo = pd.read_csv(DATA / "eloundou_occ_level.csv")
    title_to_beta = dict(zip(elo["Title"], elo["human_rating_beta"]))
    # Map UK SOC civil occupations to Eloundou O*NET titles (generative exposure).
    soc_to_title = {
        "2121": "Civil Engineers",
        "3120": "Architectural and Civil Drafters",
        "3114": "Civil Engineering Technologists and Technicians",
    }
    first = aps[aps.date == aps.date.min()][["soc", "occupation", "emp"]].rename(columns={"emp": "emp0"})
    last = aps[aps.date == aps.date.max()][["soc", "emp"]].rename(columns={"emp": "emp1"})
    x = first.merge(last, on="soc")
    x["dlog"] = np.log(x["emp1"] / x["emp0"])
    x["beta"] = x["soc"].map({s: title_to_beta[t] for s, t in soc_to_title.items()})
    scored = x.dropna(subset=["beta"]).copy()
    fit = smf.ols("dlog ~ beta", data=scored).fit()
    return {"fit": fit, "scored": scored, "all": x}


def figure_trade(res: dict) -> None:
    d = res["d"]
    its = res["its"]
    fig, ax = plt.subplots(figsize=(7, 4.3))
    ax.plot(d.year, d.sj3, "o-", color="#1f77b4", label="UK ← India SJ3 (Mode 1), USD mn")
    d = d.assign(fit=np.exp(its.fittedvalues))
    ax.plot(d.year, d.fit, "--", color="#d62728", label="Interrupted time-series fit")
    ax.axvline(SHOCK_YEAR + 0.5, color="grey", ls=":", lw=1)
    ax.text(SHOCK_YEAR + 0.55, ax.get_ylim()[1] * 0.35, "ChatGPT\nNov 2022", fontsize=8, color="grey")
    ax.set_xlabel("Year")
    ax.set_ylabel("USD million (balanced)")
    ax.set_title("UK imports of engineering-related services from India (BaTIS SJ3)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGS / "fig_ukin_1_trade.png", dpi=150)
    plt.close(fig)


def figure_employment(aps: pd.DataFrame) -> None:
    def index(group: pd.DataFrame) -> pd.Series:
        piv = group.groupby("date")["emp"].sum()
        return 100 * piv / piv.iloc[0]

    core = index(aps[aps.core == 1])
    rest = index(aps[aps.core == 0])
    fig, ax = plt.subplots(figsize=(7, 4.3))
    ax.plot(core.index, core.values, "o-", color="#d62728", label="Codifiable design core (SOC 2121 + 3120)")
    ax.plot(rest.index, rest.values, "s-", color="#1f77b4", label="Other civil-adjacent occupations")
    ax.axvline(POST_FROM, color="grey", ls=":", lw=1)
    ax.set_xticks(list(core.index)[::3])
    ax.set_xticklabels(list(core.index)[::3], rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Employment index (2021-12 = 100)")
    ax.set_title("UK civil-engineering employment: exposed design core vs rest")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGS / "fig_ukin_2_employment.png", dpi=150)
    plt.close(fig)


def figure_exposure(expo: dict, aps: pd.DataFrame) -> None:
    x = expo["all"].copy()
    beta_map = {"2121": 0.375, "3120": 0.52, "3114": 0.4772727}
    x["beta_plot"] = x["soc"].map(beta_map)
    xs = x.dropna(subset=["beta_plot"])
    fig, ax = plt.subplots(figsize=(7, 4.3))
    ax.scatter(xs["beta_plot"], 100 * xs["dlog"], color="#1f77b4")
    for _, r in xs.iterrows():
        ax.annotate(f"{r.soc}", (r.beta_plot, 100 * r.dlog), fontsize=8,
                    xytext=(4, 4), textcoords="offset points")
    ax.axhline(0, color="grey", lw=0.8)
    ax.set_xlabel("Eloundou generative-text exposure (human β)")
    ax.set_ylabel("UK employment change 2021-12 → 2025-09 (%)")
    ax.set_title("Exposure is polarised, not uniform (SOC 3114 rose)")
    fig.tight_layout()
    fig.savefig(FIGS / "fig_ukin_3_exposure.png", dpi=150)
    plt.close(fig)


def cell(fit, name: str) -> str:
    c = fit.params[name]
    s = fit.bse[name]
    p = fit.pvalues[name]
    stars = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""
    return f"{c:.3f}{stars} ({s:.3f})"


def write_tables(trade_res, labour_res, expo_res) -> None:
    rows = [
        ("Model 1: DiD, log UK employment, core×post (SOC 2121+3120)",
         cell(labour_res["did"], "core_post"),
         int(labour_res["did"].nobs), "APS 16 occ × 16 quarters; cluster by SOC"),
        ("  pre-trend placebo (core×fake-post, pre-period)",
         cell(labour_res["placebo"], "core_fake"),
         int(labour_res["placebo"].nobs), "should be ~0"),
        ("Model 2: ITS, log UK←India SJ3, post-2022 shift",
         cell(trade_res["its"], "post"),
         int(trade_res["its"].nobs), "BaTIS 2015–2024; HC1"),
        ("  pre-trend placebo (fake shock 2019, pre-sample)",
         cell(trade_res["placebo"], "fake_post"),
         int(trade_res["placebo"].nobs), "should be ~0"),
        ("Model 3: cross-occupation slope, Δlog emp on exposure β",
         f"{expo_res['fit'].params['beta']:.3f} ({expo_res['fit'].bse['beta']:.3f})",
         int(expo_res["fit"].nobs), "civil occupations with Eloundou scores"),
    ]
    df = pd.DataFrame(rows, columns=["specification", "coef (se)", "n", "note"])
    df.to_csv(TABLES / "tbl_ukin_model.csv", index=False)
    print(df.to_string(index=False))

    trade_res["d"][["year", "sj3", "lsj3"]].to_csv(TABLES / "tbl_ukin_trade_series.csv", index=False)
    expo_res["all"].to_csv(TABLES / "tbl_ukin_exposure.csv", index=False)


def main() -> None:
    trade = load_trade()
    aps = load_aps()

    trade_res = model_trade(trade)
    labour_res = model_labour(aps)
    expo_res = model_exposure(aps)

    print("=" * 64)
    print("UK-India generative-AI model")
    print("=" * 64)
    print(f"UK←India SJ3 pre-2022 CAGR: {trade_res['pre_cagr']*100:.1f}%/yr")
    print(f"UK←India SJ3 2022→2024 growth: {trade_res['post_growth']*100:.1f}%")
    print()
    write_tables(trade_res, labour_res, expo_res)

    figure_trade(trade_res)
    figure_employment(aps)
    figure_exposure(expo_res, aps)
    print("\nfigures: fig_ukin_1_trade.png, fig_ukin_2_employment.png, fig_ukin_3_exposure.png")
    print("done")


if __name__ == "__main__":
    main()
