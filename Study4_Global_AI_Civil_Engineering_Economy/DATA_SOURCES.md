# Data sources (retrieved 17 September 2026)

No interpolated occupation or GDP cells. Construction value added `NV.IND.CONS.ZS` is not a valid World Bank indicator (API error 120).

| Series | Publisher | Access |
|---|---|---|
| Enterprise AI by NACE F/M, E_AI_TANY, PC_ENT, GE10 | Eurostat `isoc_eb_ain2` | Statistics API JSON, one geo × nace call |
| GenAI types TNLG/TML/TTM/TIR/TPVSG, NACE F/M/C/J/N | Eurostat `isoc_eb_ain2` | Same API; TNLG is the preferred shock |
| Internet users, broadband, R&D / GDP | World Bank WDI | Context only, not the DiD shock |
| Balanced trade in services SJ3, SE, SI, USD_EXC, adjustment B | OECD–WTO BaTIS | SDMX CSV `OECD.SDD.TPS,DSD_BATIS@DF_BATIS` |
| Employment by sex and economic activity, ISIC F/M | ILOSTAT `DF_EMP_TEMP_SEX_ECO_NB` | SDMX CSV |
| GDP, services share, industry share | World Bank WDI | `NY.GDP.MKTP.CD`, `NV.SRV.TOTL.ZS`, `NV.IND.TOTL.ZS` |
| AI user share H1 2025–Q1 2026 | Microsoft AI Diffusion Report | `data/AI_Diffusion_Q12026_Update.csv` |
| UK APS SOC 2020 employment | ONS, file in this repo | `Data_IJCM/04_external_indices/aps_employment_2021_2025.csv` |
| LLM occupation scores | Study 1 | `Data_IJCM/06_derived/occupation_scores_20run.csv` |

M71 AI adoption is not published in `isoc_eb_ain2`. China ISIC F/M is absent from this ILO pull.
