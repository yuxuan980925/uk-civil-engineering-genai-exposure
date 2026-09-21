# Reset research question: generative AI and transnational civil-engineering relocation

Retrieved 21 September 2026. No interpolated ITS, occupation or BaTIS cells.

## Why the question was reset

The motivating claim — *generative AI caused civil-engineering work, jobs or GDP to move across countries* — is larger than any official series in this repository. ILOSTAT does not publish ISCO 2142 (civil engineers) in this pull. OECD–WTO BaTIS does not publish EBOPS SJ312. The United Kingdom drops out of Eurostat ITS after 2019. There is no enterprise-NLG survey for the UK, India or China.

What *can* be asked, and tested, is a narrower relocation hypothesis:

> Among EU importers, is the 2023–24 jump in professional-service use of natural-language-generation AI associated with a shift toward digitally deliverable Indian **engineering** services relative to Chinese construction and Chinese engineering services, and with slower nominal NACE M71 turnover but **not** falling M71 employment?

That pattern would be consistent with **task unbundling** (drawings, calculations and reports sourced remotely) rather than **headcount relocation** of licensed civil engineers. It is still an association, not an identified causal effect of generative AI.

## Research questions

| ID | Question | Series | Verdict in these files |
|---|---|---|---|
| RQ1 | Is bilateral engineering trade (SJ312) published for the GenAI window? | Eurostat `bop_its6_det`; BaTIS; ILO 2142 | **Yes for Eurostat ITS** (India, China except Hong Kong, Philippines). **No** for BaTIS SJ312, ILO 2142, Viet Nam ITS, or UK ITS after 2019. |
| RQ2 | Does importer ΔTNLG covary with Indian engineering / SJ3 imports? | BaTIS B SJ3; Eurostat ITS SJ312/SJ31/SJ3 | **Yes, association.** India SJ3 (BaTIS B) 0.021*** (0.008), N=119. India SJ312 (ITS) 0.026* (0.014), N=96. India ITS SJ3 0.035** (0.015), N=119. Architectural SJ311 is null. |
| RQ3 | Does the same shock raise Chinese construction or Chinese engineering? | BaTIS SE/SJ3; ITS SJ312 | **No.** Chinese SE −0.008 (0.009). Chinese SJ312 −0.062** (0.027). Indian SI −0.009*. Project relocation and a generic computer-services channel are not supported. |
| RQ4 | Does a relocation index (India minus China) rise with ΔTNLG? | log IN SJ3 − log CN SE; log IN SJ312 − log CN SJ312 | **Panel yes, 2022–24 cross-section no.** BaTIS index 0.029** (0.013), N=119; ITS engineering index 0.101*** (0.035), N=86. Cross-section of the BaTIS index is −0.001 (0.012). Event-study 2019 is also significant, so pre-trends are not clean. |
| RQ5 | Is M71 employment falling where NLG and Indian engineering rise? | Eurostat SBS M71 | **Employment 0.000 (0.002); turnover −0.007**; wages −0.009***. Inconsistent with simple headcount offshoring. |
| RQ6 | Do *reported* BaTIS cells change RQ2? | Adjustment N vs B | Reported EU←India SJ3 **ends in 2023**. Post-2023 coefficient remains 0.021* (0.012), N=102. UK reported SJ3 2019→2024 is 2,543 → 6,741 USD million, larger than balanced B (2,187 → 4,979). |
| RQ7 | Did UK high-exposure civil occupations fall after 2022? | ONS APS SOC 2020 | **Descriptive polarisation, not identified.** Civil engineers 2121 −12.5%; CAD 3120 −21.0%; technicians 3114 +196.8%; physical scientists 2114 +15.3%. No Indian/Chinese occupation counterpart. |
| RQ8 | Did EU science-and-engineering professionals fall where NLG jumped? | Eurostat `lfsa_egai2d` OC21 | **No.** OC21 −0.001 (0.004). ICT professionals and building trades decline with ΔTNLG; that is not a civil-engineer count. |

## What was newly retrieved

Official APIs only. Empty cubes are stored as logs, not filled.

| Object | Result | File |
|---|---|---|
| Eurostat ITS SJ31 / SJ311 / SJ312 / SJ3 / SE / SI, EU reporters × IN / CN_X_HK / PH / VN, 2015–2024 | **6,338 cells.** China partner code is `CN_X_HK`. Viet Nam cube is empty. UK ITS stops in 2019. India SJ312 debit: 16 reporters in 2024; 14–15 have both 2022 and 2024. | `09_relocation_probe/eurostat_its_engineering.csv` |
| Eurostat LFS ISCO-08 two-digit employment | **1,421 cells** for OC21/OC31/OC25/OC71 and aggregates. Not ISCO 2142. | `09_relocation_probe/eurostat_lfsa_occ2d.csv` |
| ILOSTAT occupation employment 2142 / 214 / 21 / 2 | **HTTP 404** at every attempted code | `09_relocation_probe/ilo_occupation_fetch_log.csv` |
| BaTIS SJ312 / SJ31 | **OECD SDMX 404** | already documented |
| BaTIS reported (N) vs balanced (B) | Already in `03_trade/batis_civil_related.csv`. EU←India SJ3 reported **has no 2024**. | `09_relocation_probe/tables/uk_corridors_B_vs_N.csv` |

## Honest interpretation

The new ITS evidence **tightens** the trade object from “technical and other business services (SJ3)” toward **engineering services (SJ312)**. Indian SJ312 covaries positively with importer NLG; Chinese SJ312 covaries negatively; architectural services do not. Combined with flat M71 employment, the data are consistent with a **supplier-mix shift in engineering services** during the first NLG wave, not with licensed civil engineers leaving EU payrolls.

They still do not show that generative AI *caused* that shift. Eurostat ITS is reporter-published and unbalanced (missing years are dropped). The BaTIS relocation-index event study is not free of pre-2022 coefficients. SJ312 is all engineering, not civil engineering only. GATS mode of supply is not observed.

Do not interpolate Viet Nam ITS, ILO 2142, BaTIS SJ312, UK post-2019 ITS, or 2024 reported BaTIS for the EU panel.

## Corroboration (independent re-collection, 21 September 2026)

A second Eurostat pull was used to support the association, not to manufacture a causal relocation result. Details: `CORROBORATION.md`.

- Re-fetch of India and China-except-HK SJ312: **598/598 cells identical** (DE←IN 2024 = 390 EUR million).
- SJ312 from the United States, United Kingdom, Switzerland, Japan and extra-EU: **all null**. The India coefficient is not a generic engineering-import boom.
- Indian share of extra-EU SJ312: **0.382\* (0.202)** pp, N=93.
- Dropping Finland: India SJ312 **0.020\* (0.012)**.
- NACE **M7112** engineering consultancy (not all of M71): employment **0.000**, output **−0.008**, wages **−0.009** (output and wages p<0.05).
- Inward FATS M71 by controlling country **ends in 2020**; India-controlled affiliates unpublished. Mode 3 cannot be tested against the NLG shock.

## Replication

```bash
python3 Data_Study4_IJCM/07_scripts/download_relocation_series.py
python3 Data_Study4_IJCM/07_scripts/run_relocation_experiments.py
python3 Data_Study4_IJCM/07_scripts/download_corroboration.py
python3 Data_Study4_IJCM/07_scripts/run_corroboration_experiments.py
```

Machine-readable estimates: `Data_Study4_IJCM/09_relocation_probe/results_relocation.json`.
Pretty table: `09_relocation_probe/tables/article_relocation_results.csv`.
