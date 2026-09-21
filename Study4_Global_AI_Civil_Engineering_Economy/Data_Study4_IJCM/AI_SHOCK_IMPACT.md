# Redesign: civil-engineering industry economy under an AI shock

Retrieved 21 September 2026. Official cells only. No interpolation.

## Why the study was redesigned

The previous draft led with UK–India and UK–China corridors. Those series have **no enterprise NLG treatment**, so they cannot measure an AI-shock *impact*. The series that do have a realised generative-adoption shock are the Eurostat ICT-usage panel and the overlapping EU industry and trade files.

The object of this paper is therefore:

> Among EU economies, is the 2023–24 jump in professional-service use of natural-language-generation AI associated with (i) slower nominal architectural-and-engineering (NACE M71 / M7112) turnover, wages and value added but not falling employment or labour productivity, and (ii) a shift toward Indian engineering-related services relative to Chinese construction and Chinese engineering services?

That is an **association between a realised GenAI shock and industry-plus-trade outcomes**. It is not a causal account of ISCO 2142 jobs or GDP moving from the UK to India.

UK–India–China corridors remain a descriptive illustration of service mix. They are not the identifying sample.

## Shock

\[
\Delta TNLG_i
=
TNLG^{NACE\,M}_{i,2024}
-
TNLG^{NACE\,M}_{i,2023}
\]

Eurostat `isoc_eb_ain2`, enterprises with at least ten persons, percent using AI to generate written or spoken language. NACE M contains M71 firms; **M71 itself is unpublished** (HTTP 400). Construction (NACE F) and generic any-AI (E_AI_TANY) are comparison shocks. Size-class TNLG (10–49, 50–249, 250+) is retrieved as a robustness split; missing cells are left missing.

## Outcomes and formulas

### (1) Domestic industry impact

For EU members \(i\) and years overlapping SBS (2021–2024):

\[
\log Y_{it}
=
\alpha_i+\delta_t
+
\beta\bigl(\mathbf{1}[t\ge 2024]\times\Delta TNLG_i\bigr)
+
u_{it}.
\]

\(Y\) is, in turn, net turnover, persons employed, wages, value added, gross operating surplus, **apparent labour productivity** (`LABPRY_TEUR`, thousand euro per person employed) and **labour cost per person employed** (`LC_EMP_TEUR`). These last two are Eurostat SBS indicators, not author-filled ratios. Where both value added and employment are published, \(\log(VA/E)\) is reported as a check; it is computed only from co-published cells.

Standard errors clustered by country after an iterative within transformation. Construction (F) and all-professional (M) are industry placebos. NACE **M7112** (engineering consultancy) is the tighter civil-adjacent industry.

### (2) Implied magnitude

A coefficient \(\beta\) is a semi-elasticity. One extra percentage point of \(\Delta TNLG\) is associated with a \(100\beta\) percent change in \(Y\). The interquartile range of \(\Delta TNLG\) in the EU-17 sample, \(IQR\), gives the scale of the first observed GenAI wave:

\[
\widehat{\Delta\log Y}^{IQR}
=
\beta\times IQR(\Delta TNLG).
\]

This is a scaled association, not a welfare estimate.

### (3) Transnational mix

Preferred engineering-trade object is Eurostat ITS **SJ312** (architectural and engineering services). BaTIS **SJ3** remains the balanced, broader backup.

\[
Mix^{eng}_{it}
=
\log M^{SJ312,IND}_{it}
-
\log M^{SJ312,CN}_{it},
\qquad
Mix^{task}_{it}
=
\log M^{SJ3,IND}_{it}
-
\log M^{SE,CN}_{it}.
\]

The same TWFE as (1) is applied to \(\log M^{k}_{it}\) and to \(Mix_{it}\). Placebos: Indian SI; SJ312 from the United States, United Kingdom, Switzerland, Japan and extra-EU.

### (4) Vacancies and hours (if published)

Job-vacancy rates (`jvs_a_nace2`) and national-accounts hours (`nama_10_a64_e`) are retrieved for M71/F/M. Empty cubes are logged, not filled. If a series exists through 2024 it enters (1); otherwise it is coverage only.

### (5) UK illustration (not identified)

UK–India and UK–China BaTIS SJ3/SE/SI, APS SOC 2020 occupations, and the calendar-break formulas in `UK_INDIA_MEASUREMENT.md` describe composition. They do **not** receive \(\Delta TNLG_i\).

## Experiments

| ID | Formula | Rejects what |
|---|---|---|
| A1 | (1) on M71 turnover, wages, VA, employment | “The shock is only a trade story” / “NLG coincides with headcount cuts” |
| A2 | (1) on official LABPRY and LC_EMP | “Slower turnover is only a price or hours story that must raise measured productivity” |
| A3 | (1) on M7112 vs M7111 vs F | “The domestic pattern is all of construction or all of architecture” |
| A4 | (3) Indian SJ312 and Mix | “NLG is unrelated to engineering-service supplier mix” |
| A5 | (3) Chinese SE/SJ312 and SI / extra-EU SJ312 | Generic digital or engineering-import boom |
| A6 | (1) with size-class ΔTNLG if published | Shock is only large-firm ICT |
| A7 | (2) IQR scaling | Coefficients without economic size |
| A8 | (5) UK corridors | Not a test of the shock; reported separately |

## Claim boundary

Supported: association between a realised professional-service NLG jump and (i) slower nominal M71/M7112 activity with flat employment, (ii) Indian engineering-related imports relative to Chinese construction/engineering.

Not identified: M71-specific AI adoption; civil-only invoices; GATS modes; ISCO 2142 relocation; UK/India/China NLG; partner GDP.

## Replication

```bash
python3 Data_Study4_IJCM/07_scripts/download_ai_impact.py
python3 Data_Study4_IJCM/07_scripts/run_ai_impact_experiments.py
```

## Results from the 21 September 2026 impact pull

Shock (EU-17 ΔTNLG NACE M, 2023–24): mean 9.3 pp, median 7.5, IQR 5.83. Size-class TNLG unpublished except GE10. M71 hours (THS_HW) unpublished.

Domestic (Post-2024 × ΔTNLG): M71 turnover −0.007**; employment 0.000; wages −0.009***; VA −0.006***; official LABPRY −0.006***; LC_EMP −0.009***. M7112 employment 0.000; output −0.008**. NACE M vacancy rate 0.002 (0.006). STS M71 turnover index −0.009*.

Trade: Indian SJ312 0.034** (0.013); Chinese SJ312 −0.051**; mix 0.095***; BaTIS Indian SJ3 0.021***; Chinese SE −0.008. Placebo SJ312 partners null.

IQR scaling: about −3.9% M71 turnover and −5.2% wages for a 5.83-point shock. Association, not a welfare effect.
