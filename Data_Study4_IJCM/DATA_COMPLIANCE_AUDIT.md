# Study 4 data-compliance audit

Independent check, 21 September 2026, against `Data_Study4_IJCM/` source CSVs and live Eurostat / OECD–WTO APIs.

**Verdict:** Study 4 is built from retrieved official series. Authors do not fill missing occupation, M71 or GDP cells. Main-text Tables 1, 2, 4 and 6, and the headline SJ3 / M71 coefficients, recompute from the CSVs. The study did **not** fully follow the data in three places; those are corrected in this revision.

## What follows the data

| Claim | Check |
|---|---|
| Table 1 UK–India / UK–China 2019–24 levels and % | Exact match to `batis_uk_india_china.csv` (120 rows). Live OECD SDMX returns the same cells (e.g. GBR←IND SJ3 2019 = 2186.610935, 2024 = 4979.295577). |
| Table 2 EU-27 TNLG | Exact match to `eurostat_ai_genai_types.csv`. Live Eurostat `isoc_eb_ain2` returns M 2.60 / 4.55 / 11.51 / 17.74 and F 0.99 / 0.58 / 2.42 / 3.25. Germany M also matches (2.48, 5.98, 12.28, 14.74). |
| Table 3 Indian SJ3 0.021*** (0.008), N=119 | Recomputed: 0.021 (0.008), p=0.007, 17 importers × 2018–24. Dummy two-way FE gives 0.021 (0.009), p=0.015. |
| Table 3 pooled SJ3 Post-2024 0.007** (0.003), N=357 | Recomputed. Partners are **India, the Philippines and Viet Nam** (17 × 3 × 7). |
| Table 3 China SE −0.008 (0.009), China SJ3 0.005 (0.010) | Recomputed, both n.s. |
| Table 3 generic any-AI 0.000 (0.006), N=336 | Recomputed. Portugal has no TANY 2021–24 pair, so 16 importers × 3 partners × 7 years. |
| Table 4 M71 SBS, N=68 | 17 countries × 2021–24, no missing turnover cells. Turnover −0.007** (0.003) recomputes. |
| Table 6 claim boundary | Matches what the series can identify. |
| Failed pulls (OWID, IMF AIPI, OECD ICT, M71 AI, ILO M71) | Logged and not filled. |
| `log(value.clip(0.01))` | Does not bind in the headline trade samples (all values > 0.37). |
| APS 2121 / 3114 / 3120 % changes in the inventory | Match `Data_IJCM` APS (115800→99200; 5500→17300; 72900→55500). Main text does not use them as the shock. |
| Eloundou 17-2051.00 / 17-3011.00 / 17-3022.00 | human β = 0.375 / 0.52 / 0.477 as catalogued. |

Scripts drop missing rows (`dropna`); they do not interpolate.

## Issues found and corrected

### 1. Table 3 mislabelled the computer-services comparison (material)

The row “Indian computer services comparison, −0.002 (0.006), N=357” was specification N11: **pooled SI from India, the Philippines and Viet Nam**, not India-only SI.

India-only SI, the comparison the text describes, is **−0.009\* (0.005), N=119** (p=0.090). The pooled analogue remains −0.002 (0.006), N=357.

Table 3, notes, and the results prose now report the India-only SI estimate. The qualitative claim (SI does not rise with importer NLG the way Indian SJ3 does) still holds.

### 2. Every trade cell used in Table 1 and the EU panels is OECD–WTO imputed (disclosure)

`OBS_STATUS = I` for:

- all 120 UK–India–China corridor cells
- all 119 India-SJ3 panel cells
- all 357 pooled SJ3 panel cells

The authors did not invent these numbers; they are the official BaTIS adjustment-B balanced series, and live SDMX returns the same `I` flag. Reported (`A`) values exist under other adjustments but are incomplete. The previous wording (“some observations are … imputed”) understated this. Section 3.5, `DATA_SOURCES.md` and Table 3 notes now state it.

### 3. Table 5 65.4% vs 47.5% depends on the median tie

Spain’s ΔTNLG equals the 17-country median (7.48). Assigning Spain to the **higher** group (the stored table) gives 65.4% vs 47.5%. A strict greater-than split gives **56.5% vs 54.9%**. In both splits, higher-NLG destinations do **not** grow faster, so the qualitative claim stands; the size of the contrast does not. The Table 5 note now reports the tie rule and the alternative split.

### 4. Leftover Mode-1 / Mode-3 labels

The English IJCM manuscript already says BaTIS does not identify GATS modes. Chinese copies and `DATA_INVENTORY.md` still called Indian SJ3 “Mode 1” and Chinese SE “Mode 3”. Those labels are removed.

## What the data still cannot support (unchanged)

- AI **causing** UK–India or UK–China bilateral changes (UK is outside Eurostat TNLG).
- Civil-specific SJ312 invoices (SJ3 is broader).
- Bilateral civil-engineer employment or GDP relocation.
- M71-specific enterprise NLG (survey is NACE M).
- A construction-versus-engineering split in the domestic SBS slowdown (NACE F turnover is also negative).

Word `.docx` copies were not regenerated in this pass; markdown, HTML and CSV tables are the corrected record.
