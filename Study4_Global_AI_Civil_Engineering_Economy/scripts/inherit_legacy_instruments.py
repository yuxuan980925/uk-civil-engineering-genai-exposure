#!/usr/bin/env python3
"""Reuse official instruments already in the repo (Felten AIOE, ONS automation, APS).

These files lived in Data_IJCM for the previous occupation paper and in the
desktop Study 4 data_recollect folder. They are not LLM scores.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
SRC = REPO / "Data_IJCM" / "04_external_indices"
DST = ROOT / "data" / "from_legacy_study4"
TAB, FIG = ROOT / "tables", ROOT / "figures"
DST.mkdir(parents=True, exist_ok=True)

COPY = [
    "AIOE_DataAppendix.xlsx",
    "Language_Modeling_AIOE_AIIE.xlsx",
    "AIOE_README.md",
    "ons_automation_probability_soc2010_table9.csv",
    "ons_automation_matches.csv",
    "aps_employment_2021_2025.csv",
]


def main():
    for name in COPY:
        shutil.copy2(SRC / name, DST / name)
    shutil.copy2(REPO / "Data_IJCM" / "06_derived" / "occupation_scores_20run.csv", DST / "occupation_scores_20run.csv")
    shutil.copy2(REPO / "Data_IJCM" / "02_occupation_frame" / "occupation_frame.csv", DST / "occupation_frame.csv")

    aioe = pd.read_excel(DST / "AIOE_DataAppendix.xlsx", sheet_name="Appendix A")
    aioe["SOC Code"] = aioe["SOC Code"].astype(str)
    lm = pd.read_excel(DST / "Language_Modeling_AIOE_AIIE.xlsx", sheet_name="LM AIOE")
    lm["SOC Code"] = lm["SOC Code"].astype(str)
    aiie = pd.read_excel(DST / "AIOE_DataAppendix.xlsx", sheet_name="Appendix B")
    aiie.to_csv(TAB / "article_T12b_aiie_construction.csv", index=False)
    cons = aiie[aiie.NAICS.astype(str).str.startswith("23")].copy()
    cons.to_csv(TAB / "article_T12c_aiie_naics23.csv", index=False)

    rows = [
        dict(SOC2020="2121", occupation="Civil engineers", onet="17-2051",
             eloundou=0.375, aioe=float(aioe.loc[aioe["SOC Code"]=="17-2051","AIOE"].iloc[0]),
             lm_aioe=float(lm.loc[lm["SOC Code"]=="17-2051","Language Modeling AIOE"].iloc[0]),
             ons_auto=0.252381, llm_study1=3.00),
        dict(SOC2020="3114", occupation="Building and civil engineering technicians", onet="17-3022",
             eloundou=0.477, aioe=float(aioe.loc[aioe["SOC Code"]=="17-3022","AIOE"].iloc[0]),
             lm_aioe=float(lm.loc[lm["SOC Code"]=="17-3022","Language Modeling AIOE"].iloc[0]),
             ons_auto=0.377667, llm_study1=2.67),
        dict(SOC2020="3120", occupation="CAD, drawing and architectural technicians", onet="17-3011",
             eloundou=0.520, aioe=float(aioe.loc[aioe["SOC Code"]=="17-3011","AIOE"].iloc[0]),
             lm_aioe=float(lm.loc[lm["SOC Code"]=="17-3011","Language Modeling AIOE"].iloc[0]),
             ons_auto=0.386736, llm_study1=4.33),
        dict(SOC2020="2453", occupation="Quantity surveyors", onet="",
             eloundou=None, aioe=None, lm_aioe=None, ons_auto=0.273715, llm_study1=4.00),
        dict(SOC2020="2455", occupation="Construction project managers", onet="",
             eloundou=None, aioe=None, lm_aioe=None, ons_auto=0.257037, llm_study1=2.67),
    ]
    t = pd.DataFrame(rows)
    aps = pd.read_csv(ROOT / "tables" / "article_T2_uk_aps_all_soc.csv")
    aps["SOC2020"] = aps.SOC2020.astype(str)
    t = t.merge(aps[["SOC2020", "change_pct"]], on="SOC2020", how="left")
    t.to_csv(TAB / "article_T12_multi_instrument.csv", index=False)

    plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 220, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.2))
    m = t.dropna(subset=["eloundou", "change_pct"])
    axes[0].scatter(m.eloundou, m.change_pct)
    for _, r in m.iterrows():
        axes[0].annotate(r.SOC2020, (r.eloundou, r.change_pct), textcoords="offset points", xytext=(4, 4), fontsize=8)
    axes[0].set_xlabel("Eloundou β_human")
    axes[0].set_ylabel("UK APS employment change, 2021–25 (%)")
    axes[0].set_title("GenAI task exposure vs UK headcount")
    m2 = t.dropna(subset=["aioe", "change_pct"])
    axes[1].scatter(m2.aioe, m2.change_pct)
    for _, r in m2.iterrows():
        axes[1].annotate(r.SOC2020, (r.aioe, r.change_pct), textcoords="offset points", xytext=(4, 4), fontsize=8)
    axes[1].set_xlabel("Felten AIOE (2021)")
    axes[1].set_ylabel("UK APS employment change, 2021–25 (%)")
    axes[1].set_title("Pre-GenAI AIOE vs UK headcount")
    fig.tight_layout()
    fig.savefig(FIG / "figure10_instruments_vs_aps.png")
    plt.close()

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    c = cons.sort_values("AIIE")
    ax.barh(c["Industry Title"].str.slice(0, 42), c.AIIE)
    ax.axvline(0, color="0.3", lw=0.8)
    ax.set_xlabel("Felten AIIE (industry AI exposure)")
    ax.set_title("US construction NAICS 23: on-site industries are negatively exposed")
    fig.tight_layout()
    fig.savefig(FIG / "figure11_aiie_construction.png")
    plt.close()
    print(t.to_string(index=False))
    print("copied", list(DST.iterdir()))


if __name__ == "__main__":
    main()
