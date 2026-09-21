#!/usr/bin/env python3
"""Study 4 article assets from official series only (not Study 1 LLM scores)."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA, TAB, FIG = ROOT / "data", ROOT / "tables", ROOT / "figures"
ART = ROOT / "manuscript" / "tables_for_article.md"

# SOC 2020 -> Eloundou O*NET (documented; only clean civil matches)
CROSSWALK = [
    ("2121", "Civil engineers", "17-2051.00", "Civil Engineers"),
    ("3114", "Building and civil engineering technicians", "17-3022.00", "Civil Engineering Technologists and Technicians"),
    ("3120", "CAD, drawing and architectural technicians", "17-3011.00", "Architectural and Civil Drafters"),
]


def md_table(df: pd.DataFrame, cols=None, fmt=None) -> str:
    if cols:
        df = df[cols].copy()
    fmt = fmt or {}
    lines = ["| " + " | ".join(df.columns) + " |", "|" + "|".join(["---"] * len(df.columns)) + "|"]
    for _, r in df.iterrows():
        cells = []
        for c in df.columns:
            v = r[c]
            if c in fmt and pd.notna(v) and isinstance(v, (int, float, np.floating)):
                cells.append(fmt[c] % v)
            elif pd.isna(v):
                cells.append("—")
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main():
    plt.rcParams.update({
        "figure.dpi": 150,
        "savefig.dpi": 220,
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "axes.titlesize": 11,
    })

    el = pd.read_csv(DATA / "eloundou_occ_level.csv")
    rows = []
    for soc, socname, onet, onetname in CROSSWALK:
        hit = el[el["O*NET-SOC Code"] == onet].iloc[0]
        rows.append({
            "SOC2020": soc,
            "UK occupation": socname,
            "O*NET": onet,
            "O*NET title": onetname,
            "Eloundou β_human": float(hit.human_rating_beta),
            "Eloundou β_model": float(hit.dv_rating_beta),
        })
    t_exp = pd.DataFrame(rows)
    t_exp.to_csv(TAB / "article_T1_exposure_crosswalk.csv", index=False)

    aps = pd.read_csv(DATA / "from_study1" / "aps_employment_2021_2025.csv")
    aps["soc"] = aps.SOC2020_FULL_NAME.str.extract(r"^(\d{4})")
    aps["name"] = aps.SOC2020_FULL_NAME.str.replace(r"^\d{4}\s*:\s*", "", regex=True)
    aps = aps[aps.OBS_STATUS == "A"].copy()
    aps["emp"] = pd.to_numeric(aps.OBS_VALUE, errors="coerce")
    chg = []
    for soc, g in aps.groupby("soc"):
        a = g[g.DATE == "2021-12"]
        b = g[g.DATE == "2025-09"]
        if a.empty or b.empty:
            continue
        e0, e1 = float(a.emp.iloc[0]), float(b.emp.iloc[0])
        chg.append({
            "SOC2020": soc,
            "occupation": a.name.iloc[0],
            "emp_2021_12": int(e0),
            "emp_2025_09": int(e1),
            "change_pct": 100 * (e1 / e0 - 1),
        })
    t_aps = pd.DataFrame(chg).sort_values("change_pct")
    t_aps = t_aps.merge(t_exp[["SOC2020", "Eloundou β_human"]], on="SOC2020", how="left")
    t_aps.to_csv(TAB / "article_T2_uk_aps_all_soc.csv", index=False)

    # Figure 2: all APS occupations
    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    t2 = t_aps.sort_values("change_pct")
    colors = ["#3b6d99" if pd.notna(x) else "#888888" for x in t2["Eloundou β_human"]]
    ax.barh(t2.occupation, t2.change_pct, color=colors)
    ax.axvline(0, color="0.3", lw=0.8)
    ax.set_xlabel("Employment change, Dec 2021–Sep 2025 (%)")
    ax.set_title("UK APS civil-adjacent SOC 2020 occupations (status A)")
    fig.tight_layout()
    fig.savefig(FIG / "figure2_uk_aps_bundle.png")
    plt.close()

    # Identification table already exists — pretty copy
    ident = pd.read_csv(TAB / "table_identification.csv")
    ident_out = ident[["spec", "display", "n", "note"]].copy()
    ident_out.columns = ["Specification", "Coefficient (s.e.)", "N", "Note"]
    ident_out.to_csv(TAB / "article_T5_identification.csv", index=False)

    euro = pd.read_csv(TAB / "table_eurostat_M_F.csv")
    cor = pd.read_csv(TAB / "table_batis_corridors.csv")
    es = pd.read_csv(TAB / "table_event_study.csv")
    ilo = pd.read_csv(TAB / "table_ilo_FM.csv")
    m71 = pd.read_csv(TAB / "table_m71_gva_pct_2019_2023.csv")
    nov = pd.read_csv(TAB / "table_novelty_m71_sj2.csv")
    inten = pd.read_csv(TAB / "table_ai_intensity.csv")
    loo = pd.read_csv(TAB / "table_loo_importer.csv")

    blocks = []
    blocks.append("## Article tables (generated from official series)\n")
    blocks.append("LLM occupation scores from the IJCM paper are **not** used. Exposure is Eloundou et al. matched to SOC 2020; employment is ONS APS.\n")
    blocks.append("### Table 1. Civil occupation exposure (Eloundou occ_level.csv)\n")
    blocks.append(md_table(t_exp, fmt={"Eloundou β_human": "%.3f", "Eloundou β_model": "%.3f"}))
    blocks.append("\n### Table 2. UK APS employment, civil-adjacent SOC 2020 (Dec 2021–Sep 2025)\n")
    show = t_aps.copy()
    show["emp_2021_12"] = show.emp_2021_12.map(lambda x: f"{x:,}")
    show["emp_2025_09"] = show.emp_2025_09.map(lambda x: f"{x:,}")
    show["change_pct"] = show.change_pct.map(lambda x: f"{x:.1f}")
    show["Eloundou β_human"] = show["Eloundou β_human"].map(lambda x: "" if pd.isna(x) else f"{x:.3f}")
    blocks.append(md_table(show, cols=["SOC2020", "occupation", "emp_2021_12", "emp_2025_09", "change_pct", "Eloundou β_human"]))
    blocks.append("\n### Table 3. Eurostat enterprise any-AI use (E_AI_TANY), NACE M vs F (%)\n")
    blocks.append(md_table(euro.round(2)))
    blocks.append("\n### Table 4. BaTIS balanced corridors (USD million)\n")
    c2 = cor.copy()
    for col in ["usd_mn_2019", "usd_mn_2024", "pct"]:
        if col in c2:
            c2[col] = pd.to_numeric(c2[col], errors="coerce").round(1)
    blocks.append(md_table(c2))
    blocks.append("\n### Table 5. Identification (log SJ3 unless noted)\n")
    blocks.append(md_table(ident_out))
    blocks.append("\n### Table 6. Event study: year × ΔM (omit 2022)\n")
    es2 = es.copy()
    es2["coef"] = es2.coef.round(3)
    es2["se"] = es2.se.round(3)
    es2["p"] = es2.p.round(3)
    blocks.append(md_table(es2))
    blocks.append("\n### Table 7. ILO ISIC M vs F employment, 2019–2024 (%)\n")
    ilo2 = ilo[["country", "pct_M", "pct_F"]].copy().round(1)
    blocks.append(md_table(ilo2))
    blocks.append("\n### Table 8. NACE M71 vs F GVA, 2019–2023 current EUR (%)\n")
    m712 = m71.round(1)
    blocks.append(md_table(m712))
    blocks.append("\n### Table 9. M71 GVA and SJ1/SJ2 placebos\n")
    nov2 = nov[["spec", "display", "n"]].copy()
    nov2.columns = ["Specification", "Coefficient (s.e.)", "N"]
    blocks.append(md_table(nov2))
    blocks.append("\n### Table 10. Leave-one-importer-out, Post × ΔM\n")
    loo2 = loo[["dropped", "country", "display", "n"]].copy()
    blocks.append(md_table(loo2))
    blocks.append("\n### Table 11. Importer AI intensity (Eurostat pp)\n")
    inten2 = inten.round(2)
    blocks.append(md_table(inten2))
    nlg = pd.read_csv(TAB / "article_T13_nlg_shock.csv")
    blocks.append("\n### Table 13. Generative NLG shock (log SJ3 unless noted)\n")
    blocks.append(md_table(nlg))
    esn = pd.read_csv(TAB / "table_event_study_tnlg.csv")
    esn2 = esn.copy()
    esn2["coef"] = esn2.coef.round(3)
    esn2["se"] = esn2.se.round(3)
    esn2["p"] = esn2.p.round(3)
    blocks.append("\n### Table 14. Event study: year × ΔM TNLG 2023–24 (omit 2022)\n")
    blocks.append(md_table(esn2))
    eu27 = pd.read_csv(TAB / "table_tnlg_eu27.csv")
    blocks.append("\n### Table 15. EU-27 Eurostat AI types by NACE (% of enterprises, 10+)\n")
    blocks.append(md_table(eu27.round(2)))
    indus = pd.read_csv(TAB / "article_T16_industry_economy.csv")
    blocks.append("\n### Table 16. M71 industry economy under TNLG (SBS 2021–24 and nama)\n")
    blocks.append(md_table(indus))
    sbsg = pd.read_csv(TAB / "table_sbs_m71_growth.csv")
    showg = sbsg[["country", "pct_M71_turn_21_24", "pct_F_turn_21_24", "pct_M71_emp_21_24", "pct_F_emp_21_24", "d_tnlg_M_2324"]].copy()
    showg.columns = ["country", "M71 turnover 21–24 %", "F turnover 21–24 %", "M71 emp 21–24 %", "F emp 21–24 %", "ΔTNLG M 23–24"]
    blocks.append("\n### Table 17. SBS growth, NACE M71 vs F, 2021–2024\n")
    blocks.append(md_table(showg.round(1)))
    ART.write_text("\n".join(blocks) + "\n")
    print("wrote", ART)
    print(t_aps[["SOC2020", "occupation", "change_pct"]].to_string(index=False))


if __name__ == "__main__":
    main()
