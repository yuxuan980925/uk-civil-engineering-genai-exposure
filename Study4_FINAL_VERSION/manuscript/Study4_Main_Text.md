# Superseded working note

The IJCM submission is `Study4_Manuscript.md`. This short note is not the article. Occupation APS figures here are supplementary context only and do not identify partner GDP.

# How Does the Civil Engineering Industry Economy Change under an AI Shock?
 Evidence from a Cross-Country Stack

Yuxuan Chai · University of Strathclyde · `yuxuanchai98@outlook.com`  
Working paper · 17 September 2026

Main text only: AI *exposure* inside civil occupations, a generative adoption shock (Eurostat E_AI_TNLG), and measured effects on the cross-country civil-engineering **industry economy** (NACE M71 and Mode-1 SJ3). No interpolated cells. LLM occupation scores from the IJCM paper are not the shock.

**Claim boundary.** A decline in UK SOC 2121 does **not** identify another country’s civil-engineer counts or GDP.

---

## Abstract

Does generative AI exposure change the *civil engineering industry economy*, and does any change stay inside one country? This paper stacks three official objects: (i) task exposure inside civil occupations (Eloundou et al.); (ii) realised **natural-language generation** use in professional services (Eurostat E_AI_TNLG, NACE M, 2024 minus 2023); (iii) industry accounts at NACE **M71** (architectural and engineering activities) and Mode-1 engineering-adjacent trade (OECD–WTO BaTIS SJ3).

Exposure is polarised, not uniform. Eloundou β_human is 0.52 for architectural and civil drafters, 0.477 for civil engineering technicians, and 0.375 for civil engineers. UK APS, December 2021–September 2025: CAD technicians (3120) −23.9%, civil engineers (2121) −14.3%, building and civil technicians (3114) +214.5%.

The industry did not boom where NLG jumped. EU-27 professional NLG rose from 4.55% of enterprises (2023) to 11.51% (2024) and 17.74% (2025); construction NLG stayed at 0.58, 2.42, 3.25. On 17 EU members, post-2024 × ΔTNLG is **−0.007** (s.e. 0.003) on log M71 turnover and **−0.009** on log wages; M71 employment is a precise null. The cross-border association that moves is India Mode-1 SJ3 (**0.021\*\*\***), not China Mode 3, and not generic any-AI (TANY **0.000**).

**Keywords:** generative AI; AI exposure; civil engineering; NACE M71; Mode 1; Eurostat TNLG.

---

## 1. Question

When country A adopts generative AI, how does the civil engineering *industry economy* change—in A’s own M71 firms, and in engineering-related trade with country B? Occupation exposure (Eloundou; Felten AIOE) is not the same object as industry incidence (Eurostat TNLG × SBS M71). Mixing “construction” (NACE F) with engineering consultancies (M71) is a specification error: sites barely use NLG.

Preferred shock: ΔTNLG in NACE M, 2024−2023. Industry outcome: SBS M71 turnover, wages, employment, 2021–24. Trade: BaTIS SJ3 from India / Philippines / Viet Nam. Construction TNLG and China SE are placebos.

---

## 2. AI exposure inside civil occupations

Table 1 matches three UK SOC 2020 unit groups to Eloundou occupation scores. Drafters outrank licensed civil engineers on generative-text exposure. Table 2 and Figure 1 show APS polarisation: high-exposure CAD contracted; technicians 3114 expanded. Figure 2 and Table 3 show why a 2021 ability index is the wrong ranking for 2022–25: Felten AIOE scores civil engineers *above* drafters (1.28 vs 0.92), the reverse of Eloundou and of APS.

Exposure is not incidence (Autor 2015): 3114 is high on Eloundou and still rose 214.5%. The industry question is therefore not “did 2121 fall?” but “did M71 turnover, wages and jobs, and Mode-1 trade, move with NLG?”

---

## 3. Generative shock versus generic AI

Eurostat E_AI_TANY mixes pre-ChatGPT machine learning with language generation. EU-16 post × ΔM TANY on log SJ3 is **0.000 (0.006)**. Figure 3 and Table 5 isolate NLG: EU-27 M TNLG 2.60 (2021), 4.55 (2023), 11.51 (2024), 17.74 (2025). Figure 4: 2024 professional NLG is high in Denmark, Finland and Sweden and low in France and Romania; construction (F) is far lower. Figure 5: ICT (J) NLG is higher still—the shock is a national generative wave, not an M71-only survey cell (M71 AI is unpublished).

---

## 4. Cross-country industry economy

**Domestic M71 (Table 6, Figures 7–8).** Nominal M71 turnover rose in almost every member in 2021–24 (Table 7); that path is recovery and prices, not GenAI. DiD: where ΔTNLG was larger, log M71 turnover grew **more slowly** (−0.007**), as did wages (−0.009***); employment **0.000**. Construction turnover is also negative (−0.010***). High-NLG Europe did not expand its engineering-consultancy industry.

**Mode 1 (Table 5, Figure 6).** Post-2024 × ΔTNLG on log SJ3 is 0.007**; India only 0.021***. Philippines and Viet Nam are not significant. China SE (Mode 3) is null. Computer services SI is null. Generic TANY is null. The cross-border movement that lines up with NLG is India Mode-1 SJ3, not partner GDP identified from UK 2121.

---

## 5. What this does and does not say

Task-based automation predicted polarisation inside civil offices (Tables 1–3, Figures 1–2). Industry accounts show no M71 expansion under TNLG (Table 6, Figures 7–8). Globotics predicted Mode 1; the data show it for India SJ3 only (Figure 6). APS 2121 is an outcome in one labour market, not an instrument for another country’s GDP.

---

## References (main text)

Acemoglu, D., & Restrepo, P. (2018, 2019, 2020). Automation, tasks, and the labour share / displacement and reinstatement. *AER / JEP / Carnegie-Rochester*.

Autor, D. H. (2015). Why are there still so many jobs? *JEP*.

Autor, D. H., Levy, F., & Murnane, R. J. (2003). The skill content of recent technological change. *QJE*.

Baldwin, R. (2016, 2019). *The great convergence*; *The globotics upheaval*.

Eloundou, T., Manning, S., Mishkin, P., & Rock, D. (2023, 2024). GPTs are GPTs. *Science* / NBER.

Eurostat. `isoc_eb_ain2` (E_AI_TNLG); SBS `sbs_ovw_act`, `sbs_sc_ovw` (NACE M71).

Felten, E., Raj, M., & Seamans, R. (2021). Occupational, industry, and geographic exposure to AI. *Organization Science*.

Grossman, G. M., & Rossi-Hansberg, E. (2008). Trading tasks. *AER*.

Noy, S., & Zhang, W. (2023). Experimental evidence on generative AI. *Science*.

OECD & WTO. BaTIS, heading SJ3.

WTO. (1994). GATS.

---

## Figures (main text)

**Figure 1.** UK APS employment change, civil-adjacent SOC 2020, Dec 2021–Sep 2025 (AI-exposure polarisation).

![Figure 1](figures/figure2_uk_aps_bundle.png)

**Figure 2.** APS change versus Eloundou β_human and versus Felten AIOE.

![Figure 2](figures/figure10_instruments_vs_aps.png)

**Figure 3.** EU-27 AI types: professional NLG versus machine learning versus construction NLG.

![Figure 3](figures/figure12_tnlg_vs_tml.png)

**Figure 4.** 2024 NLG use, NACE M versus F, by country.

![Figure 4](figures/figure13_tnlg_2024_MF.png)

**Figure 5.** EU-27 NLG by NACE M, J, C, N, F.

![Figure 5](figures/figure16_tnlg_by_nace.png)

**Figure 6.** ΔM TNLG 2023–24 versus Δ log India SJ3, 2022–24 (cross-country Mode 1).

![Figure 6](figures/figure15_cross_section_tnlg.png)

**Figure 7.** SBS net turnover growth 2021–24, M71 versus construction F.

![Figure 7](figures/figure17_sbs_turnover_m71_vs_F.png)

**Figure 8.** ΔTNLG 2023–24 versus M71 turnover change 2023–24.

![Figure 8](figures/figure19_tnlg_vs_m71_turnover.png)

---

## Tables (main text)

### Table 1. Civil occupation AI exposure (Eloundou)

| SOC2020 | UK occupation | O*NET | Eloundou β_human | Eloundou β_model |
|---|---|---|---|---|
| 2121 | Civil engineers | 17-2051.00 | 0.375 | 0.446 |
| 3114 | Building and civil engineering technicians | 17-3022.00 | 0.477 | 0.591 |
| 3120 | CAD, drawing and architectural technicians | 17-3011.00 | 0.520 | 0.540 |

### Table 2. UK APS, civil-adjacent SOC 2020 (Dec 2021–Sep 2025)

| SOC2020 | occupation | emp_2021_12 | emp_2025_09 | change_pct | Eloundou β_human |
|---|---|---|---|---|---|
| 3120 | CAD, drawing and architectural technicians | 72,900 | 55,500 | -23.9 | 0.520 |
| 2121 | Civil engineers | 115,800 | 99,200 | -14.3 | 0.375 |
| 3114 | Building and civil engineering technicians | 5,500 | 17,300 | 214.5 | 0.477 |

Full 16-group ranking is in `tables/article_T2_uk_aps_all_soc.csv`.

### Table 3. Exposure instruments versus APS (selected civil matches)

| SOC2020 | occupation | Eloundou | Felten AIOE | APS % change |
|---|---|---|---|---|
| 2121 | Civil engineers | 0.375 | 1.283 | -14.3 |
| 3114 | Building and civil engineering technicians | 0.477 | 0.932 | +214.5 |
| 3120 | CAD, drawing and architectural technicians | 0.520 | 0.923 | -23.9 |

### Table 4. EU-27 NLG use (% of enterprises, 10+)

| NACE | 2021 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| M professional (contains M71) | 2.60 | 4.55 | 11.51 | 17.74 |
| F construction | 0.99 | 0.58 | 2.42 | 3.25 |
| J ICT | 6.34 | 11.14 | 25.83 | 42.23 |

### Table 5. TNLG and Mode-1 SJ3 (selected)

| Specification | Coefficient (s.e.) | N |
|---|---|---|
| Post-2024 × ΔM TNLG | 0.007** (0.003) | 357 |
| India only | 0.021*** (0.008) | 119 |
| Generic TANY Post × ΔM | 0.000 (0.006) | 336 |
| Placebo SI (computer) | -0.002 (0.006) | 357 |
| Placebo China SE (Mode 3) | -0.008 (0.009) | 119 |

### Table 6. M71 industry economy under TNLG (SBS 2021–24)

| Specification | Coefficient (s.e.) | N |
|---|---|---|
| log M71 turnover | -0.007** (0.003) | 68 |
| log M71 employment | -0.000 (0.002) | 68 |
| log M71 wages | -0.009*** (0.003) | 68 |
| log M71 value added | -0.006*** (0.002) | 68 |
| log F turnover (placebo) | -0.010*** (0.003) | 68 |
