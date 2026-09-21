# Data sources (retrieved 17 September 2026)

No interpolated occupation or GDP cells. Construction value added `NV.IND.CONS.ZS` is not a valid World Bank indicator (API error 120).

| Series | Publisher | Access |
|---|---|---|
| Enterprise AI by NACE F/M, E_AI_TANY, PC_ENT, GE10 | Eurostat `isoc_eb_ain2` | Statistics API JSON, one geo × nace call |
| GenAI types TNLG/TML/TTM/TIR/TPVSG, NACE F/M/C/J/N | Eurostat `isoc_eb_ain2` | Same API; TNLG is the preferred shock |
| M71 / F / M enterprise turnover, employment, wages | Eurostat SBS `sbs_ovw_act`, `sbs_sc_ovw` | 2021–2024 |
| Compensation D1 and output P1 | Eurostat `nama_10_a64` | Current EUR |
| Balanced trade in services SJ3, SE, SI, USD_EXC, adjustments B / N / F | OECD–WTO BaTIS | SDMX CSV `OECD.SDD.TPS,DSD_BATIS@DF_BATIS`. Adjustment B cells in the preferred 2024 panel are observation status I. Adjustment N (reported) for EU←India SJ3 ends in 2023. Authors do not interpolate. |
| International trade in services, BPM6, SJ31/SJ311/SJ312 | Eurostat `bop_its6_det` | Statistics API JSON; partner China is `CN_X_HK`; Viet Nam empty; UK to 2019 |
| Employment by detailed occupation (ISCO-08 two-digit) | Eurostat `lfsa_egai2d` | Statistics API JSON; OC21 is not civil engineers |
| Employment by sex and economic activity, ISIC F/M | ILOSTAT `DF_EMP_TEMP_SEX_ECO_NB` | SDMX CSV |
| GDP, services share, industry share (archived context; not used in main estimates) | World Bank WDI | `NY.GDP.MKTP.CD`, `NV.SRV.TOTL.ZS`, `NV.IND.TOTL.ZS` |
| AI user share H1 2025–Q1 2026 (archived context; not used in main estimates) | Microsoft AI Diffusion Report | `data/AI_Diffusion_Q12026_Update.csv` |
| UK APS SOC 2020 employment (supplementary context only) | ONS, file in this repo | `Data_IJCM/04_external_indices/aps_employment_2021_2025.csv` |
| LLM occupation scores (legacy comparison only; not the shock) | Study 1 | `Data_IJCM/06_derived/occupation_scores_20run.csv` |

M71 AI adoption is not published in `isoc_eb_ain2`. China ISIC F/M is absent from this ILO pull.
