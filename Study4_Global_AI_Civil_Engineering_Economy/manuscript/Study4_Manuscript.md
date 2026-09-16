# Generative AI and the Cross-Border Civil Engineering Economy

**Occupation exposure, sectoral adoption, Mode-1 versus Mode-3 trade, and a 17-country robustness check**

Study 4 working paper · 16 September 2026  
Replication: `Study4_Global_AI_Civil_Engineering_Economy/scripts/run_analysis.py`

**Claim boundary.** This paper does **not** identify that a decline in civil-engineer headcount in country *A* causes engineer counts or GDP in country *B*. The objects that can be measured are (i) UK task substitution inside civil-adjacent SOC codes, (ii) bilateral Mode-1 / Mode-3 services trade, and (iii) whether importer professional-AI *acceleration* predicts those imports in a European panel.

---

## Abstract

Generative AI is uneven inside civil engineering: drafting, CAD/BIM and quantity-surveying tasks are more exposed than licensed design and on-site construction. Using official series only, we document three facts.

First, in the UK Annual Population Survey, SOC 2121 civil engineers fell 14.3% from December 2021 to September 2025, while SOC 3120 CAD/drawing technicians fell 23.9% and SOC 2453 quantity surveyors fell 14.0%. SOC 3114 building and civil engineering technicians rose 214.5%. That is task reallocation, not a uniform occupation collapse.

Second, OECD–WTO BaTIS balanced imports of SJ3 (technical, trade-related and other business services) from India to the UK rose from USD 2.19 billion (2019) to 4.98 billion (2024). UK imports of construction services (SE) from China rose 52% over the same window. UK log 2121 employment and log India SJ3 imports move in opposite directions (correlation −0.89, *n* = 4 years).

Third, a 17-country European panel that matches Eurostat NACE M versus F enterprise AI to BaTIS SJ3 from India, the Philippines and Viet Nam does **not** yield a significant post-2023 × ΔM-AI coefficient (0.000, s.e. 0.006, *N* = 336). The same specification on an eight-country subsample is 0.019 (s.e. 0.006). Event-study coefficients on year × ΔM are already positive in 2018 relative to 2022. The EU-8 interaction is therefore sample-dependent and fails a pre-trend check on the expanded panel. Placebos (computer services, Chinese SE/SJ3, construction AI) are also null.

The contribution is a civil-specific **five-layer stack**—exposure × sectoral adoption × **NACE M71 industry** × GATS mode × placebos—and an honest robustness result: **Mode-1 trade and UK task substitution are in the data; a stable causal spillover from importer professional AI to partner SJ3 or to domestic M71 GVA is not.**

**Keywords:** generative AI; civil engineering; NACE M71; Mode 1; BaTIS; Eurostat; India; China.

---

## 1. Introduction

A tempting sentence is: “AI reduces civil engineers in the UK, so India loses (or gains) civil engineers and GDP.” That sentence is not identified. ILO does not publish bilateral ISCO 2142 counts. APS 2121 is an importer labour-market outcome, not a shock. Construction GVA is not a valid World Bank indicator (`NV.IND.CONS.ZS` returns API error 120).

What *can* be measured, with public data, is a three-layer object:

1. **Exposure** differs within the civil family (Study 1 LLM panel; Eloundou drafters vs 17-2051).
2. **Adoption** differs by NACE: Eurostat enterprise AI in professional services (M) versus construction (F).
3. **Delivery mode** differs by partner: India/Philippines/Viet Nam as Mode-1 SJ3 exporters; China as Mode-3 SE contractors.

Relative to an eight-country first pass, this draft **expands Eurostat–BaTIS coverage to 17 EU importers**, adds leave-one-out and pre-trend placebos, widens the UK APS bundle to CAD technicians, quantity surveyors and construction project managers, and adds the **NACE M71** national-accounts layer (architectural and engineering activities) plus BaTIS **SJ1/SJ2** placebos. BaTIS does **not** publish SJ311/SJ312; SJ3 is the official ceiling. Eurostat does **not** publish M71 in the AI survey.

The full have / missing catalogue is `DATA_INVENTORY.md`.

---

## 2. Data

All files under `Study4_Global_AI_Civil_Engineering_Economy/data/` were downloaded on 16 September 2026. See `DATA_SOURCES.md`.

**Occupation exposure (UK Study 1, 50 occupations × 3 models × 20 runs).** Pooled means: civil engineer 3.00; civil engineering technician 2.67; BIM/CAD technician 4.33; quantity surveyor 4.00; construction project manager 2.67 (1–5 scale).

**Eurostat** `isoc_eb_ain2`, E_AI_TANY, enterprises 10+, NACE F and M, 2021/23/24/25. EU-27 M: 17.39, 18.66, 30.53, 40.43. EU-27 F: 4.62, 3.20, 6.09, 10.79. NACE M71 is not in this dataset (HTTP 400); M is the finest official engineering-inclusive AI series.

**OECD–WTO BaTIS**, USD million, adjustment **B**, services SJ3, SE, SI, 2015–2024. 15,120+ balanced cells after filters.

**ILOSTAT** employment by ISIC F and M, 2018–2025 extract. China is not in the extract. India is.

**ONS APS** SOC 2020 codes 2121, 3114, 3120, 2453, 2455, status A.

**World Bank** NY.GDP.MKTP.CD, NV.SRV.TOTL.ZS, NV.IND.TOTL.ZS.

**Microsoft** AI User Share, Q1 2026 update (economy-wide; 2025–26, not usable as a 2015–24 shock).

---

## 3. Design

For importer *i* in the Eurostat–BaTIS overlap, partner *j* ∈ {IND, PHL, VNM}, *t* = 2018…2024:

\[
\log M^{SJ3}_{ijt}=\alpha_i+\delta_t+\gamma_j+\beta(\mathbf{1}[t\ge 2023]\times \Delta M_i)+\varepsilon_{ijt}
\]

\(\Delta M_i\) is Eurostat NACE M AI in 2024 minus 2021. Standard errors clustered by importer. Estimation is iterative within transformation (importer, year, partner).

Placebos replace the outcome with SI, SE from China, SJ3 from China, or SE from Mode-1 partners; or replace \(\Delta M\) with \(\Delta F\).

The expanded importer set is AUT, BEL, CZE, DEU, DNK, ESP, FIN, FRA, GRC, HUN, IRL, ITA, NLD, POL, ROU, SWE (Portugal has no 2024 M AI, so \(\Delta M\) is missing). The EU-8 subsample is DEU, FRA, NLD, POL, ITA, ESP, IRL, ROU.

---

## 4. Results

### 4.1 UK civil-adjacent employment

| SOC | Occupation | Dec 2021 | Sep 2025 | Change |
|---|---|---:|---:|---:|
| 2121 | Civil engineers | 115,800 | 99,200 | **−14.3%** |
| 3120 | CAD, drawing and architectural technicians | 72,900 | 55,500 | **−23.9%** |
| 2453 | Quantity surveyors | 63,000 | 54,200 | **−14.0%** |
| 3114 | Building and civil engineering technicians | 5,500 | 17,300 | **+214.5%** |
| 2455 | Construction project managers | 107,500 | 112,300 | **+4.5%** |

The occupation with the highest Study 1 exposure in this bundle (CAD/BIM, 4.33) contracted more than licensed civil engineers (3.00). Technicians expanded. Project managers, less exposed to drafting, were flat-to-up. This is the micro novelty: **generative AI shows up as polarisation inside the civil family**, not as a single headcount.

ILO UK ISIC M employment *rose* 21.8% from 2019–24 while ISIC F fell 7.6%. APS 2121 can fall while professional-services employment rises; M is broader than civil engineers.

### 4.2 Trade corridors (BaTIS balanced, USD million)

| Corridor | 2019 | 2024 | Change |
|---|---:|---:|---:|
| UK ← India SJ3 | 2,187 | 4,979 | +128% |
| UK ← India SI | 2,215 | 4,723 | +113% |
| UK ← China SE | 119 | 180 | +52% |
| Germany ← India SJ3 | 660 | 926 | +40% |
| Germany ← Poland SJ3 | 1,516 | 2,328 | +54% |
| France ← India SJ3 | 524 | 830 | +58% |
| Netherlands ← India SJ3 | 831 | 967 | +16% |
| US ← India SJ3 | 2,398 | 2,585 | +8% |
| Australia ← India SJ3 | 167 | 250 | +50% |

UK 2121 (annual mean) versus UK←India SJ3, 2021–24: corr(logs) = −0.89, *n* = 4. Direction: importer engineer counts down, Mode-1 imports up. Four points are not an elasticity.

### 4.3 European panel

| Spec | Coef. (s.e.) | *N* |
|---|---|---:|
| (2) EU-16: Post × ΔM 2021–24 | 0.000 (0.006) | 336 |
| (10) EU-16: time-varying M AI | 0.003 (0.003) | 150 |
| (5)–(8) Placebos SI / China SE / China SJ3 / Mode-1 SE | all insignificant | 112–336 |
| (13) Fake post=2020 × ΔM, 2018–21 | −0.000 (0.005) | 192 |
| (H) Viet Nam only | 0.010 (0.006), *p*=0.10 | 112 |
| (16) Cross-section Δlog India SJ3 2022–24 on ΔM | 0.007 (0.004), *p*=0.13 | 16 |
| **(17) EU-8 only: Post × ΔM** | **0.019\*\*\* (0.006)** | 168 |
| **(18) EU-8 only: time-varying M** | **0.023\*\* (0.010)** | 72 |

Leave-one-out on EU-16: every drop stays near zero except dropping Sweden (0.010, *p*=0.08). Portugal is already out of (2) because 2024 M AI is missing.

Event study (year × ΔM, omit 2022): 2018 = 0.017 (*p*=0.049); 2023 = 0.011 (*p*=0.005); 2024 = 0.013 (*p*=0.016). Pre-2022 is not flat. We do not interpret 2023–24 as a GenAI break.

**Reading.** The eight-country coefficient is real in that sample and matches the first-pass study. It does not survive adding Austria, Belgium, Czechia, Denmark, Finland, Greece, Hungary, Spain’s neighbours, Sweden. A paper that stopped at EU-8 would over-claim. This draft treats (17)–(18) as a **fragility result**, not a headline causal estimate.

### 4.6 NACE M71: the civil-industry object (not ISIC F, not all of M)

NACE M71 is architectural and engineering activities. It is the closest official industry to civil consultancies. Eurostat national accounts provide M71 GVA and employment; the UK series stops in **2018**, so it cannot overlap GenAI. For EU members with 2019 and 2023:

Spain’s M71 GVA rose 47.1% while construction F rose 6.8%; Germany’s M71 rose 14.7% while F rose 30.5%; Italy’s F outpaced M71. These are current-euro changes (inflation included).

On 2018–2023, country and year FE, Post×ΔM on log M71 GVA is **−0.006 (0.005), N=90**. The same specification on construction GVA is **−0.008 (0.004)**. Time-varying M AI in 2021/23 on M71 is 0.000 (0.004). Domestic engineering GVA is not the channel through which the 2023–24 professional-AI jump shows up.

Eloundou occupation file (official `occ_level.csv`): civil engineers β_human **0.375**; architectural and civil drafters **0.52**; civil engineering technologists **0.477**. That ranking matches the UK APS polarisation (CAD −23.9% vs 2121 −14.3%).

### 4.7 SJ1 and SJ2 placebos

BaTIS service list for GBR←IND contains SJ, SJ1, SJ2, SJ3 but **not** SJ311/SJ312. Post×ΔM on log SJ2 (consulting) = 0.007 (0.007); SJ1 (R&D) = 0.003 (0.009); N=336. Neighbouring EBOPS headings do not restore a trade effect.

### 4.4 Exporter labour markets (ILO, 2019–2024)

Professional (M) versus construction (F) employment: Philippines +39.9% / +12.8%; Viet Nam +28.5% / −1.4%; Poland +30.4% / +0.3%; India +13.0% / +33.0%. India expanded on-site construction faster than professional services—the opposite of a Mode-1-only story. China remains missing from ILO F/M.

---

## 5. Case notes

**UK–India.** High Microsoft diffusion (42.2% in Q1 2026) but no Eurostat M series after Brexit. The identified UK facts are APS polarisation plus SJ3, not a regression of Indian GDP on 2121.

**China.** Microsoft Copilot share 16.4% undercounts domestic models. Mode-3 SE to the UK +52% versus Mode-1 SJ3 from India +128%. EU professional-AI intensity does not load on Chinese SE or SJ3.

**Germany–Poland.** Nearshore SJ3 +54% while Microsoft shares are similar (~31%); Eurostat M AI differs (DE 48.3 vs PL 22.2 in 2025). Sectoral AI still discriminates even when Copilot shares do not.

**Sweden.** Largest ΔM in the intensity table (+37.2 pp). LOO suggests Sweden pulls the expanded panel toward zero; dropping it still does not restore the EU-8 magnitude.

---

## 6. Limitations

SJ3 is broader than M71 engineering; SJ311/SJ312 are not in BaTIS. M71 GVA is current prices. UK M71 national accounts end in 2018. M71 AI adoption is unpublished. Eight clusters in the EU-8 spec are few. Event-study pre-trends fail on the 17-country panel. APS cells have sampling error. BaTIS ends 2024; Eurostat continues to 2025; Microsoft is 2025–26. Balanced BaTIS includes modelled cells (we keep adjustment B only). No bilateral civil-engineer census exists.

---

## 7. Conclusion

Enough novelty remains without a forced causal spillover. The civil family is not one exposure; UK CAD/QS employment fell while technicians rose; Mode-1 SJ3 from India to the UK more than doubled as 2121 declined; Mode-3 Chinese construction services moved less; a 17-country Eurostat–BaTIS test of “importer professional AI causes Mode-1 imports” is a **null that overturns an eight-country significant coefficient**. That null is the result, not a reason to drop the larger sample.

---

## Figures and tables

`figures/figure1`–`figure9`; `tables/table_*.csv`; `DATA_INVENTORY.md`. Sources: Eurostat (including `nama_10_a64` M71), OECD–WTO BaTIS, ILOSTAT, ONS APS, World Bank, Microsoft AI Diffusion Report, Eloundou `occ_level.csv`, Study 1 occupation panel.
